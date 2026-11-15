// Reference decision engine for the reflective check-in.
// Pure functions over the dataset in ../data. Written in plain JavaScript (Node 18+)
// so it can run in a backend or be ported line by line to Dart for the Flutter app.
//
// Principle: the person's confirmed feelings drive everything. The vision model's
// guesses are only used to pre-fill chips (see prefillChips); decide() never reads them
// as feelings.

import { readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DATA_DIR = join(HERE, '..', 'data');

// Intensity chips -> score. Uncalibrated defaults chosen to sit around the dataset's
// 0.4 "active" and 0.75 "high intensity" thresholds (data/safety.json).
export const LEVEL_SCORE = { 1: 0.45, 2: 0.65, 3: 0.85 };
export const LEVEL_LABEL = { 1: 'a little', 2: 'quite', 3: 'very' };

// Placeholder self-harm cue list. Replace with a reviewed, localised list or a
// dedicated classifier before release; this is a demo safety net, not a screening tool.
const SELF_HARM_CUES = [
  /\bkill(ing)? myself\b/i, /\bsuicid/i, /\bself[- ]?harm/i, /\bhurt(ing)? myself\b/i,
  /\bend (it|my life)\b/i, /\bwant to die\b/i, /\bdon'?t want to (be here|live|exist)\b/i,
  /\bno (reason|point) (to|in) (live|living|going on)\b/i, /\bdisappear forever\b/i,
];

function readJson(dir, name) { return JSON.parse(readFileSync(join(dir, name), 'utf8')); }

function readCsv(dir, name) {
  const text = readFileSync(join(dir, name), 'utf8');
  const rows = [];
  let row = [], field = '', inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQuotes) {
      if (ch === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (ch === '"') inQuotes = false;
      else field += ch;
    } else if (ch === '"') inQuotes = true;
    else if (ch === ',') { row.push(field); field = ''; }
    else if (ch === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (ch !== '\r') field += ch;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const [header, ...body] = rows;
  return body.filter(r => r.length > 1).map(r => Object.fromEntries(header.map((h, i) => [h, r[i] ?? ''])));
}

const splitIds = s => (s || '').split(';').map(x => x.trim()).filter(Boolean);

export function loadData(dataDir = DEFAULT_DATA_DIR) {
  const activities = new Map(readJson(dataDir, 'activities.json').activities.map(a => [a.id, a]));
  const emotions = readJson(dataDir, 'emotions.json');
  const recs = readJson(dataDir, 'recommendations.json').by_emotion;
  const safety = readJson(dataDir, 'safety.json');
  const pairs = new Map(readCsv(dataDir, 'combination_matrix.csv').map(r => [r.pair_key, r]));
  const triples = new Map(readCsv(dataDir, 'combination_triples.csv').map(r => [r.combination_key, r]));
  return { activities, emotions, recs, safety, pairs, triples,
    negative: new Set(emotions.groups.negative), positive: new Set(emotions.groups.positive) };
}

// Turn the vision model's guesses into pre-selected (unconfirmed) chips.
// Returns [] when the model said it could not tell, so the person starts from a blank form.
export function prefillChips(vlmOutput) {
  if (!vlmOutput || vlmOutput.insufficient_signal) return [];
  return (vlmOutput.feeling_guesses || [])
    .filter(g => g.feeling !== 'neutral')
    .slice(0, 3)
    .map(g => ({ id: g.feeling, level: 1, confirmed: false, basis: g.basis }));
}

function needsPerson(a) {
  return a.requirements.some(r => /another person|partner|friend|someone|responsive person|group|choir|organisation|animal|class/i.test(r));
}
function needsOutdoors(a) {
  return a.requirements.some(r => /outdoors|green space|woodland|water access|access to water|garden|somewhere to walk|stairs/i.test(r));
}

function safetyCheck(data, input) {
  const reasons = [];
  if (input.struggling) reasons.push('person chose "I\'m really struggling"');
  if (input.vlm && input.vlm.safety_concern) reasons.push('vision model flagged a safety concern in the person\'s words');
  if (input.freeText && SELF_HARM_CUES.some(re => re.test(input.freeText))) reasons.push('free text matched a self-harm cue');
  return reasons;
}

function confirmedFeelings(data, input) {
  const seen = new Map();
  for (const f of input.feelings || []) {
    if (f.confirmed === false) continue; // pre-filled but not tapped
    if (!data.recs[f.id] && f.id !== 'neutral') continue;
    const score = LEVEL_SCORE[f.level] ?? LEVEL_SCORE[2];
    if (!seen.has(f.id) || seen.get(f.id).score < score) seen.set(f.id, { id: f.id, level: f.level ?? 2, score });
  }
  return [...seen.values()].sort((a, b) => b.score - a.score);
}

// Candidate activity ids for the set of negative feelings, most specific evidence first.
function candidatesFor(data, negIds) {
  const out = { ids: [], avoid: new Set(), rule: null, evidenceBasis: null, source: null, note: null };
  const add = ids => { for (const id of ids) if (!out.ids.includes(id)) out.ids.push(id); };
  const top = negIds.slice(0, 4);
  // Try the most specific combination first: 4, then 3, then 2 emotions.
  for (let n = Math.min(top.length, 4); n >= 2 && !out.source; n--) {
    const key = [...top.slice(0, n)].sort().join('+');
    const row = n === 2 ? data.pairs.get(key) : data.triples.get(key);
    if (row) {
      add(splitIds(row.recommended_activity_ids));
      splitIds(row.avoid_activity_ids).forEach(id => out.avoid.add(id));
      splitIds(row.contraindicated_by_combo_evidence).forEach(id => out.avoid.add(id));
      out.rule = row.rules_applied || null;
      out.evidenceBasis = row.evidence_basis || null;
      out.source = n === 2 ? `combination_matrix.csv: ${key}` : `combination_triples.csv: ${key}`;
      out.note = row.note || null;
    }
  }
  // Fill from each emotion's own ranked list, strongest feeling first.
  for (const id of top) {
    const r = data.recs[id];
    if (!r) continue;
    add(r.recommended.map(x => x.activity_id));
    if (!out.source) { out.source = `recommendations.json: ${id}`; out.rule = r.single_emotion_rule?.rule_id || null; out.evidenceBasis = 'single_emotion'; }
  }
  // Avoid anything contraindicated for ANY confirmed negative feeling.
  for (const id of negIds) for (const a of data.recs[id]?.avoid || []) out.avoid.add(a.activity_id);
  return out;
}

function bestEvidenceFor(data, activityId, feelingIds) {
  for (const f of feelingIds) {
    const hit = data.recs[f]?.recommended.find(x => x.activity_id === activityId);
    if (hit) return { feeling: f, citation: hit.top_citation, doi_or_url: hit.top_citation_doi_or_url,
      verification: hit.top_citation_verification_status, evidence_score: hit.evidence_score };
  }
  return null;
}

function rank(data, ids, avoid, feelingIds, input, { highIntensity, limit }) {
  const prefs = input.preferences || {};
  const likes = new Set(prefs.likes || []), dislikes = new Set(prefs.dislikes || []);
  const ctx = { otherPersonAvailable: true, canGoOutside: true, ...(prefs.context || {}) };
  const helped = new Map((input.history || []).map(h => [h.activity_id, h.helped]));
  const never = new Set(data.safety.never_suggest_activity_ids || []);
  const feelings = new Set(feelingIds);

  const scored = [];
  ids.forEach((id, idx) => {
    const a = data.activities.get(id);
    if (!a || !a.suggestable || a.suggest_mode !== 'right_now') return;
    if (never.has(id) || avoid.has(id)) return;
    if ((a.contraindicated_for || []).some(c => c.kind === 'emotion' && feelings.has(c.id))) return;
    if (!ctx.otherPersonAvailable && needsPerson(a)) return;
    if (!ctx.canGoOutside && needsOutdoors(a)) return;
    let s = 1 - idx * 0.04;                       // evidence order from the dataset
    for (const t of a.preference_tags) { if (likes.has(t)) s += 0.15; if (dislikes.has(t)) s -= 0.5; }
    if (helped.get(id) === true) s += 0.3;        // "did that help?" re-ranking (rule R29)
    if (helped.get(id) === false) s -= 0.6;
    if (highIntensity && a.arousal_effect === 'calming' && a.effort === 'low') s += 0.3; // calm first when intense (R01)
    scored.push({ a, s, idx });
  });
  scored.sort((x, y) => y.s - x.s || x.idx - y.idx);

  // Keep variety: at most one activity per category among the picks.
  const picks = [], cats = new Set();
  for (const c of scored) { if (picks.length >= limit) break; if (cats.has(c.a.category)) continue; picks.push(c); cats.add(c.a.category); }
  for (const c of scored) { if (picks.length >= limit) break; if (!picks.includes(c)) picks.push(c); }

  return picks.map(({ a }) => {
    const ev = bestEvidenceFor(data, a.id, feelingIds);
    return {
      id: a.id, name: a.name, category: a.category, instruction: a.instruction,
      duration_min: a.typical_duration_min, effort: a.effort,
      why: ev ? `Evidence for ${ev.feeling}: ${ev.citation}` : 'Recommended by the combination rule for these feelings',
      doi_or_url: ev?.doi_or_url || null, verification: ev?.verification || null,
      cautions: a.cautions.slice(0, 2),
    };
  });
}

/**
 * input = {
 *   feelings: [{ id: 'stressed', level: 1|2|3, confirmed?: boolean }],  // the person's chips
 *   struggling?: boolean,      // explicit "I'm really struggling" option
 *   freeText?: string,         // the person's own words, if any
 *   vlm?: object,              // vision-model output (reflection.schema.json); only safety_concern is read
 *   preferences?: { likes: [tag], dislikes: [tag], context: { otherPersonAvailable, canGoOutside } },
 *   history?: [{ activity_id, helped: boolean }]
 * }
 */
export function decide(data, input = {}) {
  const safety = safetyCheck(data, input);
  if (safety.length) {
    return {
      mode: 'support_safety', suggestions: [], reasons: safety,
      headline: 'Thank you for telling me.',
      message: 'It sounds like things are really hard right now. You deserve support from a person: please reach out to someone you trust, or a local crisis line if you might not be safe.',
      notes: ['Show localised crisis resources here. Do not show the activity list (safety.json crisis_gate).'],
    };
  }

  const feelings = confirmedFeelings(data, input);
  if (!feelings.length) {
    return { mode: 'ask', suggestions: [], headline: 'How does this feel to you?',
      message: 'Tap the feelings that fit right now, or "not sure". The drawing is just a starting point.' };
  }

  const neg = feelings.filter(f => data.negative.has(f.id));
  const pos = feelings.filter(f => data.positive.has(f.id));
  const negLoad = neg.reduce((t, f) => t + f.score, 0);
  const posLoad = pos.reduce((t, f) => t + f.score, 0);
  const balance = { negative: +negLoad.toFixed(2), positive: +posLoad.toFixed(2) };

  if (!neg.length) {
    if (!pos.length) {
      return { mode: 'neutral', suggestions: [], balance, headline: 'Steady is good.',
        message: 'Nothing needs fixing. Come back any time you want to check in.' };
    }
    const ids = [];
    for (const f of pos) for (const r of data.recs[f.id].recommended) if (!ids.includes(r.activity_id)) ids.push(r.activity_id);
    return { mode: 'positive', balance, headline: 'Nice, it sounds like a good moment.',
      message: 'No need to do anything. If you like, here are ways to make the most of it.',
      suggestions: rank(data, ids, new Set(), pos.map(f => f.id), input, { highIntensity: false, limit: 2 }),
      source: `recommendations.json: ${pos.map(f => f.id).join(', ')}` };
  }

  const negIds = neg.map(f => f.id);
  const highIntensity = neg[0].score >= data.safety.thresholds.high_intensity_gte;
  const cand = candidatesFor(data, negIds);

  if (pos.length && posLoad >= negLoad) {
    // Mixed moment, mostly positive: keep the good part, offer one gentle option (rule R38).
    return { mode: 'mixed', balance, headline: 'A bit of both.',
      message: 'There\'s some good here as well as something weighing on you. No need to fix anything; here\'s one small option if you want it.',
      suggestions: rank(data, cand.ids, cand.avoid, [...negIds, ...pos.map(f => f.id)], input, { highIntensity: false, limit: 1 }),
      rule: cand.rule, evidence_basis: cand.evidenceBasis, source: cand.source };
  }

  return { mode: 'support', balance, high_intensity: highIntensity,
    headline: 'Thanks for checking in.',
    message: `You said you feel ${neg.map(f => `${LEVEL_LABEL[f.level] ?? ''} ${f.id}`.trim()).join(' and ')}. Here are a few things that may help. Pick one, or none.`,
    suggestions: rank(data, cand.ids, cand.avoid, negIds, input, { highIntensity, limit: 3 }),
    rule: cand.rule, evidence_basis: cand.evidenceBasis, source: cand.source,
    notes: cand.evidenceBasis && cand.evidenceBasis !== 'single_emotion' && /extrapolated/.test(cand.evidenceBasis)
      ? ['This combination rule is extrapolated from single-emotion evidence.'] : [] };
}
