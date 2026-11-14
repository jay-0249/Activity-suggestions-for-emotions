# Verification of the "Predicting Human Characteristics Through Drawings Using AI" brief

Checked 14 November 2026 against primary records: PubMed abstracts (E-utilities), PMC full text, arXiv abstracts and full-text PDFs, the UCI and Hugging Face dataset pages, and the GitHub READMEs. Second pass the same day, after IEEE, Hugging Face, UCI and GitHub hosts were allowed. Third pass using full-text PDFs supplied by the user (EMOTHAW journal version, Nolazco-Flores 2021, DARWIN, KIDO). Tags: **[PM-abs]** PubMed abstract, **[PM-full]** PMC full text, **[arXiv]** arXiv abstract, **[arXiv-full]** arXiv full text, **[dataset]** official dataset page or README, **[web]** search snippet only.

## Claim-by-claim

| # | Brief's claim | Result | Source checked |
|---|---|---|---|
| 1 | EMOTHAW: 129 participants, 7 tasks, tablet records position, time, pressure, azimuth, altitude, on-paper and in-air; random forest | **Confirmed.** Accuracy 60–71% | arXiv 2202.12245 [arXiv-full] |
| 2 | EMOTHAW: "stronger performance for anxiety and stress than depression" | **Confirmed, with a caveat that matters.** Table III: depression has the highest accuracy (71.2%) but only **12.6% sensitivity** (specificity 92.2%), so it mostly predicts "not depressed". Anxiety: 60% accuracy, 45% sensitivity, 71% specificity. Stress: 60.2%, 41%, 74.5%. The paper says anxiety and stress "perform better than depression recognition" in ROC space. My earlier correction, which called the brief wrong on accuracy alone, is withdrawn. Labels are DASS-42 scores for the past week | IEEE journal full text (uploaded PDF) |
| 3 | EMOTHAW participants right-handed university students aged 21–32 | **Confirmed.** 71 F / 58 M, one Italian university | PMC8875261 [PM-full] |
| 4 | Nolazco-Flores 2021, IEEE Access, SVM, leave-one-out | **Confirmed.** RBF-SVM, FCBF feature selection, leave-one-out, with training data augmented by adding small Gaussian noise to a random 20% of samples. Table 4, best ("Max") accuracy per setting: depression 76.64% average (writing 80.31%), anxiety 69.29%, stress 68.5%; overall 71.47% vs a 61.97% baseline. **Caveats:** only accuracy is reported (no sensitivity or specificity, which matters given the 12.6% depression sensitivity above); filter-bank and threshold settings were tuned on the same leave-one-out accuracy that is reported, so the figures are optimistic; same 129 people, no external test | IEEE Access full text (uploaded PDF) |
| 5 | Guo et al. 2023 HTP meta-analysis: 30 studies, 6,295 participants, 39 significant characteristics, non-uniform methods | **Confirmed.** Front Psychiatry 13:1041770 (online 4 Jan 2023). 50 characteristics appeared at least 3 times; 39 significant; ORs 2.16–4.20 by dimension. Case–control associations, not individual prediction | PMID 36683989 [PM-abs] |
| 6 | 2026 tree-drawing meta-analysis: 42 studies, 8,552 participants | **Confirmed.** Guo et al., *Depression and Anxiety* 2026:9571222; studies from 1948–2024; 24 significant characteristics (ORs 2.01–7.07). Associations, not prediction | PMID 42437128 [PM-abs] |
| 7 | Lin et al. 2022: 4,196 children and adolescents; DNNs could not separate depressed from non-depressed | **Confirmed.** A summary of prior HTP indicators also found "no reliable association" with mental-health problems | PMID 36058187 [PM-abs] |
| 8 | AuDrA: 4 datasets, about 60 raters, over 13,000 drawings; r falls from .80 to .49 | **Confirmed.** Table 1: held-out test .80; new raters .76 and .65; new task + new raters .49 | PMID 37919616 [PM-abs]; PMC11133150 [PM-full] |
| 9 | Drawings of THINGS: 28,627 drawings, 1,314 participants, 1,854 concepts | **Confirmed.** Behav Res Methods 58(2):57, 2026; recruited on Prolific | PMID 41618073 [PM-abs]; PMC12858628 [PM-full] |
| 10 | DARWIN: 174 participants, 451 features, Alzheimer's vs control | **Confirmed.** 89 Alzheimer's patients and 85 healthy controls; 25 tasks × 18 features (the UCI file adds an ID column). Cilia et al. 2022, *Engineering Applications of Artificial Intelligence*, doi 10.1016/j.engappai.2022.104822. Best result: an SVM combining five tasks reached 94.28% accuracy, 88.24% specificity, 100% sensitivity. This is a diagnosis task (Alzheimer's), not mood | Paper full text (uploaded PDF); UCI page |
| 11 | KIDO: 5,430 drawings with children's written happy/sad reflections | **Corrected.** **10,860 drawings from 5,430 students** (2,715 primary, 2,715 secondary; 27 schools in Şanlıurfa, Turkey). Each child was **told** to draw happiness, then sadness, and wrote why the drawing showed that emotion. The labels are the instructed emotion, not the child's mood. Drawings: F1 up to 79.03%; written reflections: accuracy up to 97.47% (the reflections describe the instructed emotion, so text is the easier task). 85/15 train/test split; the paper does not say the split kept each child's two drawings together | IEEE Access full text (uploaded PDF) |
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

1. Jev image support: confirm against TypeSafe's official multimodal documentation.

## What the full texts change for the app

- EMOTHAW, the strongest mood-from-handwriting dataset, finds about 4 in 10 anxious or stressed people and about 1 in 8 depressed people, with a pen tablet, full-length tasks and past-week labels.
- KIDO and Damiano 2023 both test drawing an *instructed* emotion. That supports a "draw how you feel" prompt where the person chooses the feeling, not hidden-mood detection.
- In KIDO, the child's own words carried far more signal than the drawing, which supports asking for a word or one-tap label alongside the drawing.
