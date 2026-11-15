#!/usr/bin/env python3
"""Build data/exports/mvp_activity_pack.{json,csv} for the MVP's five sketch classes.

Joins the hand-curated app content in data/curation/mvp_activity_pack.json with the
evidence in data/evidence_links.json, data/activities.json and data/recommendations.json.
Every citation, DOI, PMID and effect size is copied from evidence_links.json; nothing is
written by hand here. Run: python3 scripts/build_mvp_activity_pack.py
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "exports"

VERIFICATION_RANK = {
    "verified_fulltext": 0, "verified_abstract": 1, "corrected": 2,
    "citation_exists_number_not_confirmed": 3, "not_in_pubmed": 4, "not_found": 5, "unverified": 6,
}
VERIFIED = {"verified_fulltext", "verified_abstract", "corrected"}
LEVEL_RANK = {"meta_analysis": 0, "systematic_review": 1, "rct": 2, "experiment": 3, "observational": 4, "indirect": 5}
MAX_CITATIONS = 3


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def short_citation(citation):
    """'de Witte, Spruit, ... 2020, Health Psychology Review' -> 'de Witte et al., 2020'."""
    m = re.search(r"\b(19|20)\d{2}\b", citation)
    year = m.group(0) if m else ""
    authors = citation[: m.start()].strip(" ,(") if m else citation
    first = re.split(r",| & | and ", authors)[0].strip()
    n_authors = len([a for a in re.split(r",| & | and ", authors) if a.strip()])
    if n_authors <= 1:
        return f"{first}, {year}".strip(", ")
    if n_authors == 2:
        second = re.split(r",| & | and ", authors)[1].strip()
        return f"{first} & {second}, {year}".strip(", ")
    return f"{first} et al., {year}".strip(", ")


def evidence_for(links, activity_id, emotions):
    rows = [l for l in links if l["activity_id"] == activity_id and l["emotion_id"] in emotions and l["direction_class"] == "benefit"]
    rows.sort(key=lambda l: (
        0 if l["verification_status"] in VERIFIED else 1,
        LEVEL_RANK.get(l.get("evidence_level_class") or "", 9),
        VERIFICATION_RANK.get(l["verification_status"], 9),
        -(l.get("link_score") or 0),
    ))
    seen, out = set(), []
    for l in rows:
        key = (l.get("pmid") or l.get("doi") or l["citation"]).lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(l)
    return out


def citation_record(l):
    doi = l.get("doi") or ""
    url = l.get("doi_or_url") or (f"https://doi.org/{doi}" if doi else "")
    return {
        "citation": l["citation"],
        "citation_short": short_citation(l["citation"]),
        "doi": doi or None,
        "pmid": l.get("pmid") or None,
        "url": url or None,
        "verification_status": l["verification_status"],
        "evidence_level": l.get("evidence_level_class") or l.get("evidence_level"),
        "evidence_strength": l.get("evidence_strength_class") or l.get("evidence_strength"),
        "outcome_measured": l.get("original_target_emotion"),
        "effect_size": l.get("effect_size"),
        "dose_tested": l.get("dose_tested"),
        "population": l.get("population"),
        "single_session_evidence": l.get("single_session_evidence"),
        "source_link_id": l["link_id"],
    }


def evidence_grade(cits):
    """A: a verified meta-analysis/systematic review/RCT; B: other verified evidence or
    unverified meta-analysis/RCT; C: preliminary, unverified or indirect only."""
    if not cits:
        return "none"
    def strong_design(c):
        return (c["evidence_level"] or "") in ("meta_analysis", "systematic_review", "rct")
    if any(c["verification_status"] in VERIFIED and strong_design(c) for c in cits):
        return "A"
    if any(c["verification_status"] in VERIFIED or strong_design(c) for c in cits):
        return "B"
    return "C"


def main():
    cur = load("curation/mvp_activity_pack.json")
    acts = {a["id"]: a for a in load("activities.json")["activities"]}
    links = load("evidence_links.json")
    links = links["links"] if isinstance(links, dict) else links
    recs = load("recommendations.json")["by_emotion"]
    safety = load("safety.json")
    never = set(safety.get("never_suggest_activity_ids", []))
    class_emotions = cur["meta"]["class_to_dataset_emotions"]
    fallbacks = cur["meta"]["fallback_aggregate_targets"]
    classes = list(cur["classes"])

    emotion_to_classes = {}
    for c, ems in class_emotions.items():
        for e in ems:
            emotion_to_classes.setdefault(e, []).append(c)

    out_classes, flat_rows, problems = {}, [], []
    for cls in classes:
        spec = cur["classes"][cls]
        items = []
        for rank, item in enumerate(spec["activities"], start=1):
            aid = item["activity_id"]
            a = acts.get(aid)
            if a is None:
                problems.append(f"{cls}: unknown activity {aid}")
                continue
            if aid in never or not a["suggestable"] or a["suggest_mode"] != "right_now":
                problems.append(f"{cls}: {aid} is not suggestable right now")
                continue
            contra_emotions = [c["id"] for c in a.get("contraindicated_for", []) if c.get("kind") == "emotion"]
            contraindicated = sorted({c for e in contra_emotions for c in emotion_to_classes.get(e, [])})
            if cls in contraindicated:
                problems.append(f"{cls}: {aid} is contraindicated for this class")
                continue

            ev = evidence_for(links, aid, class_emotions[cls])
            evidence_basis = "direct"
            if not ev and fallbacks.get(cls):
                ev = evidence_for(links, aid, fallbacks[cls])
                evidence_basis = "aggregate_outcome" if ev else "none"
            elif not ev:
                evidence_basis = "none"
            cits = [citation_record(l) for l in ev[:MAX_CITATIONS]]
            if not cits:
                problems.append(f"{cls}: {aid} has no benefit evidence for {class_emotions[cls]}")

            score = max((x["evidence_score"] for e in class_emotions[cls] for x in recs.get(e, {}).get("recommended", []) if x["activity_id"] == aid), default=None)
            also = []
            for other in classes:
                if other == cls:
                    continue
                if evidence_for(links, aid, class_emotions[other]):
                    also.append(other)

            dose_gap = None
            if item.get("short_version_seconds"):
                dose_gap = (f"The {item['short_version_seconds']}-second version is shorter than the tested dose "
                            f"(typical {a['typical_duration_min']} min); present it as a taster.")

            record = {
                "id": aid,
                "class": cls,
                "rank_in_class": rank,
                "default_three": rank <= 3,
                "title": item["title"],
                "subtitle": item["subtitle"],
                "interaction_type": item["interaction_type"],
                "duration_seconds": item["duration_seconds"],
                "short_version_seconds": item.get("short_version_seconds"),
                "steps": item["steps"],
                **({"pacer": item["pacer"]} if "pacer" in item else {}),
                **({"canvas_template": item["canvas_template"]} if "canvas_template" in item else {}),
                "category": a["category"],
                "effort": a["effort"],
                "arousal_effect": a["arousal_effect"],
                "preference_tags": a["preference_tags"],
                "requirements": [r for r in a["requirements"] if r != "none"],
                "evidence": {
                    "basis": evidence_basis,
                    "grade": evidence_grade(cits),
                    "dataset_evidence_score": score,
                    "evidence_dose": a.get("min_effective_dose"),
                    "dose_gap_note": dose_gap,
                    "citations": cits,
                },
                "also_supports_classes": also,
                "contraindicated_classes": contraindicated,
                "cautions": a["cautions"][:3],
            }
            items.append(record)
            top = cits[0] if cits else {}
            flat_rows.append({
                "class": cls, "rank_in_class": rank, "default_three": rank <= 3, "id": aid,
                "title": item["title"], "subtitle": item["subtitle"], "interaction_type": item["interaction_type"],
                "duration_seconds": item["duration_seconds"], "short_version_seconds": item.get("short_version_seconds") or "",
                "evidence_grade": record["evidence"]["grade"], "evidence_basis": evidence_basis,
                "top_citation": top.get("citation", ""), "top_citation_doi": top.get("doi") or "",
                "top_citation_pmid": top.get("pmid") or "", "top_citation_verification": top.get("verification_status", ""),
                "top_effect_size": top.get("effect_size") or "", "n_citations": len(cits),
                "also_supports_classes": ";".join(also), "cautions": " | ".join(a["cautions"][:2]),
            })
        out_classes[cls] = {"framing": spec["framing"], "dataset_emotions": class_emotions[cls], "activities": items}

    if problems:
        raise SystemExit("Pack has problems:\n  " + "\n  ".join(problems))

    n_unique = len({r["id"] for r in flat_rows})
    pack = {
        "meta": {
            "title": "MVP activity pack: evidence-backed activities for the five sketch classes",
            "generated_by": "scripts/build_mvp_activity_pack.py",
            "sources": ["data/curation/mvp_activity_pack.json", "data/evidence_links.json", "data/activities.json", "data/recommendations.json", "data/safety.json"],
            "classes": classes,
            "class_to_dataset_emotions": class_emotions,
            "counts": {"class_activity_rows": len(flat_rows), "unique_activities": n_unique},
            "how_to_use": [
                "Each class lists activities in recommended order; the first three (default_three) are the suggested replacement for the current fixed list.",
                "Show title, subtitle and duration; render steps with the given interaction_type; show citations[0].citation_short behind a 'Why this?' link.",
                "Do not suggest any activity whose contraindicated_classes contains the sketch's class (none do in this pack) or any id in never_suggest_activity_ids.",
                "Citations are copied from the research dataset. verification_status says how far each was checked: verified_fulltext/verified_abstract/corrected were confirmed against PubMed; others were not.",
            ],
            "evidence_grade_definition": "A = at least one meta-analysis, systematic review or RCT confirmed against PubMed; B = other confirmed evidence, or an unconfirmed meta-analysis/RCT; C = preliminary, unconfirmed or indirect only.",
            "important_caveats": [
                "Most tested doses are 5-30 minutes. The 60-90 second MVP format is shorter than any tested dose for most activities; treat short versions as tasters.",
                "calm_flow and radiant_joy are positive states: the activities help savour or share them, not fix anything. Make them optional.",
                "The sketch scores are not a validated measure of emotion. Use these activities as suggestions the person can decline.",
                "Not medical advice. Crisis and blocked results must still skip activities.",
            ],
            "interaction_types": cur["meta"]["interaction_types"],
            "duration_note": cur["meta"]["duration_note"],
        },
        "never_suggest_activity_ids": sorted(never),
        "existing_mvp_activity_notes": cur["existing_mvp_activity_notes"],
        "classes": out_classes,
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "mvp_activity_pack.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (OUT / "mvp_activity_pack.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(flat_rows[0]), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(flat_rows)

    print(f"rows {len(flat_rows)}, unique activities {n_unique}")
    for cls in classes:
        grades = [a["evidence"]["grade"] for a in out_classes[cls]["activities"]]
        print(f"  {cls:15} {len(grades)} activities, grades {''.join(grades)}, default: {[a['id'] for a in out_classes[cls]['activities'][:3]]}")


if __name__ == "__main__":
    main()
