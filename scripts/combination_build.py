"""Combination-evidence layer of the dataset build. Imported by build_dataset.py.

Reads (never modifies) research_notes/Emotion combination evidence map/*.md:
  co_occurrence_prevalence.md              "## Pair prevalence table"
  multi_outcome_physical_nature_mindbody.md "## Multi-outcome rows", "## Baseline moderation findings"
  multi_outcome_creative_social_rest.md    "## Multi-outcome rows", "## Baseline moderation findings"
  mixed_state_interventions.md             "## Combination evidence rows", "## Rule review"
plus the hand-curated tables data/curation/combo_*.csv and prevalence_overrides.csv.

Nothing here generates a statistic, PMID or DOI: every value is copied from a notes table cell.
Verification tags ([PM-full], [PM-abs], [prior-notes], [web], [memory]) are carried through verbatim
(normalised to the bracketed form).
"""
import csv
import re
from collections import OrderedDict, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMBO_NOTES = ROOT / "research_notes" / "Emotion combination evidence map"
CUR = ROOT / "data" / "curation"

PREV_FILE = "co_occurrence_prevalence.md"
CPN_FILE = "multi_outcome_physical_nature_mindbody.md"
CCS_FILE = "multi_outcome_creative_social_rest.md"
CMX_FILE = "mixed_state_interventions.md"
ABBR = {CPN_FILE: "CPN", CCS_FILE: "CCS", CMX_FILE: "CMX", PREV_FILE: "PRV"}

TAGS = ["[PM-full]", "[PM-abs]", "[prior-notes]", "[web]", "[memory]"]
NEG = ["stressed", "anxious", "angry", "restless", "sad", "lonely", "tired", "bored"]
POS = ["calm", "content", "energetic"]
OUTCOMES = OrderedDict([
    ("both_improved", "every emotion of the combination improved in the same study row (for a pair listed under combination_pairs_supported, or a combination row whose finding says so)"),
    ("one_not_improved", "one emotion improved, the other was measured and did not improve (ns), or was not reported as changed"),
    ("one_worsened", "at least one emotion of the combination got worse; the activity is excluded for that combination in the matrix"),
    ("neither_improved", "both emotions measured, neither improved (or neither beat the comparator)"),
    ("mixed", "changes in both directions, or the result depends on a moderator, framing or comparator"),
    ("single_emotion_only", "only one emotion of the combination was measured; the row is linked to the combination through a rule (evidence_basis single_emotion_extrapolation)"),
    ("proxy_outcome", "the outcome is a mechanism or proxy (detachment, recovery, performance, perceived support), not the emotions themselves"),
    ("association_only", "correlational, diary or rating evidence; no change was tested"),
    ("general_principle", "a regulation principle for any mixed state; not tied to a specific combination"),
])
BASES = ["directly_tested_on_combination", "same_sample_both_outcomes", "pooled_parallel_outcomes", "single_emotion_extrapolation"]
BASIS_FROM_NOTES = {"directly_tested_on_combination": "directly_tested_on_combination",
                    "tested_on_both_outcomes": "same_sample_both_outcomes",
                    "single_emotion_extrapolation": "single_emotion_extrapolation"}
GENERAL_KEYS = {"(any mix)": "any_mix", "(any negative mix)": "any_negative_mix"}


# ----------------------------------------------------------------------------- generic helpers
def read(path):
    return Path(path).read_text(encoding="utf-8")


def parse_table(text, heading):
    """Markdown table after `heading`, split on '|' (cells in these notes never contain a pipe)."""
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
        cells = [c.strip() for c in line.strip()[1:-1].split("|")]
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            raise SystemExit(f"{heading!r}: expected {len(header)} cells, got {len(cells)}: {line[:90]}")
        rows.append(OrderedDict(zip(header, cells)))
    if not rows:
        raise SystemExit(f"No table rows under {heading!r}")
    return header, rows


def split_outside(s, seps=";,"):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch in "([":
            depth += 1
        elif ch in ")]":
            depth = max(0, depth - 1)
        if ch in seps and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def norm_tags(raw):
    """'PM-abs / PM-full' -> (['[PM-full]', '[PM-abs]'], '[PM-abs]'). Second value = most conservative tag."""
    found = []
    for t in re.findall(r"PM-full|PM-abs|prior-notes|web|memory", raw or ""):
        b = f"[{t}]"
        if b not in found:
            found.append(b)
    if not found:
        raise SystemExit(f"Unrecognised verification tag {raw!r}")
    found.sort(key=TAGS.index)
    return found, max(found, key=TAGS.index)


def norm_pmid(s):
    s = (s or "").strip()
    return s if re.fullmatch(r"\d{6,9}", s) else ""


def pmid_from_url(u):
    m = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{6,9})", u or "")
    return m.group(1) if m else ""


def norm_doi(s):
    m = re.search(r"10\.\d{4,9}/[^\s;,)\]]+", s or "")
    return m.group(0).lower().rstrip(".").replace("//", "/") if m else ""


def combo_key(emos):
    return "+".join(sorted(emos))


def design_class(design):
    d = design.lower()
    if re.search(r"umbrella|meta-analys|multilevel meta", d):
        return "meta_analysis"
    if re.search(r"systematic review|\breview\b", d):
        return "systematic_review"
    if "quasi" in d:
        return "quasi_experimental"
    if re.search(r"\brct\b|randomi[sz]ed|randomised", d):
        return "rct"
    if re.search(r"\bcontrolled\b", d):
        return "controlled_or_crossover"
    if re.search(r"single-arm|single-group|pre-post|repeated measures|single-session", d):
        return "pre_post"
    if re.search(r"crossover|counterbalanced|within-subject|experiment|comparison|\bvs\b", d):
        return "controlled_or_crossover"
    if re.search(r"survey|cross-sectional|\bema\b|\besm\b|diary|observational|prospective|longitudinal|correlational", d):
        return "observational"
    return "other"


# ----------------------------------------------------------------------------- curation
def load_combo_curation():
    cur = {}
    am = {}
    with open(CUR / "combo_activity_map.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            ids = []
            for item in [x for x in r["activity_ids"].split(";") if x]:
                aid, mtype = item.split("=")
                assert mtype in ("exact", "close", "proxy"), item
                ids.append((aid, mtype))
            am[r["raw_activity"]] = {"ids": ids, "note": r["note"]}
    cur["activity_map"] = am
    po = defaultdict(list)
    with open(CUR / "combo_pair_overrides.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            po[(r["source"], int(r["row"]), r["field"])].append(r)
    cur["pair_overrides"] = po
    mo = {}
    with open(CUR / "combo_mixed_outcomes.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            mo[int(r["row"])] = r
    cur["mixed_outcomes"] = mo
    pv = defaultdict(list)
    with open(CUR / "prevalence_overrides.csv", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            pv[int(r["row"])].append(r)
    cur["prevalence_overrides"] = pv
    return cur


def map_activity(cc, raw, where):
    if raw not in cc["activity_map"]:
        raise SystemExit(f"Unmapped combination activity {raw!r} ({where}); add it to data/curation/combo_activity_map.csv")
    return cc["activity_map"][raw]["ids"]


# ----------------------------------------------------------------------------- per-cell heuristics
NOT_IMPROVED_PAT = re.compile(r"\bns\b|n\.s\.|not reported sig|not sig|unaffected|marginal|\btrend\b|no change|minimal|"
                              r"not listed|unchanged|little consistent|borderline|p ?= ?\.06|p ?= ?\.055", re.I)
UNCLEAR_PAT = re.compile(r"not reported|composite|pooled|unspecified|\(within|promising|indirect|^negative subscales", re.I)
EFFECT_ONLY_PAT = re.compile(r"\bsig\b|favoured|\bg\b|SMD|WMD|\bd\b|Δ|δ|η|[−-]\d|\+\d|\d", re.I)
PHYSIO_INVERSE = re.compile(r"cortisol|amylase|\bHR\b|HRV", re.I)


def cell_status(emotion, text):
    t = (text or "").strip()
    if not t or t in ("—", "-"):
        return "not_measured"
    if re.search(r"\bworse\b|worsen", t, re.I):
        return "worsened"
    if NOT_IMPROVED_PAT.search(t):
        return "not_improved"
    if UNCLEAR_PAT.search(t):
        return "unclear"
    arrows = [c for c in t if c in "↑↓"]
    if arrows:
        a = arrows[0]
        good = "↓" if emotion in NEG else "↑"
        if emotion not in NEG and PHYSIO_INVERSE.search(t):
            good = "↓"
        if re.search(r"inverse|belonging|interest", t, re.I) or (emotion == "sad" and re.search(r"mood ↑|↑ mood", t)):
            return "improved"
        return "improved" if a == good else "worsened"
    if EFFECT_ONLY_PAT.search(t):
        return "improved"
    return "unclear"


PAIR_TOKEN = re.compile(r"^(\(?[a-z]+\)?(?:\+\(?[a-z]+\)?)+)\s*(\(.*\))?\s*$")


def parse_pairs(cell, class_ids):
    """Returns (list of (key, emotions, qualifier, proxy_flag)), unparsed tokens."""
    c = (cell or "").strip()
    if c in ("", "—", "-"):
        return [], []
    out, bad = [], []
    m = re.search(r"all pairs among ([a-z, ]+)", c)
    if m:
        emos = [e.strip() for e in m.group(1).split(",") if e.strip()]
        if all(e in class_ids for e in emos):
            for a, b in combinations(emos, 2):
                out.append((combo_key([a, b]), sorted([a, b]), "all pairs among " + ", ".join(emos), False))
            c = (c[:m.start()] + c[m.end():]).strip(" ;,")
            if not c:
                return out, bad
    for tok in split_outside(c):
        mm = PAIR_TOKEN.match(tok)
        if not mm:
            bad.append(tok)
            continue
        parts = mm.group(1).split("+")
        emos = [p.strip("()") for p in parts]
        if not all(e in class_ids for e in emos) or len(set(emos)) != len(emos):
            bad.append(tok)
            continue
        proxy = any(p.startswith("(") for p in parts)
        out.append((combo_key(emos), sorted(emos), (mm.group(2) or "").strip("() "), proxy))
    return out, bad


# ----------------------------------------------------------------------------- source index
def author_year(citation):
    """('surname', 'year') of a citation string: first word of the first author, and the first 19xx/20xx year."""
    c = (citation or "").lower()
    m = re.search(r"\b(19|20)\d\d\b", c)
    head = re.split(r",| & | et al|\(| \d{4}", c, maxsplit=1)[0].strip()
    return (head.split(" ")[0] if head else "", m.group(0) if m else "")


class SourceIndex:
    """Citations seen in the combination notes tables, keyed by PMID, else DOI, else URL/citation."""

    def __init__(self):
        self.by_key = OrderedDict()
        self.doi_to_key, self.pmid_to_key = {}, {}

    def add(self, citation, pmid, doi_or_url, tags, file, dataset):
        pmid = norm_pmid(pmid) or pmid_from_url(doi_or_url)
        doi = norm_doi(doi_or_url)
        url = "" if doi or pmid else (doi_or_url or "").strip()
        key = (self.pmid_to_key.get(pmid) if pmid else None) or (self.doi_to_key.get(doi) if doi else None)
        if not key and not (pmid or doi or url):
            sig = author_year(citation)
            hits = [k for k, e in self.by_key.items() if sig[0] and sig[1] and any(author_year(c) == sig for c in e["citations"])]
            key = hits[0] if len(hits) == 1 else None
        key = key or pmid or doi or url or citation.lower()
        e = self.by_key.setdefault(key, {"key": key, "citations": [], "pmid": "", "doi": "", "url": "", "tags": [],
                                         "files": [], "datasets": defaultdict(int)})
        if citation and citation not in e["citations"]:
            e["citations"].append(citation)
        e["pmid"] = e["pmid"] or pmid
        e["doi"] = e["doi"] or doi
        e["url"] = e["url"] or url or ((doi_or_url or "").strip() if not doi else "")
        for t in tags:
            if t not in e["tags"]:
                e["tags"].append(t)
        e["tags"].sort(key=TAGS.index)
        if file not in e["files"]:
            e["files"].append(file)
        e["datasets"][dataset] += 1
        if pmid:
            self.pmid_to_key[pmid] = key
        if doi:
            self.doi_to_key[doi] = key
        return key

    def lookup(self, pmid_or_doi):
        k = pmid_or_doi.strip().lower()
        key = self.pmid_to_key.get(k) or self.doi_to_key.get(norm_doi(k)) if k else None
        return self.by_key.get(key) if key else None


# ----------------------------------------------------------------------------- multi-outcome rows (inputs 2 and 3)
def build_multi_outcome(cc, class_ids, index):
    rows_out, unparsed, conflicts, n_rows = [], [], [], {}
    for fname in (CPN_FILE, CCS_FILE):
        abbr = ABBR[fname]
        header, rows = parse_table(read(COMBO_NOTES / fname), "## Multi-outcome rows")
        n_rows[fname] = len(rows)
        emo_cols = [h for h in header if h in class_ids]
        for n, r in enumerate(rows, 1):
            if not r["citation"].strip():
                raise SystemExit(f"{fname} row {n}: no citation")
            tags, tag_c = norm_tags(r["verification_tag"])
            index.add(r["citation"], r["pmid"], r["doi_or_url"], tags, fname, "combination_evidence")
            amap = map_activity(cc, r["activity"], f"{fname} row {n}")
            status = {e: cell_status(e, r[e]) for e in emo_cols}
            effects = OrderedDict((e, r[e]) for e in emo_cols if r[e].strip())
            dclass = design_class(r["study_design"])
            for field, col in (("supported", "combination_pairs_supported"), ("not_supported", "pairs_not_supported")):
                ov = cc["pair_overrides"].get((abbr, n, field))
                groups = []
                if ov:
                    for o in ov:
                        if not r["activity"].startswith(o["activity_startswith"]):
                            raise SystemExit(f"combo_pair_overrides.csv: {abbr} {n} no longer starts with {o['activity_startswith']!r}")
                        prs = []
                        for k in [x for x in o["pairs"].split(";") if x]:
                            emos = k.split("+")
                            assert all(e in class_ids for e in emos), (abbr, n, k)
                            prs.append((combo_key(emos), sorted(emos), o["qualifier"], False))
                        groups.append((prs, o))
                else:
                    prs, bad = parse_pairs(r[col], class_ids)
                    if bad:
                        unparsed.append((abbr, n, field, r["activity"], bad, r[col]))
                    groups.append((prs, None))
                for prs, o in groups:
                    for key, emos, qual, proxy in prs:
                        a_ids = amap
                        if o and o["activity_ids"]:
                            a_ids = [tuple(x.split("=")) for x in o["activity_ids"].split(";")]
                        st = [status.get(e, "not_measured") for e in emos]
                        if o and o["outcome"]:
                            outcome = o["outcome"]
                        elif field == "supported":
                            outcome = "both_improved"
                        elif "worsened" in st:
                            outcome = "one_worsened"
                        elif all(s == "not_improved" for s in st):
                            outcome = "neither_improved"
                        else:
                            outcome = "one_not_improved"
                        if field == "supported" and outcome == "both_improved" and not (o and o["outcome"]) and any(s in ("worsened", "not_improved") for s in st):
                            conflicts.append((abbr, n, key, dict(zip(emos, st))))
                        if o and o["evidence_basis"]:
                            basis = o["evidence_basis"]
                        elif dclass in ("meta_analysis", "systematic_review") or re.search(r"pooled|not same sample|narrative", qual + " " + r[col]):
                            basis = "pooled_parallel_outcomes"
                        else:
                            basis = "same_sample_both_outcomes"
                        assert outcome in OUTCOMES and basis in BASES, (abbr, n, outcome, basis)
                        for aid, mtype in (a_ids or [("", "none")]):
                            rows_out.append({
                                "evidence_id": f"{abbr}{n:03d}_{'s' if field == 'supported' else 'n'}_{key}_{aid or 'none'}",
                                "combo_key": key, "emotions": emos, "activity_id": aid, "activity_mapping": mtype,
                                "original_activity_text": r["activity"], "outcome": outcome,
                                "effect_by_emotion": OrderedDict((e, r.get(e, "") or "(see other_dimensions)" if e not in emo_cols else r[e]) for e in emos),
                                "cell_status_by_emotion": OrderedDict((e, status.get(e, "no_column")) for e in emos),
                                "all_dimension_effects": effects, "other_dimensions": r["other_dimensions"],
                                "effect_size_text": "", "finding": "",
                                "pair_listed_as": field, "pair_qualifier": qual, "proxy_constructs": proxy,
                                "study_design": r["study_design"], "design_class": dclass, "n": r["n"], "dose": r["dose"],
                                "population": r["population"], "instrument": r["instrument"],
                                "evidence_basis": basis, "evidence_basis_original": "",
                                "rule_link": "", "rule_link_relation": "", "derived_from_combination": "",
                                "citation": r["citation"], "pmid": norm_pmid(r["pmid"]) or pmid_from_url(r["doi_or_url"]),
                                "doi_or_url": r["doi_or_url"], "verification_tag": "; ".join(tags), "verification_tag_conservative": tag_c,
                                "source_notes_file": fname, "source_row": n, "source_row_id": f"{abbr}{n:03d}",
                                "curation_note": (o["note"] if o else ""),
                            })
    return rows_out, unparsed, conflicts, n_rows


# ----------------------------------------------------------------------------- mixed-state rows (input 4)
def build_mixed_state(cc, class_ids, index):
    header, rows = parse_table(read(COMBO_NOTES / CMX_FILE), "## Combination evidence rows")
    out = []
    for n, r in enumerate(rows, 1):
        if not r["citation"].strip():
            raise SystemExit(f"{CMX_FILE} row {n}: no citation")
        cur = cc["mixed_outcomes"].get(n)
        if cur is None:
            raise SystemExit(f"{CMX_FILE} row {n} ({r['intervention_or_strategy']!r}) has no entry in combo_mixed_outcomes.csv")
        if cur["emotion_combination"] != r["emotion_combination"]:
            raise SystemExit(f"combo_mixed_outcomes.csv row {n}: expected combination {r['emotion_combination']!r}")
        tags, tag_c = norm_tags(r["verification_tag"])
        index.add(r["citation"], r["pmid"], r["doi_or_url"], tags, CMX_FILE, "combination_evidence")
        amap = map_activity(cc, r["intervention_or_strategy"], f"{CMX_FILE} row {n}")
        raw = r["emotion_combination"]
        if raw in GENERAL_KEYS:
            own_key, own_emos = GENERAL_KEYS[raw], []
        elif raw == "stressed+(any negative)":
            own_key, own_emos = "any_negative+stressed", ["stressed"]
        else:
            own_emos = raw.split("+")
            assert all(e in class_ids for e in own_emos), (n, raw)
            own_key = combo_key(own_emos)
        basis = BASIS_FROM_NOTES[r["evidence_basis"]]
        rel = r["supports_or_contradicts_rule"]
        rule_ids = re.findall(r"R\d\d", rel)
        relation = (re.match(r"^(supports|refines|contradicts|new)", rel) or [None, "other"])[1] if rel else ""
        effects = OrderedDict()
        for item in [x for x in cur["effect_by_emotion"].split(";;") if x]:
            e, txt = item.split("=", 1)
            assert e in class_ids, (n, e)
            effects[e] = txt
        keys = []
        if cur["pairs"]:
            for k in cur["pairs"].split(";"):
                emos = k.split("+")
                assert all(e in class_ids for e in emos), (n, k)
                keys.append((combo_key(emos), sorted(emos), ""))
            if len(own_emos) >= 3:
                keys.insert(0, (own_key, sorted(own_emos), ""))
            keys = [(k, e, (own_key if k != own_key and len(own_emos) >= 3 else "")) for k, e, _ in keys]
        else:
            keys = [(own_key, sorted(own_emos), "")]
        outcome = cur["outcome"]
        assert outcome in OUTCOMES, (n, outcome)
        for key, emos, derived in keys:
            for aid, mtype in (amap or [("", "none")]):
                out.append({
                    "evidence_id": f"CMX{n:03d}_{key}_{aid or 'none'}", "combo_key": key, "emotions": emos,
                    "activity_id": aid, "activity_mapping": mtype, "original_activity_text": r["intervention_or_strategy"],
                    "outcome": outcome,
                    "effect_by_emotion": OrderedDict((e, effects.get(e, "")) for e in emos),
                    "cell_status_by_emotion": OrderedDict(), "all_dimension_effects": effects, "other_dimensions": "",
                    "effect_size_text": r["effect_size"], "finding": r["finding"],
                    "pair_listed_as": "combination_row", "pair_qualifier": "", "proxy_constructs": False,
                    "study_design": r["study_design"], "design_class": design_class(r["study_design"]), "n": r["n"],
                    "dose": r["dose"], "population": r["population"], "instrument": "",
                    "evidence_basis": basis, "evidence_basis_original": r["evidence_basis"],
                    "rule_link": ";".join(rule_ids), "rule_link_relation": relation, "derived_from_combination": derived,
                    "citation": r["citation"], "pmid": norm_pmid(r["pmid"]), "doi_or_url": r["doi_or_url"],
                    "verification_tag": "; ".join(tags), "verification_tag_conservative": tag_c,
                    "source_notes_file": CMX_FILE, "source_row": n, "source_row_id": f"CMX{n:03d}",
                    "curation_note": cur["note"],
                })
    return out, len(rows)


def combo_weight(row, W):
    cw = W["combination"]
    return round(cw["verification_tag"][row["verification_tag_conservative"]] * cw["design"][row["design_class"]]
                 * cw["evidence_basis"][row["evidence_basis"]] * cw["mapping"].get(row["activity_mapping"], 0.0), 3)


# ----------------------------------------------------------------------------- prevalence (input 1)
def measure_type(measure, sample):
    m, s = measure.lower(), sample.lower()
    if "% of moments" in m:
        return "percent_of_moments"
    if m.startswith("qualitative"):
        return "qualitative_most_frequent"
    if "within-r" in m:
        return "within_person_r"
    if "shared factor" in m:
        return "shared_factor_loading"
    if "latent profile" in m:
        return "latent_profile_percent"
    if m.startswith("experimental"):
        return "experimental_effect"
    if "pooled r" in m or (m.startswith("r") and "meta-analysis" in s):
        return "pooled_r_meta"
    if "spearman" in m:
        return "spearman_r"
    if m.startswith("r"):
        return "scale_r"
    if m.startswith("%"):
        return "conditional_percent"
    raise SystemExit(f"Unclassified prevalence measure {measure!r}")


def first_number(v):
    t = v.replace("−", "-").replace("–", "-")
    m = re.search(r"-?\d*\.\d+|-?\d+", t)
    if not m:
        return None
    x = m.group(0)
    return float(x if not x.startswith((".", "-.")) else x.replace(".", "0.", 1))


TIER_RANK = {"common": 2, "moderate": 1, "rare_or_unknown": 0}
MEASURE_PRIORITY = ["within_person_r", "pooled_r_meta", "scale_r", "spearman_r", "conditional_percent", "latent_profile_percent",
                    "shared_factor_loading", "qualitative_most_frequent", "experimental_effect", "percent_of_moments"]


def row_tier(mt, v, T):
    if mt in ("within_person_r", "scale_r", "spearman_r", "pooled_r_meta"):
        lo, hi = (T["within_r_moderate_gte"], T["within_r_common_gte"]) if mt == "within_person_r" else (T["r_moderate_gte"], T["r_common_gte"])
        return "common" if v >= hi else "moderate" if v >= lo else "rare_or_unknown"
    if mt in ("conditional_percent", "latent_profile_percent"):
        return "common" if v >= T["percent_common_gte"] else "moderate" if v >= T["percent_moderate_gte"] else "rare_or_unknown"
    return T["by_measure_type"][mt]


def build_prevalence(cc, class_ids, index, T):
    text = read(COMBO_NOTES / PREV_FILE)
    header, rows = parse_table(text, "## Pair prevalence table")
    out = []
    for n, r in enumerate(rows, 1):
        tags, tag_c = norm_tags(r["verification_tag"])
        index.add(r["citation"], r["pmid"], r["doi_or_url"], tags, PREV_FILE, "pair_prevalence")
        emos, groups, order = [], [], []
        for col in ("emotion_a", "emotion_b", "emotion_c"):
            v = r[col].strip()
            if not v:
                continue
            if v in class_ids:
                emos.append(v)
                order.append(v)
            else:
                g = {"(any positive)": "any_positive", "(any negative)": "any_negative"}[v]
                groups.append(g)
                order.append(g)
        mt = measure_type(r["measure"], r["sample & method"])
        val = first_number(r["value"]) if mt not in ("qualitative_most_frequent", "experimental_effect") else None
        tier_cap, extra_note = None, []
        for o in cc["prevalence_overrides"].get(n, []):
            if not r["measure"].startswith(o["measure_startswith"]):
                raise SystemExit(f"prevalence_overrides.csv: row {n} measure no longer starts with {o['measure_startswith']!r}")
            if o["field"] == "extra_emotion":
                assert o["value"] in class_ids
                emos.append(o["value"])
            elif o["field"] == "tier_cap":
                tier_cap = o["value"]
            extra_note.append(f"{o['field']}={o['value']} ({o['reason']})")
        tier = None
        if emos and not groups:
            tier = row_tier(mt, val, T)
            if tier_cap and TIER_RANK[tier] > TIER_RANK[tier_cap]:
                tier = tier_cap
        neg_assoc = mt in ("within_person_r", "scale_r", "spearman_r", "pooled_r_meta") and val is not None and val <= T["negative_r_lte"]
        key = combo_key(emos) if not groups else "+".join(groups)
        pmid = norm_pmid(r["pmid"])
        out.append({
            "prevalence_id": f"PRV{n:03d}", "pair_key": key, "emotions": sorted(emos), "n_emotions": len(emos),
            "listed_order": order, "emotion_a": r["emotion_a"], "emotion_b": r["emotion_b"], "emotion_c": r["emotion_c"],
            "measure": r["measure"], "measure_type": mt, "value": r["value"], "value_numeric": val,
            "value_unit": ("percent" if mt in ("conditional_percent", "latent_profile_percent", "percent_of_moments") else
                           "correlation" if mt.endswith("_r") or mt == "within_person_r" else "loading" if mt == "shared_factor_loading" else ""),
            "row_tier": tier or "", "negatively_associated": neg_assoc,
            "clinical_sample": bool(re.search(r"clinical|MDD|GAD|primary care", r["sample & method"])),
            "sample_and_method": r["sample & method"], "citation": r["citation"], "pmid": pmid,
            "pmid_note": "" if pmid else r["pmid"], "doi_or_url": r["doi_or_url"],
            "verification_tag": "; ".join(tags), "verification_tag_raw": r["verification_tag"],
            "verification_tag_conservative": tag_c, "override_note": "; ".join(extra_note),
            "source_notes_file": PREV_FILE, "source_row": n,
        })
    no_data_listed = parse_no_data_paragraph(text, class_ids)
    return out, no_data_listed


def parse_no_data_paragraph(text, class_ids):
    line = next(l for l in text.split("\n") if l.startswith("**Pairs with no data found:**"))
    pairs = set()
    if "involving **neutral**" in line:
        pairs |= {combo_key([e, "neutral"]) for e in class_ids if e != "neutral"}
    m = re.search(r"\*\*restless\*\* with ([a-z, ]+?) and ([a-z]+)\.", line)
    if m:
        for e in [x.strip() for x in m.group(1).split(",")] + [m.group(2)]:
            assert e in class_ids, e
            pairs.add(combo_key([e, "restless"]))
    for a, b in re.findall(r"([a-z]+)–([a-z]+)", line):
        if a in class_ids and b in class_ids:
            pairs.add(combo_key([a, b]))
    return pairs


def prevalence_summary(prev, class_ids, no_data_listed):
    out = []
    pr = {m: i for i, m in enumerate(MEASURE_PRIORITY)}
    for a, b in combinations(class_ids, 2):
        key = combo_key([a, b])
        rs = [p for p in prev if p["pair_key"] == key]
        best = sorted(rs, key=lambda p: (pr[p["measure_type"]], -(p["value_numeric"] or 0), p["prevalence_id"]))
        tiered = sorted(rs, key=lambda p: (-TIER_RANK[p["row_tier"]], pr[p["measure_type"]], -(p["value_numeric"] or 0), p["prevalence_id"]))
        tier = tiered[0]["row_tier"] if rs else "rare_or_unknown"
        cites = sorted({p["pmid"] or p["citation"] for p in rs})
        b0 = best[0] if rs else None
        t0 = tiered[0] if rs else None
        out.append({
            "pair_key": key, "emotion_a": a, "emotion_b": b,
            "best_measure": b0["measure"] if b0 else "", "best_measure_type": b0["measure_type"] if b0 else "",
            "best_value": b0["value"] if b0 else "", "best_citation": b0["citation"] if b0 else "",
            "best_verification_tag": b0["verification_tag"] if b0 else "",
            "prevalence_tier": tier, "tier_basis_measure": t0["measure"] if t0 else "", "tier_basis_value": t0["value"] if t0 else "",
            "tier_basis_citation": t0["citation"] if t0 else "",
            "n_sources": len(cites), "n_rows": len(rs), "no_data": not rs,
            "negatively_associated": any(p["negatively_associated"] for p in rs),
            "clinical_only": bool(rs) and all(p["clinical_sample"] for p in rs),
            "notes_list_as_no_data": key in no_data_listed,
            "triple_rows_including_pair": sum(1 for p in prev if p["n_emotions"] >= 3 and {a, b} <= set(p["emotions"])),
        })
    return out


# ----------------------------------------------------------------------------- baseline moderation (inputs 2 and 3)
MOD_TYPES = [
    ("floor_effect", r"floor"),
    ("dose_or_duration", r"dose moderator|long-term than short|>20 min"),
    ("no_moderation_found", r"^No moderation|No baseline moderator"),
    ("comparator_matched", r"rest also|≈ quiet rest|as much as|equally"),
    ("baseline_severity", r"higher stress|higher K6|started higher|high trait|higher baseline|lower baseline|not elevated|"
                          r"greater pre-exercise|higher anxiety|high levels of loneliness|elevated|lower pre-exercise|depressive-tendency|lonelier days"),
    ("context", r"thermal|motive|reason"),
    ("subgroup", r"aged|older|altruistic|resilient|cognitive|at-risk|healthy|experience|handler|empathy|stability|mentally ill|adherence|depression more likely"),
]


def build_moderation(cc, class_ids, index):
    out = []
    for fname in (CPN_FILE, CCS_FILE):
        abbr = ABBR[fname]
        header, rows = parse_table(read(COMBO_NOTES / fname), "## Baseline moderation findings")
        for n, r in enumerate(rows, 1):
            tags, tag_c = norm_tags(r["verification_tag"])
            index.add(r["citation"], r["pmid"], "", tags, fname, "baseline_moderation")
            ids = map_activity(cc, r["activity"], f"{fname} moderation row {n}")
            text = r["dimension"] + " || " + r["finding"]
            mtype = next((k for k, p in MOD_TYPES if re.search(p, r["finding"], re.I) or re.search(p, r["dimension"], re.I)), "other")
            emos = [e for e in class_ids if re.search(rf"\b{e}\b", r["dimension"])]
            out.append({
                "moderation_id": f"{abbr}M{n:02d}", "activity": r["activity"], "activity_ids": [a for a, _ in ids],
                "activity_mapping": [m for _, m in ids], "dimension": r["dimension"], "emotion_ids": emos,
                "moderation_type": mtype, "finding": r["finding"], "citation": r["citation"],
                "pmid": norm_pmid(r["pmid"]), "pmid_note": "" if norm_pmid(r["pmid"]) else r["pmid"],
                "verification_tag": "; ".join(tags), "verification_tag_raw": r["verification_tag"],
                "source_notes_file": fname, "source_row": n,
            })
            assert text
    return out


# ----------------------------------------------------------------------------- rule review (input 4)
VERDICTS = [("partly_contradict", r"contradict"), ("refine", r"^refine"), ("confirm_with_additions", r"addition"),
            ("confirm", r"^confirm"), ("no_new_evidence", r"no new evidence")]


def parse_rule_review(index):
    text = read(COMBO_NOTES / CMX_FILE)
    lines = text.split("\n")
    i = lines.index("## Rule review")
    out = OrderedDict()
    for l in lines[i + 1:]:
        if l.startswith("## "):
            break
        m = re.match(r"^- \*\*(R\d\d) (.+?) — (.+?)\.\*\*\s*(.*)$", l)
        if not m:
            continue
        rid, label, vtext, body = m.groups()
        verdict = next(k for k, p in VERDICTS if re.search(p, vtext))
        cites = []
        for lab, url, web in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)(, web)?", body):
            e = index.lookup(norm_doi(url) or pmid_from_url(url))
            cites.append({"citation": lab, "doi_or_url": url, "pmid": e["pmid"] if e else "",
                          "verification_tag": "; ".join(e["tags"]) if e else ("[web]" if web else ""),
                          "found_in_combination_tables": bool(e)})
        out[rid] = {"label": label, "verdict": verdict, "verdict_text": vtext, "text": body, "citations": cites}
    assert list(out) == [f"R{k}" for k in range(10, 28)], list(out)
    return out


def resolve_citation_keys(keys, index):
    out = []
    for k in keys:
        e = index.lookup(k)
        if not e:
            raise SystemExit(f"rules_curated.json: citation key {k!r} is not in the combination notes tables")
        out.append({"citation": max(e["citations"], key=len), "pmid": e["pmid"], "doi": e["doi"],
                    "doi_or_url": ("https://doi.org/" + e["doi"]) if e["doi"] else (f"https://pubmed.ncbi.nlm.nih.gov/{e['pmid']}/" if e["pmid"] else e["url"]),
                    "verification_tag": "; ".join(e["tags"]), "notes_files": e["files"], "source_key": e["key"]})
    return out


# ----------------------------------------------------------------------------- top-level
def build_all(W, class_ids):
    cc = load_combo_curation()
    index = SourceIndex()
    multi, unparsed, conflicts, n_multi = build_multi_outcome(cc, class_ids, index)
    if unparsed:
        msg = "\n".join(f"  {a} row {n} {f}: {act!r}: {bad} (cell: {cell!r})" for a, n, f, act, bad, cell in unparsed)
        raise SystemExit("Unparsed combination pair tokens; add entries to data/curation/combo_pair_overrides.csv:\n" + msg)
    mixed, n_mixed = build_mixed_state(cc, class_ids, index)
    rows = multi + mixed
    for r in rows:
        r["combo_weight"] = combo_weight(r, W) if r["activity_id"] else 0.0
    ids = [r["evidence_id"] for r in rows]
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, dup
    prev, no_data_listed = build_prevalence(cc, class_ids, index, W["prevalence_tiers"])
    summary = prevalence_summary(prev, class_ids, no_data_listed)
    moderation = build_moderation(cc, class_ids, index)
    review = parse_rule_review(index)
    return {"evidence": rows, "conflicts": conflicts, "n_table_rows": {**n_multi, CMX_FILE: n_mixed},
            "prevalence": prev, "prevalence_summary": summary, "no_data_listed": no_data_listed,
            "moderation": moderation, "review": review, "index": index, "curation": cc}


def combo_index(rows, acts, W):
    """Per combination key: activity -> combo score (both_improved, tier-eligible bases), worsened set, row counts.
    Triple keys are added from study rows whose pair rows cover all three pairs with both_improved."""
    cw = W["combination"]
    tier_bases = {"directly_tested_on_combination", "same_sample_both_outcomes", "pooled_parallel_outcomes"}
    by_key = defaultdict(lambda: {"rows": [], "both": defaultdict(list), "worsened": set()})
    for r in rows:
        k = by_key[r["combo_key"]]
        k["rows"].append(r)
        if r["activity_id"] and r["outcome"] == "both_improved" and r["evidence_basis"] in tier_bases:
            k["both"][r["activity_id"]].append(r)
        if r["activity_id"] and r["outcome"] == "one_worsened":
            k["worsened"].add(r["activity_id"])
    # derived triples: same study row + activity, both_improved on all three pairs
    per_row = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        if len(r["emotions"]) == 2 and r["activity_id"] and r["outcome"] == "both_improved" and r["evidence_basis"] in tier_bases:
            per_row[(r["source_row_id"], r["activity_id"])][r["combo_key"]] = r
    for (srid, aid), pairs in sorted(per_row.items()):
        emos = sorted({e for k in pairs for e in k.split("+")})
        for tri in combinations(emos, 3):
            need = [combo_key(p) for p in combinations(tri, 2)]
            if all(n in pairs for n in need):
                base = min((pairs[n] for n in need), key=lambda x: x["combo_weight"])
                tk = combo_key(tri)
                if not any(x["source_row_id"] == srid for x in by_key[tk]["both"][aid]):
                    by_key[tk]["both"][aid].append({**base, "combo_key": tk, "emotions": list(tri), "derived_triple": True})
    out = {}
    for key, k in by_key.items():
        scores = {}
        for aid, rs in k["both"].items():
            studies = {}
            for r in rs:
                sk = r["pmid"] or norm_doi(r["doi_or_url"]) or r["citation"]
                studies[sk] = max(studies.get(sk, 0.0), r["combo_weight"])
            ws = sorted(studies.values(), reverse=True)
            if not ws or ws[0] <= 0:
                continue
            s = min(1.0, ws[0] + cw["corroboration_bonus_per_extra_study"] * sum(ws[1:]))
            bases = {r["evidence_basis"] for r in rs}
            scores[aid] = {"score": round(s, 3), "n_rows": len(rs), "n_studies": len(studies),
                           "direct": "directly_tested_on_combination" in bases,
                           "same_sample": bool(bases & {"directly_tested_on_combination", "same_sample_both_outcomes"}),
                           "best_evidence_id": max(rs, key=lambda x: (x["combo_weight"], x["evidence_id"]))["evidence_id"]}
        out[key] = {"scores": scores, "worsened": sorted(k["worsened"]),
                    "n_rows": len([r for r in k["rows"]]),
                    "n_studies": len({r["pmid"] or norm_doi(r["doi_or_url"]) or r["citation"] for r in k["rows"]})}
    return out
