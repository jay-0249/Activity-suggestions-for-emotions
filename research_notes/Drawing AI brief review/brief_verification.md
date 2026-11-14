# Verification of the "Predicting Human Characteristics Through Drawings Using AI" brief

Checked 14 November 2026 against primary records: PubMed abstracts (E-utilities), PMC full text, arXiv abstracts and full-text PDFs, the UCI and Hugging Face dataset pages, and the GitHub READMEs. Second pass the same day, after IEEE, Hugging Face, UCI and GitHub hosts were allowed. Tags: **[PM-abs]** PubMed abstract, **[PM-full]** PMC full text, **[arXiv]** arXiv abstract, **[arXiv-full]** arXiv full text, **[dataset]** official dataset page or README, **[web]** search snippet only.

## Claim-by-claim

| # | Brief's claim | Result | Source checked |
|---|---|---|---|
| 1 | EMOTHAW: 129 participants, 7 tasks, tablet records position, time, pressure, azimuth, altitude, on-paper and in-air; random forest | **Confirmed.** Accuracy 60–71% | arXiv 2202.12245 [arXiv-full] |
| 2 | EMOTHAW: "stronger performance for anxiety and stress than depression" | **Wrong.** Table 3: depression 71.2%, anxiety 60%, stress 60.2% (10 repetitions of leave-one-out cross-validation). The paper says "Depression recognition performs the best." Labels are DASS-42 scores for the past week, not the current moment | arXiv 2202.12245 [arXiv-full] |
| 3 | EMOTHAW participants right-handed university students aged 21–32 | **Confirmed.** 71 F / 58 M, one Italian university | PMC8875261 [PM-full] |
| 4 | Nolazco-Flores 2021, IEEE Access, SVM, leave-one-out | **Partly confirmed.** IEEE Access 9:28496–28504, open access. Search summaries describe FCBF feature selection, Gaussian-noise augmentation of the same 129 people, RBF-SVM and leave-one-out; per-state numbers **not read**. The 2022 follow-up reports "100%" two-class accuracy with the same augmentation approach | Reference list in PMC8875261 [PM-full]; [web]; PMID 35214585 [PM-abs] |
| 5 | Guo et al. 2023 HTP meta-analysis: 30 studies, 6,295 participants, 39 significant characteristics, non-uniform methods | **Confirmed.** Front Psychiatry 13:1041770 (online 4 Jan 2023). 50 characteristics appeared at least 3 times; 39 significant; ORs 2.16–4.20 by dimension. Case–control associations, not individual prediction | PMID 36683989 [PM-abs] |
| 6 | 2026 tree-drawing meta-analysis: 42 studies, 8,552 participants | **Confirmed.** Guo et al., *Depression and Anxiety* 2026:9571222; studies from 1948–2024; 24 significant characteristics (ORs 2.01–7.07). Associations, not prediction | PMID 42437128 [PM-abs] |
| 7 | Lin et al. 2022: 4,196 children and adolescents; DNNs could not separate depressed from non-depressed | **Confirmed.** A summary of prior HTP indicators also found "no reliable association" with mental-health problems | PMID 36058187 [PM-abs] |
| 8 | AuDrA: 4 datasets, about 60 raters, over 13,000 drawings; r falls from .80 to .49 | **Confirmed.** Table 1: held-out test .80; new raters .76 and .65; new task + new raters .49 | PMID 37919616 [PM-abs]; PMC11133150 [PM-full] |
| 9 | Drawings of THINGS: 28,627 drawings, 1,314 participants, 1,854 concepts | **Confirmed.** Behav Res Methods 58(2):57, 2026; recruited on Prolific | PMID 41618073 [PM-abs]; PMC12858628 [PM-full] |
| 10 | DARWIN: 174 participants, 451 features, Alzheimer's vs control | **Confirmed.** UCI: 174 instances, 451 features (the first is the participant ID), CC BY 4.0. Introductory paper: Cilia, De Gregorio, De Stefano, Fontanella, Marcelli & Parziale 2022, *Engineering Applications of Artificial Intelligence*. The 89 / 85 split is from secondary sources | UCI dataset page [dataset]; [web] |
| 11 | KIDO: 5,430 drawings with children's written happy/sad reflections; Çiftçi 2025 IEEE Access | **Confirmed.** Dataset card: 5,430 scanned drawings, each with the child's written reflection (Turkish and English) labelling it happiness or sadness, plus education level and gender. IEEE Access 13:159730–159748. The F1 (up to 79.03% from drawings) and accuracy (up to 97.47% from text) figures are **search-level only** | Hugging Face card; GitHub README [dataset]; [web] |
| 12 | ArtCognition: small sample, preprint | **Confirmed, and weaker than the abstract suggests.** 146 samples; only 21 completed the questionnaire; one cultural group; no pen pressure. The full text gives **no correlation coefficients**: agreement with the Beck Anxiety and Depression Inventories is described qualitatively. It reports that a plain Gemini 2 Flash baseline made unsupported interpretive claims about 45.7% of the time | arXiv 2601.04297 [arXiv-full]; repo README [dataset] |
| 13 | Jev: announced September 2026; architecture and training data undisclosed; preprint studies open models, not Jev on drawings | **Confirmed.** Rastogi, arXiv 2611.15592. Those models answer structured questions "about a piece of text" | arXiv 2611.15592 [arXiv] |
| 14 | Jev's image input needs verifying | **Partly resolved, from secondary sources.** Jev 1.14 (released 14 Oct 2026) reportedly accepts PNG and JPEG behind a "danger zone" opt-in header, labelled experimental and not for production, with lower performance than text input; earlier versions are described as text-only. TypeSafe's own documentation was not reached | [web] |
| 15 | Jev probabilities "calibrated" — not established | **Confirmed as open.** An audit of five open Jev-style models (not Jev) found reported confidence is a closed-form function of how spread out the output distribution is, not of empirical accuracy. Bundling several questions in one request flipped 11.7–22.4% of binary answers on a 0.8B model (0.1–0.2% on 4B) | arXiv 2611.12521 [arXiv] |
| 16 | Quick, Draw!: 50 million timestamped vector drawings, CC BY 4.0 | **Confirmed.** 50 million drawings across 345 categories, timestamped vectors with country metadata | GitHub README [dataset] |

## What the brief leaves out

- Graphology meta-analyses (Neter & Ben-Shakhar 1989; Dazzi & Pedrabissi 2009): the null baseline for reading personality or state from handwriting.
- Damiano et al. 2023, *Journal of Vision*: colour drawings of a named emotion by non-artists were classified at 50.81% against 16.7% chance; line-only drawings at about 23–25%.
- Browser input limits: on hardware without pressure sensing, Pointer Events report a constant 0.5, so finger drawings in a PWA cannot supply EMOTHAW's pressure features.
- Task length: EMOTHAW tasks are full pen tasks (one clock drawing took 8.7–36.8 s on paper). Nothing tested a 5–30 second finger drawing.

## Still open

1. Nolazco-Flores 2021 per-state results: the open-access PDF is on iris.unicampania.it; downloading it was blocked by this session's permission settings.
2. KIDO F1 and accuracy figures: the IEEE Xplore full text could not be retrieved (automated download was blocked).
3. Jev image support: confirm against TypeSafe's official multimodal documentation.
