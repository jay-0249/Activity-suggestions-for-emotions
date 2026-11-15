// Run with: node --test checkin/
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { loadData, decide, prefillChips } from './engine.mjs';

const data = loadData();

// The two example readings from the team's walkthrough, expressed as model output.
const scribbleOnly = {
  turn: 1,
  observations: ['dense overlapping loops in the centre', 'long sweeping arcs', 'a few sharp reversals'],
  reflection: 'Lots of looping movement, gathered into one cluster. Some people scribble like this to clear their head; others just enjoy the motion.',
  feeling_guesses: [], insufficient_signal: true,
  question: 'What was on your mind while you drew?', safety_concern: false,
};
const trueQuestionMark = {
  turn: 1,
  observations: ['the word "True" in the middle', 'a large question mark curving around it'],
  written_content: ['True', '?'],
  reflection: 'You wrote "True" and wrapped a big question mark around it. That might be a thought you\'re weighing up right now.',
  feeling_guesses: [{ feeling: 'anxious', basis: 'question mark around a single word may reflect uncertainty' }],
  insufficient_signal: false,
  question: 'Is there something you\'re trying to decide?', safety_concern: false,
};

test('a plain scribble does not pre-fill any feeling', () => {
  assert.deepEqual(prefillChips(scribbleOnly), []);
});

test('model guesses are pre-filled but never treated as feelings until confirmed', () => {
  const chips = prefillChips(trueQuestionMark);
  assert.equal(chips.length, 1);
  assert.equal(chips[0].confirmed, false);
  const r = decide(data, { feelings: chips, vlm: trueQuestionMark });
  assert.equal(r.mode, 'ask');
  assert.equal(r.suggestions.length, 0);
});

test('no confirmed feelings: ask, never suggest', () => {
  assert.equal(decide(data, {}).mode, 'ask');
});

test('only positive feelings: optional savouring ideas, at most two', () => {
  const r = decide(data, { feelings: [{ id: 'content', level: 2 }] });
  assert.equal(r.mode, 'positive');
  assert.ok(r.suggestions.length > 0 && r.suggestions.length <= 2);
});

test('neutral only: no suggestions', () => {
  const r = decide(data, { feelings: [{ id: 'neutral', level: 2 }] });
  assert.equal(r.mode, 'neutral');
  assert.equal(r.suggestions.length, 0);
});

test('mixed but mostly positive: one gentle option', () => {
  const r = decide(data, { feelings: [{ id: 'content', level: 3 }, { id: 'tired', level: 1 }] });
  assert.equal(r.mode, 'mixed');
  assert.equal(r.suggestions.length, 1);
});

test('stressed + tired uses the pair rule and returns three varied options', () => {
  const r = decide(data, { feelings: [{ id: 'stressed', level: 2 }, { id: 'tired', level: 2 }] });
  assert.equal(r.mode, 'support');
  assert.match(r.source, /combination_matrix\.csv: stressed\+tired/);
  assert.equal(r.suggestions.length, 3);
  assert.equal(new Set(r.suggestions.map(s => s.category)).size, 3);
});

test('anger never gets venting or vigorous exercise', () => {
  const r = decide(data, { feelings: [{ id: 'angry', level: 3 }, { id: 'stressed', level: 2 }] });
  const ids = r.suggestions.map(s => s.id);
  for (const bad of ['venting', 'vigorous_exercise', 'running_jogging', 'hiit']) assert.ok(!ids.includes(bad), bad);
});

test('three negatives use the triple table', () => {
  const r = decide(data, { feelings: [{ id: 'sad', level: 2 }, { id: 'anxious', level: 2 }, { id: 'lonely', level: 2 }] });
  assert.match(r.source, /combination_triples\.csv: anxious\+lonely\+sad/);
});

test('no other person available removes activities that need one', () => {
  const r = decide(data, { feelings: [{ id: 'lonely', level: 2 }], preferences: { context: { otherPersonAvailable: false } } });
  for (const s of r.suggestions) assert.ok(!['call_friend', 'weak_tie_chat', 'affectionate_touch'].includes(s.id), s.id);
});

test('an activity that did not help last time drops down', () => {
  const first = decide(data, { feelings: [{ id: 'stressed', level: 2 }] }).suggestions[0].id;
  const again = decide(data, { feelings: [{ id: 'stressed', level: 2 }], history: [{ activity_id: first, helped: false }] });
  assert.notEqual(again.suggestions[0].id, first);
});

test('safety words override everything', () => {
  const r = decide(data, { feelings: [{ id: 'sad', level: 3 }], freeText: "honestly I don't want to be here anymore" });
  assert.equal(r.mode, 'support_safety');
  assert.equal(r.suggestions.length, 0);
});

test('every suggestion is a right-now activity and never on the never-suggest list', () => {
  const never = new Set(data.safety.never_suggest_activity_ids);
  for (const e of ['stressed', 'anxious', 'angry', 'restless', 'sad', 'lonely', 'tired', 'bored']) {
    for (const level of [1, 3]) {
      for (const s of decide(data, { feelings: [{ id: e, level }] }).suggestions) {
        assert.ok(!never.has(s.id), `${e}: ${s.id}`);
        assert.equal(data.activities.get(s.id).suggest_mode, 'right_now');
      }
    }
  }
});
