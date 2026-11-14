#!/usr/bin/env python3
"""Build the emotion -> activity evidence dataset from the research notes.

Inputs (never modified):
  research_notes/Emotion to activity evidence map/*.md   ("## Dataset rows", taxonomy and rule tables)
  data/verification/*.csv                                (per-citation PubMed verification)
  data/curation/*                                        (hand-curated mapping tables, see schema.md)

Outputs (all under data/): emotions.json, activities.json, evidence_links.csv/.json,
recommendations.json, combination_rules.json, combination_matrix.csv, safety.json,
schema.md, sources.csv.

Run:  python3 scripts/build_dataset.py
Only the Python standard library is used. No number, DOI or PMID is generated here:
every such value is copied from the notes tables or the verification CSVs.
"""
import csv
import json
import re
import sys

sys.dont_write_bytecode = True
import unicodedata
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "research_notes" / "Emotion to activity evidence map"
DATA = ROOT / "data"
CUR = DATA / "curation"
VER = DATA / "verification"

ACTIVITY_FILES = [
    ("creative_arts_activities.md", "CRE"),
    ("physical_nature_activities.md", "PHY"),
    ("mind_body_cognitive_techniques.md", "MBC"),
    ("social_play_and_low_arousal_states.md", "SOC"),
]
MODELS_FILE = "emotion_models_and_matching_logic.md"
HANDWRITING_FILE = "handwriting_drawing_emotion_validity.md"

STATUS_RANK = {  # higher = more confidence; used to pick the most conservative status
    "verified_fulltext": 5, "verified_abstract": 4, "corrected": 4,
    "citation_exists_number_not_confirmed": 2, "not_in_pubmed": 1, "not_found": 0, "unverified": 0,
}
VERIFIED_OK = {"verified_fulltext", "verified_abstract", "corrected"}


# ----------------------------------------------------------------------------- helpers
def read(path):
    return Path(path).read_text(encoding="utf-8")


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: _cell(r.get(k, "")) for k in fields})


def _cell(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ";".join(str(x) for x in v)
    return v


def norm_text(s):
    s = s.replace("æ", "ae").replace("Æ", "Ae").replace("ø", "o").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def parse_md_table(text, heading):
    """Return list of dicts for the first markdown table after `heading`."""
    lines = text.split("\n")
    start = lines.index(heading)
    header, rows = None, []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            if header and rows:
                break
            continue
        if re.match(r"^\|\s*-{3}", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if header is None:
            header = [re.sub(r"\s*\(.*$", "", c).strip() if c.startswith(("citation", "valence", "arousal", "source", "condition")) else c
                      for c in cells]
            continue
        if len(cells) != len(header):
            raise SystemExit(f"Table under {heading!r}: expected {len(header)} cells, got {len(cells)}: {line[:90]}")
        rows.append(OrderedDict(zip(header, cells)))
    if not rows:
        raise SystemExit(f"No table rows under {heading!r}")
    return rows


def split_outside_parens(s, sep=";"):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch == sep and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def cite_key(citation):
    """(first-author surname string, year) from a free-text citation."""
    c = norm_text(citation)
    m = re.search(r"\b(19|20)\d\d\b", c)
    year = m.group(0) if m else ""
    head = re.split(r",| & | et al|\(| \d{4}", c, maxsplit=1)[0].strip()
    return head, year


def norm_doi(s):
    m = re.search(r"10\.\d{4,9}/[^\s;,)\]]+", s or "")
    if not m:
        return ""
    return m.group(0).lower().rstrip(".").replace("//", "/")


def all_dois(s):
    return [d.lower().rstrip(".").replace("//", "/") for d in re.findall(r"10\.\d{4,9}/[^\s;,)\]]+", s or "")]


# ----------------------------------------------------------------------------- verification index
def load_verification():
    entries = []
    for path in sorted(VER.glob("*.csv")):
        with open(path, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                surname, year = cite_key(row["citation"])
                entries.append({
                    "file": path.stem, "citation": row["citation"].strip(), "pmid": row["pmid"].strip(),
                    "doi_raw": row["doi"].strip(), "doi": norm_doi(row["doi"]), "status": row["status"].strip(),
                    "what_was_checked": row["what_was_checked"].strip(), "corrections": row["corrections"].strip(),
                    "surname": surname, "year": year,
                })
    for e in entries:
        if e["status"] not in STATUS_RANK:
            raise SystemExit(f"Unknown verification status {e['status']!r} in {e['file']}")
    return entries


def match_citation(part, urls, stem, ver):
    """Find the verification entry for one citation string. Returns (entry|None, how)."""
    surname, year = cite_key(part)
    dois = set(all_dois(urls) + all_dois(part))
    pmids = set(re.findall(r"PMID (\d{6,9})", part)) | set(re.findall(r"pubmed[^\s;]*/(\d{6,9})", urls))
    pools = [[e for e in ver if e["file"] == stem], [e for e in ver if e["file"] != stem]]
    for pool, where in zip(pools, ("same_file", "other_file")):
        if surname and year:
            cands = [e for e in pool if e["year"] == year and (e["surname"] == surname or
                     e["surname"].split(" ")[0] == surname.split(" ")[0] and len(surname.split(" ")[0]) > 3)]
            if len(cands) == 1:
                return cands[0], f"author_year:{where}"
            if len(cands) > 1:
                for e in cands:
                    if (e["doi"] and e["doi"] in dois) or (e["pmid"] and e["pmid"] in pmids):
                        return e, f"author_year+id:{where}"
                exact = [e for e in cands if e["surname"] == surname]
                if len(exact) == 1:
                    return exact[0], f"author_year_exact:{where}"
        for e in pool:
            if (e["doi"] and e["doi"] in dois and (not year or not e["year"] or e["year"] == year or not surname)) \
               or (e["pmid"] and e["pmid"] in pmids):
                if not surname or not e["surname"] or e["surname"].split(" ")[0] == surname.split(" ")[0] or not year:
                    return e, f"id:{where}"
        if where == "same_file" and not (surname and year):
            # odd citations without author/year: fall back to the longest shared word run
            p = norm_text(part)[:40]
            for e in pool:
                if norm_text(e["citation"])[:25] == p[:25]:
                    return e, "prefix:same_file"
    return None, "unmatched"


# ----------------------------------------------------------------------------- classification heuristics
def level_class(level):
    s = level.lower()
    if "indirect" in s or s.startswith("none"):
        return "indirect"
    if "meta-analysis" in s:
        return "meta_analysis"
    if "systematic review" in s:
        return "systematic_review"
    if "experiment" in s:
        return "experiment"
    if "rct" in s:
        return "rct"
    if "observational" in s:
        return "observational"
    raise SystemExit(f"Unclassified evidence_level {level!r}")


def strength_class(strength):
    s = strength.lower()
    if "preliminary" in s:
        return "preliminary"
    if s.startswith("strong"):
        return "strong"
    if s.startswith("moderate"):
        return "moderate"
    raise SystemExit(f"Unclassified evidence_strength {strength!r}")


HARM_PAT = re.compile(r"\(worse\)|no effect or increases|may impair|decreases pleasure|decreases affective well-being|"
                      r"dampening|aversive|may increase", re.I)
UNCLEAR_PAT = re.compile(r"^mixed|unclear|^unknown|theoretical|plausible|inconclusive", re.I)
NULL_PAT = re.compile(r"^no (effect|benefit|significant|immediate|average|reduction)", re.I)


def direction_class(direction, activity):
    if re.search(r"do NOT suggest|to AVOID", activity):
        return "harm"
    if HARM_PAT.search(direction):
        return "harm"
    if NULL_PAT.search(direction):
        return "null"
    if UNCLEAR_PAT.search(direction):
        return "mixed_or_unclear"
    return "benefit"


SINGLE_PAT = re.compile(r"single|one session|one-off|acute|one \d+-min audio|one conversation|one commute|one gratitude|"
                        r"one purchase|one self-selected|one rehearsal|right after", re.I)
MULTI_PAT = re.compile(r"programme|program|multi-|weeks?\b|months?\b|chronic|/day|per day|daily|days/week|weekly|"
                       r"over \d+ days|habitual|trait|sustained|hours/day|/week|\byear|×|\d sessions|residential|"
                       r"\d-day|days\b", re.I)
SHORT_PAT = re.compile(r"\bmin\b|minutes?\b|seconds|brief|short|momentary|during|\bnap\b|\b1 h\b", re.I)


def single_session(dose):
    if SINGLE_PAT.search(dose):
        return "true"
    if MULTI_PAT.search(dose):
        return "false"
    if SHORT_PAT.search(dose):
        return "true"
    return "unknown"


STD_METRIC = re.compile(r"(?<![A-Za-z])(Hedges'? ?g|Hedges'? ?d|d\+|SMD|ES|[dgrΔδ])(?:\s*[=≈]\s*|\s+)(-?\d*\.\d+)")
METRIC_NAME = {"d": "d", "d+": "d_plus", "g": "hedges_g", "SMD": "smd", "ES": "es_unspecified", "r": "r",
               "Δ": "delta", "δ": "delta", "hedges g": "hedges_g", "hedges' g": "hedges_g", "hedgesg": "hedges_g",
               "hedges' d": "hedges_d", "hedges d": "hedges_d"}


def effect_value(text):
    t = text.replace("−", "-").replace("–", "-")
    found = STD_METRIC.findall(t)
    if len(found) == 1:
        m, v = found[0]
        name = METRIC_NAME.get(m) or METRIC_NAME.get(m.lower()) or m
        return v if not v.startswith((".", "-.")) else v.replace(".", "0.", 1), name
    if len(found) > 1:
        return "", "multiple_values_see_text"
    if re.search(r"\badjOR\b|\bOR\b", t):
        return "", "odds_ratio"
    if re.search(r"\bRR\b", t):
        return "", "risk_ratio"
    if "η²" in t or "eta2" in t:
        return "", "eta_squared"
    if re.search(r"\bMD\b", t):
        return "", "mean_difference"
    if re.match(r"-?\d+(\.\d+)?%", t.strip()):
        return "", "percent_change"
    if re.search(r"\d", t) and re.search(r"M = |mean|%|points|F\(|F = |t\(|-\d?\.\d", t):
        return "", "other_statistic_see_text"
    return "", "not_reported"


UNCONF_PAT = re.compile(r"not confirmed|unverified|unconfirmed|not re-verified|not re-confirmed|not checkable|"
                        r"not in pubmed|not indexed in pubmed|not verifiable|\[U\]|not independently verified|"
                        r"not found in pubmed", re.I)


# ----------------------------------------------------------------------------- load curation
def load_curation():
    cur = {}
    lm = {}
    with open(CUR / "emotion_label_map.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            maps = []
            for item in r["mappings"].split(";"):
                eid, mtype = item.split(":")
                assert mtype in ("direct", "proxy"), item
                maps.append((eid, mtype))
            lm[r["raw_label"]] = {"mappings": maps, "constructs": [c for c in r["constructs"].split(";") if c], "note": r["note"]}
    cur["label_map"] = lm
    am = {}
    with open(CUR / "activity_map.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            am[r["raw_activity"]] = {"ids": r["activity_ids"].split(";"), "category_level": r["category_level"] == "true", "note": r["note"]}
    cur["activity_map"] = am
    acts = OrderedDict()
    with open(CUR / "activities_curated.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="|", quoting=csv.QUOTE_NONE):
            contra = []
            for item in [x for x in r["contraindicated_for"].split(";;") if x]:
                target, reason = item.split("=", 1)
                kind = "emotion"
                if ":" in target:
                    kind, target = target.split(":", 1)
                contra.append({"kind": kind, "id": target, "reason": reason})
            acts[r["id"]] = {
                "id": r["id"], "name": r["name"], "category": r["category"], "suggest_mode": r["suggest_mode"],
                "arousal_effect": r["arousal_effect"], "effort": r["effort"],
                "typical_duration_min": int(r["typical_duration_min"]),
                "min_effective_dose": r["min_effective_dose"] or None,
                "requirements": [x.strip() for x in r["requirements"].split(";") if x.strip()],
                "rule_classes": [x for x in r["rule_classes"].split(";") if x],
                "instruction": r["instruction"], "contraindicated_for": contra,
            }
    cur["activities"] = acts
    cur["emotions"] = json.loads(read(CUR / "emotions_curated.json"))
    cur["rules"] = json.loads(read(CUR / "rules_curated.json"))
    cur["weights"] = json.loads(read(CUR / "score_weights.json"))
    cur["safety"] = json.loads(read(CUR / "safety_curated.json"))
    ov = defaultdict(list)
    with open(CUR / "link_overrides.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            ov[(r["source"], int(r["row"]))].append(r)
    cur["overrides"] = ov
    cm = {}
    with open(CUR / "citation_match_overrides.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            cm[(r["source"], int(r["row"]), r["citation_startswith"])] = r["verification_citation_startswith"]
    cur["citation_overrides"] = cm
    return cur


# ----------------------------------------------------------------------------- evidence links
def build_links(cur, ver):
    links, row_records, match_log = [], [], []
    for fname, abbr in ACTIVITY_FILES:
        stem = fname[:-3]
        rows = parse_md_table(read(NOTES / fname), "## Dataset rows")
        prev = {}
        for n, row in enumerate(rows, 1):
            raw = dict(row)
            resolved = dict(row)
            for col in ("dose_tested", "population", "cautions"):
                if row[col].strip().lower() in ("as above", "as above."):
                    resolved[col] = prev.get(col, row[col])
            prev = {c: resolved[c] for c in ("dose_tested", "population", "cautions")}
            if not row["citation"].strip():
                raise SystemExit(f"{fname} row {n}: evidence row without a citation")
            # citations -> verification
            parts = split_outside_parens(row["citation"])
            matched = []
            for p in parts:
                e, how = match_citation(p, row["doi_or_url"], stem, ver)
                for (osrc, orow, ostart), vstart in cur["citation_overrides"].items():
                    if (osrc, orow) == (abbr, n) and p.startswith(ostart):
                        hits = [v for v in ver if v["file"] == stem and v["citation"].startswith(vstart)]
                        if len(hits) != 1:
                            raise SystemExit(f"citation_match_overrides.csv: {abbr} {n} matches {len(hits)} verification records")
                        e, how = hits[0], "curated_override"
                matched.append((p, e, how))
                match_log.append((abbr, n, p[:70], e["citation"][:60] if e else "", e["status"] if e else "unverified", how))
            prim = matched[0][1]
            status = prim["status"] if prim else "unverified"
            pmid = prim["pmid"] if prim else ""
            if not pmid:
                m = re.search(r"PMID (\d{6,9})", parts[0])
                pmid = m.group(1) if m else ""
            all_status = [f"{cite_key(p)[0] or p[:30]} {cite_key(p)[1]}={(e['status'] if e else 'unverified')}" for p, e, _ in matched]
            unconf_text = bool(UNCONF_PAT.search(" ".join([row["effect_size"], row["dose_tested"], row["population"],
                                                           row["cautions"], row["citation"], row["doi_or_url"]])))
            ev, metric = effect_value(row["effect_size"])
            base = {
                "source_notes_file": fname, "source_row": n, "source_row_id": f"{abbr}{n:03d}",
                "original_activity": row["activity"], "original_target_emotion": row["target_emotion"],
                "direction": row["direction_of_effect"], "direction_class": direction_class(row["direction_of_effect"], row["activity"]),
                "effect_size": row["effect_size"], "effect_size_value": ev, "effect_metric": metric,
                "evidence_level": row["evidence_level"], "evidence_level_class": level_class(row["evidence_level"]),
                "evidence_strength": row["evidence_strength"], "evidence_strength_class": strength_class(row["evidence_strength"]),
                "low_applicability": "low applicability" in row["evidence_strength"].lower(),
                "dose_tested": resolved["dose_tested"], "population": resolved["population"],
                "citation": row["citation"], "doi_or_url": row["doi_or_url"],
                "doi": (prim["doi_raw"] if prim else ""), "pmid": pmid,
                "verification_status": status, "verification_status_all_citations": all_status,
                "row_has_unconfirmed_text": unconf_text,
                "single_session_evidence": single_session(resolved["dose_tested"]),
                "cautions": "" if resolved["cautions"] in ("—", "-") else resolved["cautions"],
                "preference_tags": [t.strip().lower() for t in row["preference_tags"].split(",") if t.strip()],
                "_cites": [(p, e) for p, e, _ in matched],
            }
            if row["activity"] not in cur["activity_map"]:
                raise SystemExit(f"Unmapped activity {row['activity']!r} ({fname} row {n}); add it to data/curation/activity_map.csv")
            if row["target_emotion"] not in cur["label_map"]:
                raise SystemExit(f"Unmapped target_emotion {row['target_emotion']!r} ({fname} row {n}); add it to data/curation/emotion_label_map.csv")
            amap, lmap = cur["activity_map"][row["activity"]], cur["label_map"][row["target_emotion"]]
            row_ov = cur["overrides"].get((abbr, n), [])
            for o in row_ov:
                if not row["activity"].startswith(o["activity_startswith"]):
                    raise SystemExit(f"link_overrides.csv: {abbr} row {n} no longer starts with {o['activity_startswith']!r}")
            row_records.append({**base, "activity_ids": amap["ids"], "emotion_ids": [e for e, _ in lmap["mappings"]]})
            for aid in amap["ids"]:
                for eid, mtype in lmap["mappings"]:
                    link = dict(base)
                    link.update({"link_id": f"{abbr}{n:03d}_{aid}_{eid}", "activity_id": aid, "emotion_id": eid,
                                 "emotion_mapping": mtype, "constructs": lmap["constructs"],
                                 "category_level_evidence": amap["category_level"]})
                    for o in row_ov:
                        if o["emotion_id"] in ("", eid):
                            val = o["value"]
                            link[o["field"]] = val
                            link.setdefault("overrides_applied", []).append(f"{o['field']}={val} ({o['reason']})")
                    flags = []
                    if link["direction_class"] != "benefit":
                        flags.append("direction_" + link["direction_class"])
                    if link["verification_status"] not in VERIFIED_OK:
                        flags.append("citation_" + link["verification_status"])
                    if link["row_has_unconfirmed_text"]:
                        flags.append("row_contains_unconfirmed_detail")
                    if link["evidence_strength_class"] == "preliminary":
                        flags.append("preliminary")
                    if link["evidence_level_class"] in ("indirect", "observational"):
                        flags.append("level_" + link["evidence_level_class"])
                    if link["low_applicability"]:
                        flags.append("low_applicability")
                    if link["emotion_mapping"] == "proxy":
                        flags.append("proxy_emotion_mapping")
                    if link["category_level_evidence"]:
                        flags.append("category_level_evidence")
                    if link["single_session_evidence"] == "false":
                        flags.append("not_single_session")
                    link["flags"] = flags
                    link["overrides_applied"] = link.get("overrides_applied", [])
                    links.append(link)
    return links, row_records, match_log


def link_score(link, W, mapping=None):
    m = mapping or link["emotion_mapping"]
    s = W["evidence_level"][link["evidence_level_class"]] * W["evidence_strength"][link["evidence_strength_class"]]
    if link["low_applicability"]:
        s *= W["low_applicability_multiplier"]
    s *= W["verification_status"][link["verification_status"]]
    if link["row_has_unconfirmed_text"] and link["verification_status"] in VERIFIED_OK:
        s *= W["row_unconfirmed_text_multiplier"]
    s *= W["single_session_evidence"][link["single_session_evidence"]]
    s *= W["mapping_type"][m]
    if link["category_level_evidence"]:
        s *= W["category_level_multiplier"]
    return s


# ----------------------------------------------------------------------------- emotions / activities
def build_emotions(cur, links):
    tax = parse_md_table(read(NOTES / MODELS_FILE), "## Proposed emotion taxonomy")
    ce = cur["emotions"]
    raw_by_emotion = defaultdict(list)
    for raw, m in cur["label_map"].items():
        for eid, mtype in m["mappings"]:
            raw_by_emotion[eid].append({"label": raw, "mapping": mtype})
    emotions = []
    for row in tax:
        eid = row["emotion_id"]
        c = ce["emotions"][eid]
        emotions.append({
            "id": eid, "label": row["label"], "valence": c["valence"], "arousal": c["arousal"],
            **({"arousal_norm": c["arousal_norm"]} if "arousal_norm" in c else {}),
            "valence_text": row["valence"].replace("−", "-"), "arousal_text": row["arousal"].replace("−", "-"),
            **({"coordinate_note": c["coordinate_note"]} if "coordinate_note" in c else {}),
            "tension": 1 if c["tension_member"] else 0,
            "tension_note": "member of the max() in the derived tension score" if c["tension_member"] else "not part of the derived tension score",
            "energy": {"plus energetic": 1.0, "minus tired": -1.0, "minus 0.5 x bored": -0.5}.get(c["energy_term"]),
            "energy_note": c["energy_term"] or "not part of the derived energy score",
            "polarity": c["polarity"], "quadrant": row["quadrant"],
            "closest_validated_construct": row["closest validated construct"], "source": row["source"],
            "synonyms": c["synonyms"],
            "notes_target_labels": sorted(raw_by_emotion.get(eid, []), key=lambda x: x["label"]),
        })
    assert {e["id"] for e in emotions} == set(ce["emotions"]), "taxonomy table and emotions_curated.json disagree"
    aggs = []
    for a in ce["aggregate_targets"]:
        aggs.append({**a, "kind": "aggregate", "llm_class": False,
                     "notes_target_labels": sorted(raw_by_emotion.get(a["id"], []), key=lambda x: x["label"])})
    syn = {}
    for e in emotions:
        for s in [e["id"]] + e["synonyms"]:
            key = s.lower()
            if key in syn and syn[key] != e["id"]:
                raise SystemExit(f"Synonym {s!r} maps to two emotions")
            syn[key] = e["id"]
    return {
        "meta": {
            "source": f"research_notes/Emotion to activity evidence map/{MODELS_FILE} (## Proposed emotion taxonomy)",
            "coordinate_formula": "valence = (V - 5) / 4; arousal = clip((A - 4.21) / 2.70, -1, 1) from Warriner et al. 2013 word norms (1-9 scales)",
            "caveats": ["No peer-reviewed study validates this exact 12-class set, nor vision-LLM output against DASS/POMS/PANAS.",
                        "Coordinates are ratings of words, not of felt states.",
                        "Synonym lists are a design aid for mapping free-text labels; they are not validated."],
        },
        "derived_scores": ce["derived_scores"], "groups": ce["groups"],
        "emotions": emotions, "aggregate_targets": aggs, "synonym_index": dict(sorted(syn.items())),
    }


def build_activities(cur, links):
    by_act = defaultdict(list)
    for l in links:
        by_act[l["activity_id"]].append(l)
    out = []
    for aid, a in cur["activities"].items():
        ls = by_act.get(aid, [])
        if not ls:
            raise SystemExit(f"Curated activity {aid} has no evidence rows")
        tags = sorted({t for l in ls for t in l["preference_tags"]})
        if a["effort"] == "low":
            tags = [t for t in tags if t != "high-energy"]
        if a["effort"] == "high":
            tags = [t for t in tags if t != "low-effort"]
        cautions = []
        for l in ls:
            if l["cautions"] and l["cautions"] not in cautions:
                cautions.append(l["cautions"])
        benefit = sorted({l["emotion_id"] for l in ls if l["direction_class"] == "benefit"})
        nonben = sorted({l["emotion_id"] for l in ls if l["direction_class"] in ("harm", "null")})
        best = max(STATUS_RANK[l["verification_status"]] for l in ls)
        out.append({
            "id": aid, "name": a["name"], "category": a["category"],
            "suggest_mode": a["suggest_mode"], "suggestable": a["suggest_mode"] in ("right_now", "plan_to"),
            "instruction": a["instruction"], "typical_duration_min": a["typical_duration_min"],
            "min_effective_dose": a["min_effective_dose"], "arousal_effect": a["arousal_effect"], "effort": a["effort"],
            "preference_tags": tags, "requirements": a["requirements"], "cautions": cautions,
            "contraindicated_for": a["contraindicated_for"], "rule_classes": a["rule_classes"],
            "evidence_summary": {
                "n_evidence_links": len(ls), "n_source_rows": len({l["source_row_id"] for l in ls}),
                "emotions_with_benefit_evidence": benefit, "emotions_with_null_or_harm_evidence": nonben,
                "best_verification_status": sorted({l["verification_status"] for l in ls if STATUS_RANK[l["verification_status"]] == best})[0],
                "any_single_session_evidence": any(l["single_session_evidence"] == "true" and l["direction_class"] == "benefit" for l in ls),
            },
            "source_activity_labels": sorted({l["original_activity"] for l in ls}),
            "source_notes_files": sorted({l["source_notes_file"] for l in ls}),
        })
    return out


# ----------------------------------------------------------------------------- recommendations
def contra_ids(act, kind="emotion"):
    return {c["id"] for c in act["contraindicated_for"] if c["kind"] == kind}


def build_recommendations(cur, links, activities, emotions, rules_out):
    W = cur["weights"]
    acts = {a["id"]: a for a in activities}
    negatives = set(cur["emotions"]["aggregate_targets"][0]["applies_to"])
    single_rule = {r["single_emotion"]: r for r in rules_out if r.get("single_emotion")}
    recs, score_map = OrderedDict(), defaultdict(dict)
    for emo in emotions["emotions"]:
        eid = emo["id"]
        cand = defaultdict(list)
        avoid, nulls = {}, {}
        for l in links:
            if l["emotion_id"] == eid:
                mapping = l["emotion_mapping"]
            elif l["emotion_id"] == "negative_affect_general" and eid in negatives:
                mapping = "aggregate"
            else:
                continue
            a = acts[l["activity_id"]]
            if l["direction_class"] in ("harm", "null") and (mapping != "aggregate" or l["direction_class"] == "harm"):
                (avoid if l["direction_class"] == "harm" else nulls).setdefault(l["activity_id"], []).append(
                    {"reason": f"{l['direction_class']}: {l['direction']} ({l['original_target_emotion']})",
                     "citation": l["citation"], "doi_or_url": l["doi_or_url"], "link_id": l["link_id"],
                     "verification_status": l["verification_status"]})
            if l["direction_class"] == "benefit":
                s = link_score(l, W, mapping)
                if mapping == "aggregate" and l["emotion_mapping"] == "proxy":
                    s *= W["mapping_type"]["proxy"]
                cand[l["activity_id"]].append((s, mapping, l))
        for aid, a in acts.items():
            for c in a["contraindicated_for"]:
                if c["kind"] == "emotion" and c["id"] == eid:
                    avoid.setdefault(aid, []).append({"reason": "contraindicated: " + c["reason"], "citation": "", "doi_or_url": "",
                                                      "link_id": "", "verification_status": ""})
        ranked = []
        for aid, items in cand.items():
            a = acts[aid]
            if not a["suggestable"] or eid in contra_ids(a):
                continue
            direct_harm = [l for l in links if l["activity_id"] == aid and l["emotion_id"] == eid and l["direction_class"] == "harm"]
            if direct_harm:
                continue
            items.sort(key=lambda x: (-x[0], x[2]["link_id"]))
            best_s, best_map, best = items[0]
            ckey = lambda l: l["pmid"] or norm_doi(l["doi"]) or norm_doi(l["doi_or_url"]) or l["citation"]
            seen = {ckey(best)}
            extra = 0.0
            for s, _, l in items[1:]:
                if ckey(l) not in seen:
                    seen.add(ckey(l))
                    extra += s
            score = min(1.0, best_s + W["corroboration_bonus_per_extra_link"] * extra)
            if a["suggest_mode"] == "plan_to":
                score *= W["plan_to_multiplier"]
            flags = list(best["flags"])
            if a["suggest_mode"] == "plan_to":
                flags.append("plan_ahead_not_right_now")
            if best_map == "aggregate":
                flags.append("general_negative_affect_evidence_not_emotion_specific")
            if aid in nulls:
                flags.append("also_has_null_evidence_for_this_emotion")
            es = f"; effect size {best['effect_size']}" if best["effect_metric"] != "not_reported" else ""
            why = (f"{a['name']}: {best['evidence_level']} evidence rated {best['evidence_strength']} in the notes that it "
                   f"{best['direction']} for '{best['original_target_emotion']}'{es}. Dose tested: {best['dose_tested']}. "
                   f"Citation check: {best['verification_status']}"
                   + ("; mapped to this emotion as a proxy" if best_map == "proxy" else "")
                   + ("; evidence is for negative emotion in general, not this emotion specifically" if best_map == "aggregate" else "")
                   + ".")
            ranked.append({
                "activity_id": aid, "evidence_score": round(score, 3),
                "n_supporting_links": len(items), "n_distinct_citations": len(seen),
                "best_link_id": best["link_id"], "best_link_mapping": best_map,
                "top_citation": best["citation"], "top_citation_doi_or_url": best["doi_or_url"],
                "top_citation_pmid": best["pmid"], "top_citation_verification_status": best["verification_status"],
                "single_session_evidence": best["single_session_evidence"],
                "suggest_mode": a["suggest_mode"], "effort": a["effort"], "arousal_effect": a["arousal_effect"],
                "in_single_emotion_rule": bool(single_rule.get(eid) and aid in single_rule[eid]["recommend_activity_ids"]),
                "flags": flags, "why": why,
            })
        ranked.sort(key=lambda r: (-r["evidence_score"], r["activity_id"]))
        for i, r in enumerate(ranked, 1):
            r["rank"] = i
            score_map[eid][r["activity_id"]] = r["evidence_score"]
        direct_links = [l for l in links if l["emotion_id"] == eid]
        dv = {l["activity_id"] for l in direct_links if l["direction_class"] == "benefit" and l["emotion_mapping"] == "direct"
              and l["verification_status"] in VERIFIED_OK and acts[l["activity_id"]]["suggestable"]}
        dvs = {l["activity_id"] for l in direct_links if l["direction_class"] == "benefit" and l["emotion_mapping"] == "direct"
               and l["verification_status"] in VERIFIED_OK and l["single_session_evidence"] == "true"
               and acts[l["activity_id"]]["suggest_mode"] == "right_now"}
        sr = single_rule.get(eid)
        fb = None
        if sr:
            fb = {"rule_id": sr["rule_id"], "evidence_basis": sr["evidence_basis"],
                  "activity_ids_without_direct_evidence_row": [a for a in sr["recommend_activity_ids"] if a not in score_map[eid]],
                  "note": "Activities allowed by the emotion's own matching rule but with no benefit row for this emotion; treat as extrapolated."}
        elif eid == "restless":
            fb = {"rule_id": None, "evidence_basis": "extrapolated",
                  "activity_ids_without_direct_evidence_row": resolve_classes(cur["rules"]["restless_fallback"]["recommend_classes"], acts,
                                                                              set(cur["rules"]["restless_fallback"]["avoid_activity_ids"]), eid),
                  "note": cur["rules"]["restless_fallback"]["note"]}
        recs[eid] = {
            "emotion_id": eid, "label": emo["label"],
            "evidence_depth": {
                "n_evidence_links_direct_or_proxy": len(direct_links),
                "n_links_direct_mapping": sum(1 for l in direct_links if l["emotion_mapping"] == "direct"),
                "n_benefit_links": sum(1 for l in direct_links if l["direction_class"] == "benefit"),
                "n_activities_ranked": len(ranked),
                "n_activities_with_direct_verified_benefit": len(dv),
                "n_right_now_activities_with_direct_verified_single_session_benefit": len(dvs),
                "thin_evidence": len(dv) < W["thin_evidence"]["min_activities_with_direct_verified_benefit"],
                "thin_for_right_now_use": len(dvs) < W["thin_evidence"]["min_right_now_activities_with_direct_verified_single_session_benefit"],
            },
            "single_emotion_rule": sr["rule_id"] if sr else None,
            "recommended": ranked,
            "avoid": [{"activity_id": k, "reasons": v} for k, v in sorted(avoid.items())],
            "no_benefit_found": [{"activity_id": k, "reasons": v} for k, v in sorted(nulls.items()) if k not in cand and k not in avoid],
            "rule_fallback": fb,
        }
    return recs, score_map


# ----------------------------------------------------------------------------- rules
def resolve_classes(classes, acts, avoid, *emotions, avoid_classes=(), avoid_effort=()):
    out = []
    for mode in ("right_now", "plan_to"):
        for cls in classes:
            for aid, a in acts.items():
                if a["suggest_mode"] != mode or cls not in a["rule_classes"] or aid in out or aid in avoid:
                    continue
                if a["effort"] in avoid_effort or set(a["rule_classes"]) & set(avoid_classes) and not (set(a["rule_classes"]) - set(avoid_classes)) & set(classes):
                    continue
                if any(e in contra_ids(a) for e in emotions):
                    continue
                out.append(aid)
    return out


def rule_emotions(cond):
    out = []
    for key in ("all", "any"):
        for c in cond.get(key, []):
            if "emotion" in c:
                out.append(c["emotion"])
    return out


def build_rules(cur, activities, ver):
    acts = {a["id"]: a for a in activities}
    table = parse_md_table(read(NOTES / MODELS_FILE), "## Matching rules")
    cr = cur["rules"]
    out = []
    assert [r["rule_id"] for r in table] == [f"R{i:02d}" for i in range(1, 31)], "expected R01..R30 in the notes"
    for row in table:
        rid = row["rule_id"]
        c = cr["rules"][rid]
        basis_text = row["directly_tested_or_extrapolated"]
        b = basis_text.lower()
        basis = "extrapolated" if b.startswith("extrapolated") else ("partly" if b.startswith("partly") or "partly" in b else "directly_tested")
        assert b.startswith(("extrapolated", "partly", "tested")), basis_text
        emos = c.get("pair") or ([c["single_emotion"]] if c.get("single_emotion") else [])
        avoid_classes = c.get("avoid_classes", [])
        avoid_effort = c.get("avoid_effort", [])
        explicit = c.get("avoid_activity_ids", [])
        for aid in explicit + c.get("extra_activity_ids", []):
            if aid not in acts:
                raise SystemExit(f"{rid}: unknown activity id {aid}")
        rec_classes = c.get("recommend_classes", [])
        for cls in rec_classes + avoid_classes + c.get("follow_up_classes", []) + c.get("avoid_first_classes", []):
            if cls not in cr["class_definitions"]:
                raise SystemExit(f"{rid}: unknown class {cls}")
        resolved_avoid = list(explicit)
        for aid, a in acts.items():
            if aid in resolved_avoid:
                continue
            only_avoided = a["rule_classes"] and set(a["rule_classes"]) <= set(avoid_classes)
            if a["suggestable"] and (only_avoided or a["effort"] in avoid_effort or any(e in contra_ids(a) for e in emos)):
                resolved_avoid.append(aid)
        avoid_set = set(resolved_avoid)
        rec = resolve_classes(rec_classes, acts, avoid_set, *emos, avoid_classes=avoid_classes, avoid_effort=avoid_effort)
        for aid in c.get("extra_activity_ids", []):
            if aid not in rec and aid not in avoid_set:
                rec.append(aid)
        if c.get("max_typical_duration_min"):
            rec = [a for a in rec if acts[a]["typical_duration_min"] <= c["max_typical_duration_min"]]
        follow = [a for a in resolve_classes(c.get("follow_up_classes", []), acts, avoid_set, *emos, avoid_effort=avoid_effort) if a not in rec]
        cites, raw_cites = [], []
        for p in split_outside_parens(row["citation"]):
            e, how = match_citation(p, row["doi_or_url"], MODELS_FILE[:-3], ver)
            raw_cites.append((p, e))
            cites.append({"citation": p, "matched_verification_record": e["citation"] if e else None,
                          "pmid": e["pmid"] if e else "", "doi": e["doi_raw"] if e else "",
                          "verification_status": e["status"] if e else "unverified"})
        cats = []
        for cls in rec_classes:
            for cat in cr["class_to_category"][cls]:
                if cat not in cats:
                    cats.append(cat)
        out.append({
            "rule_id": rid, "rule_type": c["rule_type"], "priority": c["priority"],
            **({"pair": sorted(c["pair"])} if c.get("pair") else {}),
            **({"single_emotion": c["single_emotion"]} if c.get("single_emotion") else {}),
            "condition_text": row["condition"], "condition": c["condition"],
            "recommended_text": row["recommended activity classes"],
            "recommend_classes": rec_classes, "follow_up_classes": c.get("follow_up_classes", []),
            **({"conditional_classes": c["conditional_classes"]} if c.get("conditional_classes") else {}),
            **({"ask_user": c["ask_user"]} if c.get("ask_user") else {}),
            **({"use_user_hobbies": True} if c.get("use_user_hobbies") else {}),
            "recommend_categories": cats, "recommend_activity_ids": rec, "follow_up_activity_ids": follow,
            "avoid_text": row["activity classes to avoid"],
            "avoid_classes": avoid_classes, "avoid_first_classes": c.get("avoid_first_classes", []),
            "avoid_effort": avoid_effort, "avoid_categories": [],
            **({"max_typical_duration_min": c["max_typical_duration_min"]} if c.get("max_typical_duration_min") else {}),
            "avoid_activity_ids_explicit": explicit, "avoid_activity_ids": resolved_avoid,
            "rationale": row["rationale"], "citation": row["citation"], "doi_or_url": row["doi_or_url"],
            "citations_verification": cites,
            "evidence_basis": basis, "evidence_basis_text": basis_text,
            "is_extrapolation": basis != "directly_tested", "_cites": raw_cites,
            **({"app_note": c["app_note"]} if c.get("app_note") else {}),
        })
    return out


# ----------------------------------------------------------------------------- combination logic (also the runtime reference)
class Recommender:
    def __init__(self, cur, activities, rules_out, score_map):
        self.cur, self.W = cur, cur["weights"]
        self.R = self.W["runtime"]
        self.acts = OrderedDict((a["id"], a) for a in activities)
        self.rules = OrderedDict((r["rule_id"], r) for r in rules_out)
        self.score = score_map
        self.groups = cur["emotions"]["groups"]
        self.pair_rules = {tuple(r["pair"]): r for r in rules_out if r["rule_type"] == "pair"}
        self.single_rules = {r["single_emotion"]: r for r in rules_out if r["rule_type"] == "single"}

    def plan(self, emos):
        """Which rule(s) govern this set of 1-2 active emotions. Returns dict."""
        emos = list(emos)
        neg, pos = self.groups["negative"], self.groups["positive"]
        if len(emos) == 2:
            key = tuple(sorted(emos))
            if key in self.pair_rules:
                r = self.pair_rules[key]
                return self._from_rule(r, [r["rule_id"]], "pair_rule", r["evidence_basis"])
            if (emos[0] in neg) != (emos[1] in neg) and all(e in neg + pos for e in emos):
                r = self.rules["R27"]
                p = self._from_rule(r, ["R27"], "group_rule_mixed_valence", r["evidence_basis"])
                for cc in r.get("conditional_classes", []):
                    if set(rule_emotions(cc["when"])) == set(emos):
                        p["classes"] = [c for c in reversed(cc["add_classes"])] + p["classes"]
                return p
        parts, ids = [], []
        ordered = sorted(emos, key=lambda e: (e not in self.groups["tension"], emos.index(e)))
        for e in ordered:
            if e in self.single_rules:
                r = self.single_rules[e]
                parts.append({"classes": r["recommend_classes"], "avoid": r["avoid_activity_ids_explicit"],
                              "avoid_classes": r["avoid_classes"], "avoid_effort": r["avoid_effort"], "extra": []})
                ids.append(r["rule_id"])
            elif e == "restless":
                fb = self.cur["rules"]["restless_fallback"]
                parts.append({"classes": fb["recommend_classes"], "avoid": fb["avoid_activity_ids"], "avoid_classes": [],
                              "avoid_effort": [], "extra": []})
                ids.append("restless_fallback")
            elif e in pos or e == "neutral":
                r = self.rules["R25"] if e != "energetic" else self.rules["R24"]
                parts.append({"classes": r["recommend_classes"], "avoid": r["avoid_activity_ids_explicit"], "avoid_classes": [],
                              "avoid_effort": [], "extra": []})
                ids.append(r["rule_id"] + "_as_default")
        classes = []
        i = 0
        while parts and any(i < len(p["classes"]) for p in parts):
            for p in parts:
                if i < len(p["classes"]) and p["classes"][i] not in classes:
                    classes.append(p["classes"][i])
            i += 1
        avoid_classes = sorted({c for p in parts for c in p["avoid_classes"]})
        classes = [c for c in classes if c not in avoid_classes]
        single = len(emos) == 1
        basis = self.single_rules[emos[0]]["evidence_basis"] if single and emos[0] in self.single_rules else "extrapolated"
        return {"rule_ids": ids, "derivation": "single_emotion_rule" if single and emos[0] in self.single_rules else
                ("no_rule_in_notes_default" if single else "composed_from_single_emotion_rules"),
                "evidence_basis": basis, "classes": classes, "follow_up_classes": [],
                "avoid": sorted({a for p in parts for a in p["avoid"]}), "avoid_classes": avoid_classes,
                "avoid_effort": sorted({x for p in parts for x in p["avoid_effort"]}), "extra": [], "max_duration": None}

    def _from_rule(self, r, ids, derivation, basis):
        return {"rule_ids": ids, "derivation": derivation, "evidence_basis": basis, "classes": list(r["recommend_classes"]),
                "follow_up_classes": list(r["follow_up_classes"]), "avoid": list(r["avoid_activity_ids_explicit"]),
                "avoid_classes": list(r["avoid_classes"]), "avoid_effort": list(r["avoid_effort"]),
                "max_duration": r.get("max_typical_duration_min"),
                "extra": [a for a in r["recommend_activity_ids"] if not set(self.acts[a]["rule_classes"]) & set(r["recommend_classes"])]}

    def candidates(self, emos, plan, extra_contra=(), likes=(), dislikes=(), include_plan_to=False):
        out = []
        n = max(1, len(plan["classes"]))
        for aid, a in self.acts.items():
            if a["suggest_mode"] not in (("right_now", "plan_to") if include_plan_to else ("right_now",)):
                continue
            if aid in plan["avoid"] or a["effort"] in plan["avoid_effort"]:
                continue
            if plan.get("max_duration") and a["typical_duration_min"] > plan["max_duration"]:
                continue
            if any(e in contra_ids(a) for e in list(emos) + list(extra_contra)):
                continue
            if set(a["preference_tags"]) & set(dislikes) or aid in dislikes or a["category"] in dislikes:
                continue
            matched = [c for c in plan["classes"] if c in a["rule_classes"]]
            if a["rule_classes"] and set(a["rule_classes"]) <= set(plan["avoid_classes"]):
                continue
            in_rule = bool(matched) or aid in plan["extra"]
            ev = sum(self.score[e].get(aid, 0.0) for e in emos) / max(1, len(emos))
            if not in_rule and ev == 0:
                continue
            order = (1 - plan["classes"].index(matched[0]) / n) if matched else 0.0
            tags = set(a["preference_tags"]) | {a["category"]}
            pref = (len(tags & set(likes)) / len(likes)) if likes else 0.0
            base = (self.R["rule_bonus"] if in_rule else 0.0) + ev + self.R["class_order_weight"] * order
            out.append({"activity_id": aid, "in_rule": in_rule, "class": matched[0] if matched else (a["rule_classes"][0] if a["rule_classes"] else a["category"]),
                        "evidence_component": round(ev, 3), "preference_match": round(pref, 3),
                        "score": round(base + self.R["preference_weight"] * pref, 3)})
        effort_rank = {"low": 0, "medium": 1, "high": 2}
        out.sort(key=lambda c: (not c["in_rule"], -c["score"], effort_rank[self.acts[c["activity_id"]]["effort"]], c["activity_id"]))
        return out

    def first_class_filter(self, plan, cands):
        """Slot 1 goes to the best candidate of the rule's first-listed class that has any candidate."""
        for cls in plan["classes"]:
            if any(c["class"] == cls and c["in_rule"] for c in cands):
                return lambda c, cls=cls: c["class"] == cls and c["in_rule"]
        return None

    @staticmethod
    def diverse(cands, k, first_filter=None):
        picked, used = [], Counter()
        pool = list(cands)
        if first_filter:
            firsts = [c for c in pool if first_filter(c)]
            if firsts:
                picked.append(firsts[0])
                used[firsts[0]["class"]] += 1
                pool.remove(firsts[0])
        for tier in (True, False):  # rule-allowed candidates are exhausted before evidence-only ones
            for limit in (1, 2, 99):
                for c in pool:
                    if len(picked) >= k:
                        break
                    if c["in_rule"] != tier or c in picked or used[c["class"]] >= limit:
                        continue
                    picked.append(c)
                    used[c["class"]] += 1
        return picked[:k]

    def pair_row(self, a, b):
        plan = self.plan([a, b])
        cands = self.candidates([a, b], plan)
        top = self.diverse(cands, 5, first_filter=self.first_class_filter(plan, cands))
        neg = self.groups["negative"]
        ptype = "negative_negative" if a in neg and b in neg else ("positive_positive" if a not in neg and b not in neg else "mixed_valence")
        return {
            "emotion_a": a, "emotion_b": b, "pair_key": "+".join(sorted([a, b])), "pair_type": ptype,
            "recommended_activity_ids": [c["activity_id"] for c in top],
            "recommended_from_rule": [c["in_rule"] for c in top],
            "n_recommended_with_evidence_for_either_emotion": sum(1 for c in top if c["evidence_component"] > 0),
            "rules_applied": plan["rule_ids"], "derivation": plan["derivation"], "evidence_basis": plan["evidence_basis"],
            "recommend_classes": plan["classes"], "follow_up_classes": plan["follow_up_classes"],
            "avoid_activity_ids": plan["avoid"], "avoid_classes": plan["avoid_classes"], "avoid_effort": plan["avoid_effort"],
            "is_extrapolation": plan["evidence_basis"] != "directly_tested",
            "note": ("Pair rule from the notes." if plan["derivation"] == "pair_rule" else
                     "No pair rule in the notes; mixed-valence group rule R27 applied." if plan["derivation"].startswith("group") else
                     "No pair rule in the notes; composed from the single-emotion rules (tension emotion first, union of avoid lists).")
                    + " No trial tested this emotion pair as a pair; ordering uses single-emotion evidence scores.",
        }

    def recommend(self, scores, likes=(), dislikes=()):
        """Reference implementation of the decision procedure documented in schema.md."""
        R = self.R
        neg = self.groups["negative"]
        trace = {"input": scores, "likes": list(likes), "dislikes": list(dislikes)}
        if any(scores.get(e, 0) >= R["crisis_threshold"] for e in neg):
            return {**trace, "outcome": "crisis_gate", "rule": "R30", "suggestions": []}
        active = sorted([e for e, v in scores.items() if v >= R["active_threshold"] and e != "neutral"], key=lambda e: (-scores[e], e))
        keep = active[:2]
        if len(active) > 2 and scores[active[1]] - scores[active[2]] <= R["third_emotion_margin"]:
            keep = active[:3]
        trace["active_emotions"] = keep
        core = keep[:2] if keep else ["neutral"]
        plan = self.plan(core)
        intensity = max([scores.get(e, 0) for e in neg] + [0])
        gate = intensity >= R["high_intensity_threshold"]
        # with no active emotion, R25 is the default and its own pair (calm + content) supplies the evidence scores
        cands = self.candidates(core if keep else ["calm", "content"], plan, extra_contra=keep[2:], likes=likes, dislikes=dislikes)
        first = None
        if gate:
            r01 = self.rules["R01"]
            cands = [c for c in cands if not ("context:high_intensity" in {f"{x['kind']}:{x['id']}" for x in self.acts[c["activity_id"]]["contraindicated_for"]})]
            pool = self.candidates(core, {**plan, "classes": r01["recommend_classes"], "extra": []}, extra_contra=keep[2:], likes=likes, dislikes=dislikes)
            pool = [c for c in pool if c["in_rule"]]
            if pool:
                first = pool[0]
                cands = [first] + [c for c in cands if c["activity_id"] != first["activity_id"]]
        top = self.diverse(cands, R["max_suggestions"],
                           first_filter=(lambda c: c is first) if first else self.first_class_filter(plan, cands))
        trace.update({"derived": {"tension": max(scores.get(e, 0) for e in self.groups["tension"]),
                                  "energy": round(scores.get("energetic", 0) - max(scores.get("tired", 0), 0.5 * scores.get("bored", 0)), 3),
                                  "intensity_negative": intensity},
                      "high_intensity_gate_R01": gate, "rules_applied": plan["rule_ids"] + (["R01"] if gate else []) + ["R29"],
                      "derivation": plan["derivation"], "evidence_basis": plan["evidence_basis"],
                      "allowed_classes": plan["classes"], "avoid_activity_ids": plan["avoid"], "avoid_effort": plan["avoid_effort"],
                      "outcome": "suggestions", "suggestions": top, "candidates_considered": len(cands),
                      "next_candidates": [c for c in cands if c not in top][:5]})
        return trace


# ----------------------------------------------------------------------------- sources
def build_sources(ver, links, rules_out):
    groups = []
    for e in ver:
        target = None
        for g in groups:
            if (e["doi"] and e["doi"] in g["dois"]) or (e["pmid"] and e["pmid"] in g["pmids"]):
                target = g
                break
        if target is None:
            target = {"entries": [], "dois": set(), "pmids": set()}
            groups.append(target)
        target["entries"].append(e)
        if e["doi"]:
            target["dois"].add(e["doi"])
        if e["pmid"]:
            target["pmids"].add(e["pmid"])
    # merge id-less groups into a unique same author+year group
    merged = []
    for g in groups:
        if not g["dois"] and not g["pmids"]:
            k = {(x["surname"], x["year"]) for x in g["entries"]}
            hits = [h for h in groups if h is not g and (h["dois"] or h["pmids"]) and
                    {(x["surname"], x["year"]) for x in h["entries"]} & k and all(kk[0] and kk[1] for kk in k)]
            if len(hits) == 1:
                hits[0]["entries"].extend(g["entries"])
                continue
            same = [h for h in merged if not h["dois"] and not h["pmids"] and {(x["surname"], x["year"]) for x in h["entries"]} & k
                    and all(kk[0] and kk[1] for kk in k)]
            if same:
                same[0]["entries"].extend(g["entries"])
                continue
        merged.append(g)
    link_use, rule_use = Counter(), Counter()
    cite_to_entry = {}
    for g in merged:
        for e in g["entries"]:
            cite_to_entry[(e["file"], e["citation"])] = id(g)
    unmatched = OrderedDict()
    for l in links:
        for p, e in l["_cites"]:
            if e:
                link_use[cite_to_entry[(e["file"], e["citation"])]] += 1
            else:
                u = unmatched.setdefault(p, {"files": set(), "n": 0})
                u["files"].add(l["source_notes_file"])
                u["n"] += 1
    for r in rules_out:
        for p, e in r["_cites"]:
            if e:
                rule_use[cite_to_entry[(e["file"], e["citation"])]] += 1
            else:
                u = unmatched.setdefault(p, {"files": set(), "n": 0})
                u["files"].add(MODELS_FILE)
    rows = []
    for g in merged:
        es = g["entries"]
        main = max(es, key=lambda e: (bool(e["doi"]), bool(e["pmid"]), len(e["citation"])))
        worst = min(es, key=lambda e: STATUS_RANK[e["status"]])["status"]
        statuses = sorted({e["status"] for e in es})
        if len(statuses) > 1 and STATUS_RANK[worst] == max(STATUS_RANK[s] for s in statuses):
            worst = "corrected" if "corrected" in statuses else worst
        m = re.search(r"\b(19|20)\d\d\b", main["citation"])
        journal = ""
        if m and m.start() > 0:
            rest = main["citation"][m.end():].lstrip(" ,.;)")
            journal = re.split(r"\s+\d|\s*\(|;|$", rest, maxsplit=1)[0].strip(" ,.")
        used_ds = [n for n, c in (("evidence_links", link_use[id(g)]), ("combination_rules", rule_use[id(g)])) if c]
        rows.append({
            "citation": main["citation"], "year": m.group(0) if m else "", "journal": journal,
            "doi": next((e["doi_raw"] for e in es if e["doi"]), ""), "pmid": next((e["pmid"] for e in es if e["pmid"]), ""),
            "verification_status": worst,
            "verification_status_by_file": [f"{e['file']}={e['status']}" for e in es],
            "used_in": sorted({e["file"] + ".md" for e in es}),
            "used_in_dataset": used_ds or ["notes_prose_only"],
            "n_evidence_links": link_use[id(g)], "n_rules": rule_use[id(g)],
        })
    for p, u in unmatched.items():
        m = re.search(r"\b(19|20)\d\d\b", p)
        rows.append({"citation": p, "year": m.group(0) if m else "", "journal": "", "doi": "", "pmid": "",
                     "verification_status": "unverified", "verification_status_by_file": [],
                     "used_in": sorted(u["files"]), "used_in_dataset": ["evidence_links" if u["n"] else "combination_rules"],
                     "n_evidence_links": u["n"], "n_rules": 0 if u["n"] else 1})
    rows.sort(key=lambda r: norm_text(r["citation"]))
    return rows


# ----------------------------------------------------------------------------- main
LINK_FIELDS = ["link_id", "activity_id", "emotion_id", "original_target_emotion", "emotion_mapping", "direction", "direction_class",
               "effect_size", "effect_size_value", "effect_metric", "evidence_level", "evidence_level_class",
               "evidence_strength", "evidence_strength_class", "dose_tested", "population", "citation", "doi_or_url", "doi", "pmid",
               "verification_status", "verification_status_all_citations", "row_has_unconfirmed_text", "single_session_evidence",
               "cautions", "flags", "link_score", "category_level_evidence", "low_applicability", "constructs", "preference_tags",
               "original_activity", "source_notes_file", "source_row", "source_row_id", "overrides_applied"]


def main():
    cur = load_curation()
    ver = load_verification()
    links, row_records, match_log = build_links(cur, ver)
    W = cur["weights"]
    for l in links:
        l["link_score"] = round(link_score(l, W), 3) if l["direction_class"] == "benefit" else ""
    emotions = build_emotions(cur, links)
    activities = build_activities(cur, links)
    rules_out = build_rules(cur, activities, ver)
    recs, score_map = build_recommendations(cur, links, activities, emotions, rules_out)
    rec = Recommender(cur, activities, rules_out, score_map)

    neg = cur["emotions"]["groups"]["negative"]
    pairs = [(a, b) for i, a in enumerate(neg) for b in neg[i + 1:]] + [tuple(p) for p in cur["rules"]["matrix_extra_pairs"]]
    matrix = [rec.pair_row(a, b) for a, b in pairs]
    sources = build_sources(ver, links, rules_out)

    # ---- write
    write_json(DATA / "emotions.json", emotions)
    write_json(DATA / "activities.json", {
        "meta": {"n_activities": len(activities),
                 "suggest_mode_values": {"right_now": "can be suggested as an immediate 1-45 min activity",
                                         "plan_to": "evidence is programme-level or needs other people/booking; offer as a plan-ahead idea",
                                         "avoid": "never suggest; kept so the evidence for NOT suggesting it is traceable",
                                         "reference_only": "generic or professional-led evidence row; not a concrete suggestion"},
                 "note": "Instructions are plain-language paraphrases grounded in the dose tested; they are not clinical advice."},
        "activities": activities})
    write_csv(DATA / "evidence_links.csv", links, LINK_FIELDS)
    write_json(DATA / "evidence_links.json", {
        "meta": {"n_links": len(links), "n_source_rows": len(row_records),
                 "note": "One record per (source row x activity_id x emotion_id). A notes row that names several emotions, or a category-level row mapped to several activities, expands into several links sharing a source_row_id."},
        "links": [{k: l.get(k) for k in LINK_FIELDS} for l in links]})
    write_json(DATA / "recommendations.json", {
        "meta": {"score": "see schema.md (evidence_score)", "weights": {k: v for k, v in W.items() if not k.startswith("_")},
                 "note": "Ranking reflects evidence quality for each emotion taken alone. Effects are small on average: present suggestions as 'may help'."},
        "by_emotion": recs})
    pair_index = {"+".join(r["pair"]): r["rule_id"] for r in rules_out if r["rule_type"] == "pair"}
    n_extrap = sum(1 for r in rules_out if r["evidence_basis"] == "extrapolated")
    write_json(DATA / "combination_rules.json", {
        "meta": {
            "source": f"research_notes/Emotion to activity evidence map/{MODELS_FILE} (## Matching rules)",
            "warning": f"MOST COMBINATION RULES ARE EXTRAPOLATIONS. Of 30 rules, {n_extrap} are 'extrapolated', "
                       f"{sum(1 for r in rules_out if r['evidence_basis'] == 'partly')} 'partly' tested and only "
                       f"{sum(1 for r in rules_out if r['evidence_basis'] == 'directly_tested')} 'directly_tested' (none of which is a pair rule). "
                       "The notes state that no meta-analysis compares activity classes by emotion combination.",
            "thresholds": {"moderate_gte": 0.4, "high_gte": 0.75, "crisis_gte": 0.9, "label": "uncalibrated engineering defaults"},
            "condition_grammar": {
                "all / any": "list of sub-conditions; all must hold / at least one must hold",
                "{emotion, gte, lt}": "score of that emotion id is >= gte and (if given) < lt",
                "{group, gte, lt}": "max score over the emotion group (see emotions.json groups) is >= gte / < lt",
                "{signal}": "boolean supplied by the app (persistent_severe_negative, self_harm_cue, severe_self_report)",
                "{selected_class}": "true when the user picked an activity of that rule class",
                "{always}": "always true"},
            "evaluation_order": "Highest priority first: R30 safety gate (100) > R01 intensity gate (90) > pair rules (60) > R27 mixed valence (50) > single-emotion rules (40) > R02 (10) > R28 (5) > R29 (1, always).",
            "label_aliases": {"happy": "content", "excited": "energetic"},
            "class_definitions": cur["rules"]["class_definitions"],
            "class_to_activity_ids": {cls: [a["id"] for a in activities if cls in a["rule_classes"] and a["suggestable"]]
                                      for cls in cur["rules"]["class_definitions"]},
            "class_to_category": cur["rules"]["class_to_category"],
            "pair_index": dict(sorted(pair_index.items())),
            "restless_fallback": cur["rules"]["restless_fallback"],
        },
        "rules": [{k: v for k, v in r.items() if not k.startswith("_")} for r in rules_out]})
    write_csv(DATA / "combination_matrix.csv", matrix,
              ["emotion_a", "emotion_b", "pair_key", "pair_type", "recommended_activity_ids", "recommended_from_rule",
               "n_recommended_with_evidence_for_either_emotion", "rules_applied", "derivation", "evidence_basis", "is_extrapolation",
               "recommend_classes", "follow_up_classes", "avoid_activity_ids", "avoid_classes", "avoid_effort", "note"])
    caut_index = {a["id"]: {"cautions": a["cautions"], "contraindicated_for": a["contraindicated_for"], "suggest_mode": a["suggest_mode"]}
                  for a in activities if a["cautions"] or a["contraindicated_for"]}
    safety = {k: v for k, v in cur["safety"].items() if not k.startswith("_")}
    safety = {"meta": {"source": f"{MODELS_FILE} section 6 and {HANDWRITING_FILE} 'Recommendations for the app'",
                       "status": "Design recommendations derived from the notes; not trial-tested. Thresholds are uncalibrated engineering defaults."},
              **safety,
              "never_suggest_activity_ids": [a["id"] for a in activities if a["suggest_mode"] == "avoid"],
              "per_activity_cautions": caut_index}
    write_json(DATA / "safety.json", safety)
    write_csv(DATA / "sources.csv", sources, ["citation", "year", "journal", "doi", "pmid", "verification_status",
                                              "verification_status_by_file", "used_in", "used_in_dataset", "n_evidence_links", "n_rules"])

    # ---- quality checks
    act_ids = {a["id"] for a in activities}
    emo_ids = {e["id"] for e in emotions["emotions"]} | {a["id"] for a in emotions["aggregate_targets"]}
    class_ids = {e["id"] for e in emotions["emotions"]}
    assert len(row_records) == sum(1 for _ in row_records) and len(row_records) >= 220, len(row_records)
    for l in links:
        assert l["activity_id"] in act_ids, l["link_id"]
        assert l["emotion_id"] in emo_ids, l["link_id"]
        assert l["citation"].strip(), f"link without citation: {l['link_id']}"
        assert l["verification_status"] in STATUS_RANK
        assert l["single_session_evidence"] in ("true", "false", "unknown")
        assert l["direction_class"] in ("benefit", "null", "harm", "mixed_or_unclear")
    assert len({l["link_id"] for l in links}) == len(links), "duplicate link ids"
    assert {r["source_row_id"] for r in row_records} == {l["source_row_id"] for l in links}, "a notes row was dropped"
    for eid, r in recs.items():
        assert eid in class_ids
        for x in r["recommended"]:
            assert x["activity_id"] in act_ids and x["top_citation"].strip()
        for x in r["avoid"]:
            assert x["activity_id"] in act_ids
    for r in rules_out:
        for k in ("recommend_activity_ids", "follow_up_activity_ids", "avoid_activity_ids"):
            assert set(r[k]) <= act_ids, (r["rule_id"], k)
        assert not set(r["recommend_activity_ids"]) & set(r["avoid_activity_ids"]), r["rule_id"]
        for e in rule_emotions(r["condition"]):
            assert e in class_ids, (r["rule_id"], e)
    for m in matrix:
        assert set(m["recommended_activity_ids"]) <= act_ids and 3 <= len(m["recommended_activity_ids"]) <= 5, m["pair_key"]
        assert m["emotion_a"] in class_ids and m["emotion_b"] in class_ids
        assert not set(m["recommended_activity_ids"]) & set(m["avoid_activity_ids"])
    for a in activities:
        for c in a["contraindicated_for"]:
            if c["kind"] == "emotion":
                assert c["id"] in class_ids, (a["id"], c)
    for aid in safety["crisis_gate"]["optional_activity_ids"]:
        assert aid in act_ids
    for f in ("emotions.json", "activities.json", "evidence_links.json", "recommendations.json", "combination_rules.json", "safety.json"):
        json.loads(read(DATA / f))
    with open(DATA / "evidence_links.csv", encoding="utf-8", newline="") as fh:
        assert sum(1 for _ in csv.DictReader(fh)) == len(links)

    # ---- summary
    stats = summarise(links, row_records, activities, recs, rules_out, matrix, sources, cur)
    example = rec.recommend({"stressed": 0.7, "tired": 0.5}, likes=["creative", "indoor", "solo"])
    (DATA / "schema.md").write_text(render_schema(cur, stats, example, rec, activities, recs), encoding="utf-8")
    print_summary(stats, match_log)


def summarise(links, row_records, activities, recs, rules_out, matrix, sources, cur):
    st = OrderedDict()
    st["n_source_rows"] = len(row_records)
    st["rows_per_file"] = dict(Counter(r["source_notes_file"] for r in row_records))
    st["n_links"] = len(links)
    st["n_activities"] = len(activities)
    st["activities_by_mode"] = dict(Counter(a["suggest_mode"] for a in activities))
    st["activities_by_category"] = dict(Counter(a["category"] for a in activities))
    order = [e for e in cur["emotions"]["emotions"]] + [a["id"] for a in cur["emotions"]["aggregate_targets"]]
    st["links_per_emotion"] = OrderedDict((e, sum(1 for l in links if l["emotion_id"] == e)) for e in order)
    st["direct_links_per_emotion"] = OrderedDict((e, sum(1 for l in links if l["emotion_id"] == e and l["emotion_mapping"] == "direct")) for e in order)
    st["benefit_links_per_emotion"] = OrderedDict((e, sum(1 for l in links if l["emotion_id"] == e and l["direction_class"] == "benefit")) for e in order)
    vs = Counter(l["verification_status"] for l in links)
    st["links_by_verification"] = OrderedDict((k, vs.get(k, 0)) for k in STATUS_RANK if vs.get(k, 0) or k != "unverified")
    st["rows_by_verification"] = dict(Counter(r["verification_status"] for r in row_records))
    st["links_by_direction"] = dict(Counter(l["direction_class"] for l in links))
    st["links_by_single_session"] = dict(Counter(l["single_session_evidence"] for l in links))
    st["links_with_numeric_effect"] = sum(1 for l in links if l["effect_size_value"] != "")
    st["rows_with_unconfirmed_text"] = sum(1 for r in row_records if r["row_has_unconfirmed_text"])
    cons = Counter()
    for l in links:
        for c in l["constructs"]:
            cons[c] += 1
    st["links_by_construct"] = dict(sorted(cons.items(), key=lambda x: -x[1]))
    st["thin"] = OrderedDict((e, r["evidence_depth"]) for e, r in recs.items())
    comments = {"loneliness": "single-session rows measure felt connection or mood, not chronic loneliness",
                "boredom": "one experiment plus theory; several rows are null or 'unclear'",
                "overwhelm": "outcomes are sleep onset, intrusive task thoughts, goal attainment or correlates, not felt overwhelm",
                "rumination": "one 90-min nature-walk experiment; the self-compassion and worry-postponement estimates come from sources not in PubMed",
                "anger": "dominated by one category-level meta-analysis"}
    home = {"loneliness": ["lonely"], "boredom": ["bored"], "overwhelm": ["stressed"], "rumination": ["sad", "anxious"], "anger": ["angry"]}
    cd = OrderedDict()
    for c, note in comments.items():
        ls = [l for l in links if c in l["constructs"] and l["emotion_id"] in home[c]]
        cd[c] = {"n_links": len(ls), "n_source_rows": len({l["source_row_id"] for l in ls}),
                 "n_benefit": sum(1 for l in ls if l["direction_class"] == "benefit"),
                 "n_direct_verified_benefit": sum(1 for l in ls if l["direction_class"] == "benefit" and l["emotion_mapping"] == "direct"
                                                  and l["verification_status"] in VERIFIED_OK),
                 "comment": note}
    st["construct_depth"] = cd
    st["rules_by_basis"] = dict(Counter(r["evidence_basis"] for r in rules_out))
    st["matrix_rows"] = len(matrix)
    st["matrix_by_derivation"] = dict(Counter(m["derivation"] for m in matrix))
    st["matrix_by_basis"] = dict(Counter(m["evidence_basis"] for m in matrix))
    st["n_sources"] = len(sources)
    st["sources_by_status"] = dict(Counter(s["verification_status"] for s in sources))
    return st


def print_summary(st, match_log):
    print("=== build_dataset summary ===")
    print("source rows:", st["n_source_rows"], st["rows_per_file"])
    print("evidence links:", st["n_links"], "| activities:", st["n_activities"], st["activities_by_mode"])
    print("activities by category:", st["activities_by_category"])
    print("links per emotion (all / direct mapping / benefit direction):")
    for e, n in st["links_per_emotion"].items():
        print(f"  {e:26s} {n:4d} {st['direct_links_per_emotion'][e]:4d} {st['benefit_links_per_emotion'][e]:4d}")
    tot = st["n_links"]
    print("links by verification_status:")
    for k, v in st["links_by_verification"].items():
        print(f"  {k:40s} {v:4d}  {100 * v / tot:5.1f}%")
    print("source rows by verification_status:", st["rows_by_verification"])
    print("links by direction_class:", st["links_by_direction"])
    print("links by single_session_evidence:", st["links_by_single_session"])
    print("links with a numeric effect_size_value:", st["links_with_numeric_effect"])
    print("rows containing unconfirmed/unverified wording:", st["rows_with_unconfirmed_text"])
    print("links by construct tag:", st["links_by_construct"])
    print("evidence depth per emotion (ranked activities / direct+verified benefit activities / ...single-session right-now / thin):")
    for e, d in st["thin"].items():
        print(f"  {e:10s} ranked={d['n_activities_ranked']:3d} direct_verified={d['n_activities_with_direct_verified_benefit']:3d} "
              f"single_session_now={d['n_right_now_activities_with_direct_verified_single_session_benefit']:3d} thin={d['thin_evidence']} "
              f"thin_for_right_now_use={d['thin_for_right_now_use']}")
    print("constructs without a class of their own (links / source rows / benefit / direct+verified benefit):")
    for c, v in st["construct_depth"].items():
        print(f"  {c:11s} {v['n_links']:3d} {v['n_source_rows']:3d} {v['n_benefit']:3d} {v['n_direct_verified_benefit']:3d}  {v['comment']}")
    print("rules by evidence_basis:", st["rules_by_basis"])
    print("combination matrix rows:", st["matrix_rows"], st["matrix_by_derivation"], st["matrix_by_basis"])
    print("sources:", st["n_sources"], st["sources_by_status"])
    un = [m for m in match_log if m[5] == "unmatched"]
    print(f"citations not matched to a verification record ({len(un)}):")
    for m in un:
        print("   ", m[0], m[1], m[2])
    print("All quality checks passed.")


def render_schema(cur, st, example, rec, activities, recs):
    from schema_template import render  # local module next to this script
    return render(cur, st, example, rec, activities, recs, STATUS_RANK)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
