# Activity suggestions for emotions

Research-backed mapping from emotions (and emotion combinations) to suggested activities, for a wellbeing app that reads a short drawing/handwriting check-in.

## Where to start

| Path | What it is |
|---|---|
| `reports/Emotion to activity evidence map.md` | The written report: findings, per-emotion and combination tables, validity of the drawing signal, guardrails |
| `data/schema.md` | Data dictionary, evidence-score formula, decision pseudo-code, worked example |
| `data/emotions.json` | 12 emotion classes with valence/arousal and label synonyms |
| `data/activities.json` | 105 activities with instructions, duration, preference tags, cautions |
| `data/evidence_links.csv` / `.json` | 331 activity–emotion evidence links with effect size, dose, citation, DOI, PMID, verification status |
| `data/recommendations.json` | Ranked activities per emotion, with avoid lists |
| `data/combination_rules.json`, `data/combination_matrix.csv` | 30 matching rules and 34 emotion pairs |
| `data/safety.json` | Crisis gate, disclaimers, wording |
| `data/sources.csv` | 311 deduplicated sources with verification status |
| `data/verification/` | Per-citation PubMed verification logs |
| `data/curation/` | Hand-curated inputs to the build (mappings, score weights) |
| `research_notes/` | Raw research notes per topic, each ending with a verification log |
| `scripts/build_dataset.py` | Rebuilds everything in `data/` from the notes: `python3 scripts/build_dataset.py` |

## Read before using the data

- **Verification.** About 68% of evidence links were confirmed against the PubMed abstract or full text. The rest are flagged in `verification_status` (mostly papers PubMed does not index) and should not be quoted as established numbers.
- **Combinations are mostly extrapolated.** Almost no study tests an emotion pair as a pair; 31 of 34 matrix rows are composed from single-emotion evidence and are labelled as such.
- **Scores and thresholds are uncalibrated.** The evidence-score weights and the 0.4 / 0.75 / 0.9 thresholds are engineering defaults, not empirical values.
- **The drawing signal is weak.** No peer-reviewed study validates inferring current mood from a short drawing or from a vision model. The report recommends that a one-tap self-report drives the suggestion and the AI reading is shown as a correctable guess.
- **Not medical advice.** This is a general-wellness dataset, not a diagnostic or treatment tool.
