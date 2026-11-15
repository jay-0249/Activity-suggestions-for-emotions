# Activity suggestions for emotions

Research-backed mapping from emotions (and emotion combinations) to suggested activities, for a wellbeing app that reads a short drawing/handwriting check-in.

## Where to start

| Path | What it is |
|---|---|
| `reports/Emotion to activity evidence map.md` | The written report: findings, per-emotion and combination tables, validity of the drawing signal, guardrails |
| `reports/Emotion combination evidence map.md` | The combination report: which emotions co-occur, same-sample and mixed-state evidence, rule review, new cluster rules |
| `checkin/` | Reflective check-in design: flow, vision-model system prompt, output schema, and a tested reference decision engine over `data/` |
| `data/schema.md` | Data dictionary, evidence-score and combo-score formulas, prevalence tiers, decision pseudo-code, two worked examples |
| `data/emotions.json` | 12 emotion classes with valence/arousal and label synonyms |
| `data/activities.json` | 109 activities with instructions, duration, preference tags, cautions |
| `data/evidence_links.csv` / `.json` | 331 activity–emotion evidence links with effect size, dose, citation, DOI, PMID, verification status |
| `data/recommendations.json` | Ranked activities per emotion, with avoid lists |
| `data/combination_rules.json` | 38 matching rules: R01–R30 with rule-review verdicts and revisions, plus R31–R38 for clusters and triples |
| `data/combination_matrix.csv`, `data/combination_triples.csv` | All 66 emotion pairs and 18 common triples/clusters, with prevalence tier and combination evidence ranked first |
| `data/combination_evidence.csv` / `.json` | 377 rows of same-sample, mixed-state and pooled evidence: one row per study row × emotion combination × activity |
| `data/pair_prevalence.csv` / `.json`, `data/pair_prevalence_summary.csv` | 71 co-occurrence rows and a 66-pair summary with prevalence tier |
| `data/baseline_moderation.csv` | 40 findings on whether an activity helps more when the state starts higher |
| `data/safety.json` | Crisis gate, disclaimers, wording |
| `data/sources.csv` | 471 deduplicated sources with verification status and combination-notes tags |
| `data/verification/` | Per-citation PubMed verification logs |
| `data/curation/` | Hand-curated inputs to the build (mappings, score weights) |
| `research_notes/` | Raw research notes per topic, each ending with a verification log |
| `scripts/build_dataset.py` | Rebuilds everything in `data/` from the notes: `python3 scripts/build_dataset.py` (uses `combination_build.py` and `schema_template.py`) |

## Read before using the data

- **Verification.** About 68% of evidence links were confirmed against the PubMed abstract or full text. The rest are flagged in `verification_status` (mostly papers PubMed does not index) and should not be quoted as established numbers.
- **Combinations are still mostly extrapolated.** Few studies test an emotion pair as a pair. In the 66-pair matrix, 22 rows have at least one suggestion backed by same-sample or direct combination evidence (4 direct, 18 same-sample); the other 44 are composed from single-emotion evidence or the notes' rules and are labelled as such. Most combination evidence comes from multi-week programmes, not 5–30 minute sessions.
- **Tags.** Combination rows carry the notes' verification tags (`[PM-full]`, `[PM-abs]`, `[prior-notes]`, `[web]`, `[memory]`); treat `[web]` and `[memory]` values as unverified.
- **Scores and thresholds are uncalibrated.** The evidence-score weights and the 0.4 / 0.75 / 0.9 thresholds are engineering defaults, not empirical values.
- **The drawing signal is weak.** No peer-reviewed study validates inferring current mood from a short drawing or from a vision model. The report recommends that a one-tap self-report drives the suggestion and the AI reading is shown as a correctable guess.
- **Not medical advice.** This is a general-wellness dataset, not a diagnostic or treatment tool.
