# Verification of the "Predicting Human Characteristics Through Drawings Using AI" brief

Checked 14 November 2026 against primary records: PubMed abstracts (E-utilities), PMC full text, and arXiv abstract pages. Tags: **[PM-abs]** PubMed abstract, **[PM-full]** PMC full text, **[arXiv]** arXiv abstract page, **[repo]** repository README, **[web]** search snippet only, **[not checked]**.

## Claim-by-claim

| # | Brief's claim | Result | Source checked |
|---|---|---|---|
| 1 | EMOTHAW: 129 participants, 7 tasks, tablet records position/time/pressure/azimuth/altitude, on-paper and in-air; random forest | **Confirmed.** Accuracy 60–71% across the three states | arXiv 2202.12245 [arXiv] |
| 2 | EMOTHAW: "stronger performance for anxiety and stress than depression" | **Not confirmed.** Not in the arXiv abstract; the IEEE full text is not reachable. The later Nolazco-Flores 2022 three-class results run the other way (depression 82.5%, anxiety 72.8%, stress 74.56%) | arXiv 2202.12245; PMID 35214585 [PM-abs] |
| 3 | EMOTHAW participants right-handed university students aged 21–32 | **Confirmed.** 71 F / 58 M, one Italian university | PMC8875261 [PM-full] |
| 4 | Nolazco-Flores 2021, IEEE Access, DOI 10.1109/ACCESS.2021.3058443, SVM, leave-one-out | **Citation confirmed** (IEEE Access 9:28496–28504) via a reference list. Method and results **not checked**. The 2022 follow-up (Sensors, PMID 35214585) used leave-percentage-out, Gaussian-noise augmentation and AutoML, and reports "100%" two-class accuracy on the same 129 people | PMC8875261 [PM-full]; PMID 35214585 [PM-abs] |
| 5 | Guo et al. 2023 HTP meta-analysis: 30 studies, 6,295 participants, 39 significant characteristics, non-uniform methods | **Confirmed.** Front Psychiatry 13:1041770, online 4 Jan 2023 (volume 2022). 50 characteristics appeared ≥3 times, of which 39 were significant; ORs 2.16–4.20 by dimension. These are case–control associations, not individual-level prediction | PMID 36683989 [PM-abs] |
| 6 | 2026 tree-drawing meta-analysis: 42 studies, 8,552 participants | **Confirmed.** Guo et al., *Depression and Anxiety* 2026:9571222 (the brief omits the journal). Studies span 1948–2024. 24 significant characteristics (ORs 2.01–7.07). Again associations, not prediction | PMID 42437128 [PM-abs] |
| 7 | Lin et al. 2022: 4,196 children/adolescents; DNNs learned features but could not separate depressed from non-depressed | **Confirmed.** Also: a summary of previous HTP indicators found "no reliable association" with mental-health problems | PMID 36058187 [PM-abs] |
| 8 | AuDrA: four datasets, ~60 raters, >13,000 drawings; r 0.80 falling to 0.49 under new task + new raters | **Confirmed.** Table 1: held-out test r = .80; new raters .76 and .65; new task + new raters .49. Behav Res Methods 2024;56:3619–3636 | PMID 37919616 [PM-abs]; PMC11133150 [PM-full] |
| 9 | Drawings of THINGS: 28,627 drawings, 1,314 participants, 1,854 concepts; stroke history, demographics, drawing ability, imagery | **Confirmed.** Behav Res Methods 58(2):57, 2026. Recruited on Prolific | PMID 41618073 [PM-abs]; PMC12858628 [PM-full] |
| 10 | DARWIN: 174 participants, 451 features, Alzheimer's vs control | **Search-level only.** 89 patients / 85 controls; 25 tasks × 18 features = 450 (451 likely includes an ID). UCI is blocked here; the paper's venue was not confirmed | [web] |
| 11 | KIDO: 5,430 drawings with children's written happy/sad reflections; Çiftçi 2025 IEEE Access | **Search-level only.** IEEE Access 13:159730–159748. Reported F1 up to 79% from drawings vs accuracy up to 97% from the children's written text. Hugging Face is blocked here | [web] |
| 12 | ArtCognition HTP dataset: small sample, preprint | **Confirmed.** 146 samples from a browser drawing app; arXiv 2601.04297 (Jan 2026), not peer reviewed. The abstract claims "significant correlations" but gives no numbers, and grounds interpretation by retrieving HTP interpretive literature — the indicators Lin 2022 found unreliable | arXiv 2601.04297 [arXiv]; repo README [repo] |
| 13 | Jev: announced Sept 2026; architecture and training data undisclosed; the preprint studies open typed-decision models, not Jev on drawings | **Confirmed.** Rastogi, arXiv 2611.15592 (11 Nov 2026). Additional point: these models "answer structured questions about a piece of text" — text in, typed decision out | arXiv 2611.15592 [arXiv] |
| 14 | Jev probabilities "calibrated" — not established | **Confirmed as open.** An audit of five open Jev-style models (arXiv 2611.12521, not Jev itself) found the reported confidence is a closed-form function of the output distribution's spread, not of empirical accuracy, and that bundling several questions in one request flipped 11.7–22.4% of binary answers on a 0.8B model (0.1–0.2% on 4B) | arXiv 2611.12521 [arXiv] |
| 15 | Quick, Draw!: 50 million timestamped vector drawings, CC BY 4.0 | **Not checked** | — |

## What the brief leaves out

- Graphology meta-analyses (Neter & Ben-Shakhar 1989; Dazzi & Pedrabissi 2009) — the null baseline for reading personality or state from handwriting.
- Damiano et al. 2023, *Journal of Vision* — the closest evidence for "draw how you feel": colour drawings of a named emotion by non-artists were classified at 50.81% vs 16.7% chance; line-only drawings at about 23–25%.
- Browser input limits: on hardware without pressure sensing, Pointer Events report a constant 0.5 pressure, so finger drawings in a PWA cannot supply the pressure features EMOTHAW used.
- Task length: EMOTHAW tasks are full copy and drawing tasks with a pen; nothing tested a 5–30-second finger drawing.

## Still needs reverification

1. EMOTHAW per-state accuracies (IEEE full text).
2. Nolazco-Flores 2021 method and results (IEEE Access full text).
3. DARWIN paper venue and feature count (UCI page / paper).
4. KIDO counts and F1 figures (paper / Hugging Face card).
5. Quick, Draw! size and licence (GitHub README).
6. ArtCognition effect sizes (full text).
7. Whether Jev accepts images at all (TypeSafe documentation); the preprints describe text input only.
