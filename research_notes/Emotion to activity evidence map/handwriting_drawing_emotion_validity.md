# Scientific validity of inferring emotional state from handwriting or a short drawing

**Verification note (read first).** Direct page fetches to pmc.ncbi.nlm.nih.gov, arxiv.org, doaj.org and artificialintelligenceact.eu were blocked by this session's network allowlist, so no primary full text could be opened. Every number below was confirmed only at abstract / repository-record / search-snippet level unless stated otherwise. Tags used:

- **[V-abs]** = confirmed against the abstract or a publisher/repository record surfaced in search.
- **[V-sec]** = confirmed only through a secondary source (press release, law-firm note, citing paper). Check the original before putting it on a slide.
- **[MEM]** = bibliographic detail or DOI supplied from the researcher's memory, not re-opened in this session. Treat as unverified until clicked.
- **Verdict scale:** pseudoscience / weak / promising-but-preliminary / well-supported.

---

## 1. Graphology: can handwriting features reveal personality or psychological state?

### Takeaway
Graphology (reading character or disposition from slant, size, loops, etc.) is **pseudoscience**: every systematic review located finds validity at or near zero, and graphologists do no better than laypeople. The app must not use, or prompt an LLM to use, graphological rules ("large letters = extraversion", "heavy pressure = anger").

### Cited Findings
- Neter & Ben-Shakhar (1989) meta-analysed 17 studies: 63 graphologists and 51 non-graphologists rated 1,223 scripts; graphologists were no better than non-graphologists at predicting job performance. [V-abs] — [Hebrew University research record](https://cris.huji.ac.il/en/publications/the-predictive-validity-of-graphological-inferences-a-meta-analyt/); DOI [MEM] 10.1016/0191-8869(89)90021-3
- Dean (1992) reviewed roughly 200 studies and found only a small effect size for inferring personality from handwriting, with mean inter-rater agreement among graphologists of about r = .42; no school of graphology outperformed another. [V-sec, via King & Koehler and Wikipedia-derived summaries] — [Wikipedia: Graphology](https://en.wikipedia.org/wiki/Graphology). Original: Dean, G. A. (1992), "The bottom line: effect size", in Beyerstein & Beyerstein (Eds.), *The Write Stuff*, Prometheus Books (book chapter, no DOI). Exact effect-size values were NOT retrieved — do not quote a number.
- King & Koehler (2000) showed experimentally that illusory correlation (semantic association between handwriting features and trait words) explains why people keep believing in graphology despite null evidence. [V-sec] — [Wikipedia: Graphology](https://en.wikipedia.org/wiki/Graphology); DOI [MEM] 10.1037/1076-898X.6.4.336
- Dazzi & Pedrabissi (2009), *Psychological Reports* 105(3 Pt 2), 1255–1268: two studies (N = 101 with the Big Five Questionnaire; N = 102 autobiographical texts rated by two graphologists and two laypersons); "no evidence was found to validate the graphological method as a measure of personality." [V-abs] — [SAGE record](https://journals.sagepub.com/doi/10.2466/PR0.105.F.1255-1268) (DOI 10.2466/PR0.105.F.1255-1268)
- British Psychological Society (1993), *Graphology in Personnel Assessment*: described in a *Nature* commentary as "an unremittingly negative picture"; secondary sources say the BPS ranked graphology alongside astrology at "zero validity". The exact "zero validity" wording is [V-sec] only. BPS hosts a guideline page with the same title. — [BPS guideline page](https://bps.org.uk/guideline/validity-graphology-personnel-assessment); secondary: [PsyBlog](https://www.spring.org.uk/2023/01/graphology-handwriting-analysis.php)
- Beyerstein & Beyerstein (1992), *The Write Stuff: Evaluations of Graphology — The Study of Handwriting Analysis* (Prometheus) is the edited volume containing Dean's meta-analysis. [V-sec] — [Wikipedia: Graphology](https://en.wikipedia.org/wiki/Graphology)

### Inferences
- Graphology concerns stable traits; the app concerns momentary state. The null results do not strictly rule out state effects on handwriting *kinematics* (section 2), but they do rule out the "read meaning from the shape of the letters" approach, which is exactly what a vision LLM looking at a static image will tend to reproduce, because graphology folklore is abundant in training text.
- King & Koehler's illusory-correlation result is directly relevant to LLM output: a fluent, plausible-sounding reading ("jagged strokes suggest tension") will feel valid to users and judges regardless of whether it is.

### Gaps
- Dean's exact effect sizes and the BPS report's exact wording were not opened. Neither is needed to support the verdict, but neither should be quoted numerically.

---

## 2. Online (digitised) handwriting and drawing kinematics as markers of emotional state

### Takeaway
**Promising-but-preliminary, and weaker than headline accuracies suggest.** Pen-tablet kinematics (timing, in-air time, velocity, pressure) show group-level differences with depression, anxiety and stress questionnaire scores, with honest baseline accuracy around 60–71% on a 129-person dataset; higher figures (up to "100%") come from repeated re-analysis of that same small dataset. None of this was done with fingers on phone touchscreens, with 5–30 s free drawings, or with momentary (within-person) emotion.

### Cited Findings
- **EMOTHAW** (Likforman-Sulem, Esposito, Faundez-Zanuy, Clémençon, Cordasco; *IEEE Trans. Human-Machine Systems* 47(2), 2017): 129 participants; emotional states (anxiety, depression, stress) "assessed by the Depression-Anxiety-Stress Scales (DASS) questionnaire"; seven tasks recorded on a digitizing tablet — pentagons and house drawing, words copied in handprint, circles and clock drawing, one sentence copied in cursive; records pen positions on-paper and in-air, time stamp, pressure, pen azimuth and altitude. [V-abs] — [IP Paris research portal](https://researchportal.ip-paris.fr/en/publications/emothaw-a-novel-database-for-emotional-state-recognition-from-han/); preprint of the same paper [arXiv:2202.12245](https://arxiv.org/abs/2202.12245); journal DOI [MEM] 10.1109/THMS.2016.2635441
- EMOTHAW baseline result: random-forest classifiers with cross-validation; "the targeted emotional states can be identified with accuracies ranging from 60% to 71%"; "anxiety and stress recognition perform better than depression recognition." [V-abs] — [arXiv:2202.12245](https://arxiv.org/abs/2202.12245)
- Cordasco et al. (2019), "Handwriting and drawing features for detecting negative moods": DASS-42-defined depressed, stressed and anxious subjects compared with age- and gender-matched controls; significant differences from controls depending on exercise and feature category (time vs. frequency of events); describes a feature database from 240 subjects. [V-abs; effect sizes not retrieved] — [University of Salerno record](https://www.iris.unisa.it/handle/11386/4906497)
- Nolazco-Flores, Faundez-Zanuy, et al. (2021), *IEEE Access*, "Emotional State Recognition Performance Improvement on a Handwriting and Drawing Task": same EMOTHAW data; time, spectral and cepstral features; RBF-SVM with leave-one-out; reports "accuracy classification improvement ranging from 4% to 34%" over baseline. [V-abs] — [author-repository PDF](https://iris.unicampania.it/retrieve/dfd1c04d-8960-0799-e053-6605fe0a8ddb/IEEEAccess2021.pdf)
- Nolazco-Flores & Faundez-Zanuy et al. (2022), *Sensors* 22(4):1686, "Mood State Detection in Handwritten Tasks Using PCA–mFCBF and Automated Machine Learning": 82.5% / 72.8% / 74.56% for three-level depression / anxiety / stress; "100% accuracy" for two-level severity; training data were augmented by adding Gaussian noise to features; authors note participants share a similar demographic background. [V-abs] — [PMC8875261](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8875261/) (DOI 10.3390/s22041686)
- Rahman & Halim (2023, *Applied Intelligence*; note: 2023, not 2022), "Identifying dominant emotional state using handwriting and drawing samples by fusing features": temporal, spectral and MFCC features with a BiLSTM on writing/drawing signals; reports fusion "improve[s] recognition accuracy significantly". Specific accuracy NOT retrieved. [V-sec] — [catalogue record](https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c319t-8c413cd4e8c9125d8128196625a70d63f616792de3ec28c7c980bf27ff805ec13)
- A 2024 PeerJ Computer Science paper applies an attention-based transformer to handwriting/drawing emotion detection (again EMOTHAW-style data). Accuracy not retrieved. — [PeerJ cs-1887](https://peerj.com/articles/cs-1887)
- Bay Ayzeren, Erbilek & Çelebi (2019), *IEEE Access* 7, 164759–164774: 134 participants, 804 handwriting and 8,040 signature samples, labelled happy / sad / stress, both online and offline; abstract claims "remarkable success especially on stress prediction for handwriting". Numeric accuracies and the emotion-induction procedure were NOT retrieved. [V-abs] — [DOAJ record](https://doaj.org/article/24a3ff7a1dff4d89b6a1dc777db52f8d) (DOI 10.1109/ACCESS.2019.2952313)
- Same group: around 77% reported for stress prediction from *offline* signatures with deep learning (IWBF 2020). [V-sec] — [METU record](https://avesis.ncc.metu.edu.tr/yayin/7e04dad5-6f73-4188-832e-a257562d3102/deep-learning-based-stress-prediction-from-offline-signatures)
- Mergl et al. (2004), *Acta Psychiatrica Scandinavica* 109, 383–391: 37 depressed patients vs. 37 healthy controls on a digitizing tablet; patients' drawing was less regular in velocity and handwriting was abnormally slow (P = 0.04). [V-sec] — [citing record](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi.dedup.....4fa04655d94540361c15837486fba8b2). DOI not verified.
- Rosenblum, Dekel, Gurevitz & Heinik (2010), *Aging Clinical and Experimental Research*: handwriting process variables differed in elderly people with mild major depressive disorder (a "preliminary study"); companion clock-drawing kinematic study by Werner et al. (2010) in *International Psychogeriatrics* (an "exploratory study"). [V-sec; sample sizes not retrieved] — [Cambridge record](https://www.cambridge.org/core/journals/international-psychogeriatrics/article/computerized-kinematic-analysis-of-the-clock-drawing-task-in-elderly-people-with-mild-major-depressive-disorder-an-exploratory-study/D8AF82818B5407F0D7D4734F726E5018)
- Features repeatedly reported as carrying signal: time-based features (including in-air / pen-up time), ductus (stroke counts/order) and pressure for depression; on-paper vs. in-air features computed separately. [V-sec] — [PMC8875261](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8875261/); [arXiv:2202.12245](https://arxiv.org/abs/2202.12245)
- Mental workload (not emotion): 56 participants wrote on a digitizer under varying cognitive load; temporal and spatial/angular-velocity measures changed with load, **pressure measures did not**. [V-abs] — [Behavior Research Methods, DOI 10.3758/s13428-011-0159-8](https://link.springer.com/content/pdf/10.3758/s13428-011-0159-8.pdf)

### Inferences
- **The labels are not momentary emotion.** DASS asks about symptoms over the past week, so EMOTHAW-family models classify *people* by recent symptom level (between-person), not the feeling a user has in this minute. The app's claim ("how you feel right now") is a different, untested construct. (DASS time frame is [MEM]: Lovibond & Lovibond 1995, DOI 10.1016/0005-7967(94)00075-U.)
- **Hardware mismatch.** All of this used a pen on a digitizing tablet with true pressure, pen tilt and in-air tracking. A finger on a phone gives no in-air trajectory, no tilt and (usually) no real pressure (see section 7). The best-supported feature family the app can still capture is *timing*: stroke durations, pauses between strokes, speed and its variability.
- **Task mismatch.** Evidence is for standardised copy tasks (pentagons, clock, a fixed sentence) so that people can be compared on identical content. Free drawing for 5–30 s confounds state with what the person chose to draw.
- **Inflation risk.** With N = 129 and hundreds of candidate features, feature selection plus leave-one-out, noise augmentation, and many papers tuning on the same dataset all push reported accuracy upward. "100%" on a two-class split of ~129 students should be treated as a red flag, not a benchmark. No independent-sample replication was located.
- Honest summary line for judges: "In lab pen-tablet studies, movement timing distinguishes higher from lower anxiety/stress questionnaire scorers about 60–70% of the time (chance ~50% for binary splits) — a real but small signal, never shown on phones or for moment-to-moment mood."

### Gaps
- Ayzeren et al.'s accuracy numbers and whether emotions were induced (e.g., by video) or self-reported: not retrieved.
- No study located using a Trier Social Stress Test or cortisol-verified stress with handwriting kinematics.
- No study located validating finger-on-touchscreen drawing dynamics against momentary affect.
- "Gupta et al." (named in the brief) could not be identified to a specific paper.
- EMOTHAW participant demographics (believed to be Italian university students, [MEM]) not re-verified.

---

## 3. Offline (static image) deep learning, and general-purpose vision LLMs

### Takeaway
**Weak.** Static-image results are sparse and unreplicated, and static images discard exactly the features (timing, in-air, pressure) that carried the signal in section 2. **No peer-reviewed evidence was found that general-purpose vision LLMs (GPT-4V/4o, Gemini, Claude) can validly infer a person's emotional state from handwriting or a free drawing.** The LLM papers that exist are preprints that measure agreement with expert *interpretations*, not accuracy against the drawer's actual state.

### Cited Findings
- Offline signatures, deep learning: about 77% stress-prediction accuracy reported by one group (IWBF 2020). [V-sec] — [METU record](https://avesis.ncc.metu.edu.tr/yayin/7e04dad5-6f73-4188-832e-a257562d3102/deep-learning-based-stress-prediction-from-offline-signatures)
- **Preprint** (arXiv 2512.21360, Dec 2025), multi-agent multimodal-LLM framework for House-Tree-Person drawings: mean semantic similarity between LLM interpretations and human expert interpretations of about 0.75. This is text similarity to experts, not validity against a mental-state criterion. [V-abs] — [arXiv:2512.21360](https://arxiv.org/abs/2512.21360v1)
- **Preprint** (arXiv 2510.19451, Oct 2025), "Reasoning Like Experts: Leveraging Multimodal LLMs for Drawing-based Psychoanalysis" (PICK): emotion-distribution targets were themselves generated with GPT-4o. [V-sec, via an AI-generated review page] — [review page](https://www.themoonlight.io/review/reasoning-like-experts-leveraging-multimodal-large-language-models-for-drawing-based-psychoanalysis)
- **Preprint** (arXiv 2601.04297, Jan 2026), "ArtCognition": combines image features with kinematic cues from the drawing process (stroke speed, pauses) plus retrieval-augmented generation; authors report "significant correlations" with standardised psychological metrics. Sample size and effect sizes not retrieved. [V-abs] — [arXiv:2601.04297](https://arxiv.org/html/2601.04297v1)
- Cautionary parallel from a far better-studied channel: Barrett, Adolphs, Marsella, Martinez & Pollak (2019) concluded that facial movements "are not universally diagnostic of emotional states" and that software "does not detect the psychological meaning" of the movements it measures. [V-sec] — [APS summary](https://www.psychologicalscience.org/publications/emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.html); DOI [MEM] 10.1177/1529100619832930

### Inferences
- A vision LLM returning `{"stress": 0.7, "anxiety": 0.4}` from a doodle is producing an *interpretation in the style of human interpreters*. Since the human interpreters' own methods (graphology, projective drawing signs) lack validity (sections 1 and 4), agreement with them is not evidence of accuracy.
- Decimal scores imply measurement precision that does not exist. This is the single least defensible element of the current design.
- What an LLM can defensibly do: describe visible properties (colour, density, line quality, content) and relate them to *documented population-level expressive conventions* (section 5), phrased as a prompt for the user's own reflection.

### Gaps
- No benchmark found that scores Gemini / Claude / GPT-4-class models on drawer-reported emotion from drawings or handwriting. Absence of evidence was established by one search pass only; a dedicated search may find more.
- Test-retest and cross-model consistency of LLM emotion scores for the same drawing: no published data found.

---

## 4. Projective drawing tests (House-Tree-Person, Draw-A-Person)

### Takeaway
**Weak (sign-based interpretation is close to pseudoscience).** The authoritative review found validity evidence for human figure drawings even more limited than for the Rorschach and TAT, with little incremental validity and a file-drawer problem. Recent deep-learning HTP papers reporting 89–99% depression-detection accuracy are small, single-site and internally validated; the one large study (N = 4,196) found the network **could not** separate depressed from non-depressed drawers.

### Cited Findings
- Lilienfeld, Wood & Garb (2000), *Psychological Science in the Public Interest* 1(2): only a small number of Rorschach/TAT indexes are empirically supported; "the validity evidence for human figure drawings is even more limited"; projective indexes "have not consistently demonstrated incremental validity above and beyond other psychometric data"; published effect sizes markedly exceeded unpublished ones (file-drawer effect). [V-abs] — [author-hosted PDF](https://www3.nd.edu/~ghaeffel/Lilienfeld(2000).pdf); DOI [MEM] 10.1111/1529-1006.002
- Motta, Little & Tobin (1993), "The use and abuse of human figure drawings", *School Psychology Quarterly* 8(3), 162–169: critical review concluding figure drawings should not be used as measures of personality/emotional adjustment. NOT retrieved this session — citation and conclusion are [MEM]; DOI [MEM] 10.1037/h0088271.
- Large null result: *Acta Psychologica* (Oct 2022), 4,196 Chinese children and adolescents — deep networks learned to recognise houses, trees and persons, but "failed to classify the drawings of depressive individuals from those of non-depressive individuals"; authors call the test's validity for diagnosing mental health problems doubtful. [V-abs] — [DOAJ record](https://doaj.org/article/a1d067ec7ddd43ab98d127d84e4ee9e7)
- High-accuracy claims: FBANet transfer-learning model, *Entropy* 25(9):1350 (2023) — maximum 99.07% validation accuracy, 97.71% mean in cross-validation, with authors acknowledging "the limited size of the collected data". [V-abs] — [MDPI](https://mdpi.com/1099-4300/25/9/1350)
- 2024 feasibility study: 309 drawings from people at risk of major depression vs. 290 without; best classifier 97.2% accuracy. [V-sec] — [RePEc record](https://econpapers.repec.org/RePEc:taf:gcmbxx:v:27:y:2024:i:9:p:1129-1140)
- 2025 CNN study: 89% accuracy, AUC 0.96 (normal vs. depressed) and AUC 1.00 (moderate vs. severe). Sample size and validation scheme not retrieved. [V-abs] — [EM-consulte record](https://www.em-consulte.com/article/1771628/feature-analysis-of-depression-patients-house-tree)

### Inferences
- Accuracy near 100% for a psychiatric label from a pencil drawing is implausible given that the questionnaires used as ground truth do not agree with each other that well; the likeliest explanations are site/scanner/paper/age confounds (patients drawn in a hospital, controls elsewhere) and leakage. The pattern "small sample → near-perfect; large sample → null" is the classic signature of overfitting.
- The app should not ask users to draw a house, tree or person and should not interpret content symbolically (e.g., "no windows = withdrawal").

### Gaps
- Limitations sections of the high-accuracy HTP papers were not opened; the confound explanation above is an inference, not a documented finding.

---

## 5. Do people encode emotion in abstract line and colour, and can it be decoded?

### Takeaway
**Promising-but-preliminary for decoding an *intended* emotion from an abstract drawing; well-supported for shared colour–emotion *associations*.** This is the most defensible basis for the product: when people are *asked to draw a named feeling*, their colour and line choices are systematic enough for humans and algorithms to guess the intended emotion well above chance — but far from reliably (roughly 25–51% correct against 17% chance among six emotions).

### Cited Findings
- Damiano, Gayen, Rezanejad, Banerjee, Banik, Patnaik, Wagemans & Walther (**2023**, not 2021), *Journal of Vision* 23(4): artists and non-artists made abstract colour drawings and line drawings for six emotions (anger, disgust, fear, joy, sadness, wonder); emotion was predicted computationally by comparing each drawing with averages of all other participants' drawings per emotion. "Prediction accuracy was higher for color drawings than line drawings and higher for color drawings by non-artists than by artists." "Anger is generally redder and more densely drawn than other emotions, sadness is more blue and contains more vertical lines." [V-abs] — [PMC10080919](https://pmc.ncbi.nlm.nih.gov/articles/PMC10080919/); DOI [MEM] 10.1167/jov.23.4.1
- Numbers for that study, from secondary sources only: chance = 17% (1 of 6); computer accuracy about 25% for line drawings, about 51% (50.81%) for non-artists' colour drawings, about 39% for artists' colour drawings; human observers about 32% for line drawings, 43% for non-artists' colour drawings, 40% for artists' colour drawings (about 41.5% overall in one summary). Sample-size reports conflict: 46 artists + 45 non-artists in one source vs. 40 + 41 in the university press release. [V-sec — verify in the paper before quoting] — [University of Toronto news](https://www.utoronto.ca/news/researchers-explore-how-we-depict-and-perceive-emotions-through-colour-and-line-visual-art); [Futurum summary](https://www.futurumcareers.com/are-there-rules-for-conveying-emotion-through-art)
- Jonauskaite et al. (2020), *Psychological Science* 31(10), 1245–1260: 4,598 participants, 30 nations, 22 native languages, 20 emotion concepts × 12 colour terms; colour–emotion association patterns were highly similar across nations (average similarity coefficient r = .88), with additional local variation by linguistic and geographic proximity. [V-abs] — [EPFL record](https://infoscience.epfl.ch/record/280269) (DOI 10.1177/0956797620948810)
- Classic line-affect studies: Lundholm (1921), "The affective tone of lines", *Psychological Review* 28, 43–60; Poffenberger & Barrows (1924), "The feeling value of lines", *Journal of Applied Psychology* 8, 187–205 — participants consistently matched line shapes (angular vs. curved, rising vs. falling) to feeling words. NOT retrieved this session; citations, DOIs (10.1037/h0072647; 10.1037/h0073513) and the summary are [MEM].

### Inferences
- **What this evidence licenses:** "People who are asked to draw anger tend to use more red and denser marks; people asked to draw sadness tend to use more blue and vertical lines." It is about *deliberate depiction of a named emotion*.
- **What it does not license:** inferring that a person who happened to use red *is* angry. Jonauskaite's data are word-to-word associations about concepts, not measurements of felt mood; Damiano's participants were told which emotion to depict.
- Design consequence: the task must be an explicit "draw how you feel right now" prompt (expression), and the app must offer a colour palette — colour carried roughly twice the signal of line alone (about 51% vs. 25% computational accuracy). A black-ink-only canvas throws away the best-supported channel.
- Even the best case (about 51% of six) means the guess is wrong about half the time, so the output must be presented as a guess for the user to confirm or correct.
- Stress, anxiety and depression were not among the six categories studied; mapping to those is an extrapolation.

### Gaps
- No study found testing whether spontaneous drawings made under a *felt* (induced or naturally occurring) emotion are decodable, as opposed to instructed depictions.
- Whether effects hold for 5–30 s finger drawings on a phone is untested.

---

## 6. Related passive sensing and the plausibility of a motor pathway

### Takeaway
**Promising-but-preliminary.** There is a credible physiological route (psychomotor slowing in depression; arousal effects on timing and force), and typing-dynamics studies show mood-related signal — but the supporting studies are tiny (e.g., N = 9) or rely on longitudinal *within-person* baselines over weeks, which a single 30-second drawing cannot provide.

### Cited Findings
- Zulueta et al. (2018), *JMIR* 20(7):e241 (BiAffect): 9 participants with bipolar disorder (5 type I, 4 type II), at least 4 weeks of data each; keystroke timing and accelerometer metadata (no text content) predicted weekly clinician ratings — depression (HDRS-17) mixed model conditional R² = .63, P = .01; mania (YMRS) OLS R² = .34, P = .001. [V-abs] — [JMIR](https://www.jmir.org/2018/7/e241) (DOI 10.2196/jmir.9775)
- Epp, Lippold & Mandryk (2011), CHI '11, pp. 715–724: field study pairing keystroke features (dwell and flight times) with experience-sampled self-reports; classifiers for 15 emotional states; secondary summaries cite accuracies of roughly 77–88% for two-level classification of several states (e.g., about 84% for anger and excitement). Participant count and exact accuracies NOT verified against the paper. [V-sec] — [bibliographic record](https://bibtex.github.io/CHI-2011-EppLM.html) (DOI 10.1145/1978942.1979046)
- Psychomotor slowing in depression is measurable in pen movements: slower handwriting and less regular drawing velocity in 37 patients vs. 37 controls. [V-sec] — Mergl et al. 2004, see section 2 [citing record](https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi.dedup.....4fa04655d94540361c15837486fba8b2)
- Stress and graphic motor control: Meulenbroek et al. (2005) tested 10 adults on a graphic task with a distracting sound as stressor, hypothesising increased muscle co-contraction and longer movement times; a related study reported longer reaction/movement times and higher axial pen pressure under cognitive stress. [V-sec] — [Meulenbroek et al. PDF](https://www.socsci.ru.nl/meulenbroek/Publications/Meulenbroek%20et%20al%202005.pdf)
- Pressure findings are inconsistent: Longstaff & Heath (2000) found people without tremor increased axial pen pressure under mild physical stress and both groups wrote slightly faster, whereas the 56-person mental-workload study found pressure insensitive to load. [V-sec / V-abs] — [SCU record](https://researchportal.scu.edu.au/esploro/outputs/journalArticle/The-influence-of-tremor-on-handwriting/991012821705302368); [DOI 10.3758/s13428-011-0159-8](https://link.springer.com/content/pdf/10.3758/s13428-011-0159-8.pdf)

### Inferences
- The pathway is plausible and timing features are the most consistent carriers; pressure is inconsistent across studies and mostly unavailable on phones anyway.
- These signals are far more interpretable as *change from the same person's own baseline* than as an absolute reading. A defensible roadmap item is per-user baselining over repeated check-ins, not single-shot inference.
- Cognitive load, fatigue, caffeine, device, posture, and whether the person is walking all move the same kinematic features; they are not specific to emotion.

### Gaps
- No controlled study found linking acute psychological stress (validated induction) to touchscreen drawing kinematics.
- Epp et al.'s sample size and exact accuracies unverified.

---

## 7. Practical recommendations: framing, self-report anchoring, signal capture, regulation

### Takeaway
The defensible product is an **expressive check-in**: the drawing is a reflection prompt and engagement device; a one-tap validated self-report is the actual input that drives the activity suggestion; the AI reading is shown as a tentative guess the user confirms or corrects. Keep it a low-risk general-wellness product with no diagnostic language, disclose the emotion inference, and keep it out of workplace and education deployments in the EU.

### Cited Findings
**Self-report anchors (all [MEM] — standard instruments, DOIs not opened this session):**
- PHQ-4: 4 items, 2 for depression (PHQ-2) and 2 for anxiety (GAD-2), validated ultra-brief screener; asks about the past 2 weeks. Kroenke, Spitzer, Williams & Löwe (2009), *Psychosomatics* 50(6), 613–621 — DOI 10.1176/appi.psy.50.6.613
- Affect Grid: single-item 9 × 9 grid capturing valence and arousal in one tap. Russell, Weiss & Mendelsohn (1989), *JPSP* 57(3), 493–502 — DOI 10.1037/0022-3514.57.3.493
- Self-Assessment Manikin: pictorial, language-free ratings of valence, arousal, dominance. Bradley & Lang (1994), *J. Behav. Ther. Exp. Psychiatry* 25(1), 49–59 — DOI 10.1016/0005-7916(94)90063-9
- I-PANAS-SF: 10-item cross-culturally validated short PANAS. Thompson (2007), *J. Cross-Cultural Psychology* 38(2), 227–242 — DOI 10.1177/0022022106297301

**Signal capture:**
- W3C Pointer Events: for hardware that does not support pressure, `pressure` "MUST be 0.5 when in the active buttons state and 0 otherwise" — so on most finger-touch phones pressure is a constant, not a measurement. [V-abs] — [MDN: PointerEvent.pressure](https://developer.mozilla.org/docs/Web/API/PointerEvent/pressure)
- Browsers deviate: WebKit on Apple platforms has reported 1.0 (and, per a bug report, 0) for non-pressure-sensitive devices; Firefox on Android has a bug reporting wrong touch pressure. [V-abs] — [WebKit bug 206216](https://bugs.webkit.org/show_bug.cgi?id=206216); [Mozilla bug 1487509](https://bugzilla.mozilla.org/show_bug.cgi?id=1487509)
- Timing features (durations, pauses, velocity) are the family with the most consistent support across sections 2 and 6. — [arXiv:2202.12245](https://arxiv.org/abs/2202.12245); [DOI 10.3758/s13428-011-0159-8](https://link.springer.com/content/pdf/10.3758/s13428-011-0159-8.pdf)

**FDA (US):**
- FDA issued an updated final guidance "General Wellness: Policy for Low Risk Devices" on 6 January 2026, superseding the 2019 version; it keeps the two-part test (general-wellness-only intended use + low risk) while broadening examples; a February 2026 CDRH town hall stressed the core principles are unchanged. [V-sec — law-firm summaries; FDA document not opened] — [FDA guidance PDF](https://www.fda.gov/media/90652/download); [Ropes & Gray](https://www.ropesgray.com/en/insights/alerts/2026/01/fda-adapts-with-the-times-on-digital-health-updated-guidances-on-general-wellness-products); [King & Spalding](https://www.kslaw.com/news-and-insights/fda-updates-general-wellness-and-clinical-decision-support-guidance-documents)

**EU AI Act (status as found November 2026; verify against the Official Journal):**
- Article 5(1)(f) prohibits AI systems "to infer emotions of a natural person in the areas of workplace and education institutions", except for medical or safety reasons. The Commission's guidelines on prohibited practices (published 4 February 2025, non-binding) treat recruitment as part of "workplace", and state the prohibition does not cover emotion recognition in other contexts such as commercial/consumer use. [V-sec] — [Future of Privacy Forum analysis](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/); [WSGR](https://www.wsgrdataadvisor.com/2025/02/eu-commission-issues-guidelines-on-prohibited-ai-practices-under-eu-ai-act/)
- Prohibitions have applied since 2 February 2025. [MEM — widely reported; not re-verified this session]
- "Emotion recognition system" is defined (Art. 3(39), Recital 18) as an AI system identifying or inferring emotions or intentions of natural persons **on the basis of their biometric data**; it excludes physical states such as pain or fatigue. Biometric data covers physical, physiological or **behavioural** characteristics. [V-abs] — [Commission AI Act Service Desk, Recital 18](https://ai-act-service-desk.ec.europa.eu/en/ai-act/recital-18); [Mishcon Article 3](https://mishcon.com/eu-uk-ai-navigator/article-3)
- Article 50(3): deployers of an emotion recognition system must inform the people exposed to it. Article 50 transparency obligations became applicable on 2 August 2026 and were **not** delayed by the Digital Omnibus (only the Art. 50(2) machine-readable-marking duty for systems already on the market got a short extension — sources conflict between 2 December 2026 and 2 February 2027). [V-sec] — [Goodwin, Aug 2026](https://www.goodwinlaw.com/en/insights/publications/2026/08/alerts-technology-dpc-eu-ai-act-transparency-obligations-now-in-force); [CMS](https://cms.law/en/cze/legal-updates/eu-ai-act-developments-key-political-agreement-on-the-digital-omnibus-on-ai-implementation-timeline-and-transparency-consultation)
- Emotion recognition systems are an Annex III high-risk category; the Digital Omnibus reportedly deferred Annex III standalone high-risk obligations to 2 December 2027. Sources disagree on whether the Omnibus was formally adopted (one reports Parliament endorsement 16 June 2026 and Council approval 29 June 2026). [V-sec, mixed-quality sources] — [Simmons & Simmons](https://www.simmons-simmons.com/en/publications/cmoveo6ke00icuxskpgueb0od/ai-omnibus-update); [Cooley](https://cdp.cooley.com/digital-ai-omnibus-delays-key-deadlines-introduces-new-rules/)

### Inferences
- **Does the app fall under the AI Act's emotion-recognition definition?** Captured stroke dynamics are behavioural data from an identifiable person and plausibly "biometric data"; a static picture of a drawing is less clearly so. No source found addresses drawings or handwriting specifically. The safe posture is to assume it does: disclose clearly (Art. 50(3)), and never market to employers or schools (Art. 5(1)(f)). A consumer self-care app is outside the prohibition but may still be a high-risk emotion-recognition system once Annex III obligations apply. This is an inference, not legal advice.
- A design in which the *user's own self-report* is the operative input, and the AI only describes the drawing and offers a guess the user can overrule, both weakens the "AI infers your emotion" characterisation and is the scientifically honest design.
- Mood/emotion inferences are sensitive personal data in practice; sending drawings plus stroke data to third-party LLM APIs needs explicit consent and minimisation (GDPR point — not researched here).
- Multi-LLM agreement measures **reliability, not validity**: two models can agree because they share the same folk-psychology priors. Use disagreement as a reason to suppress output, never agreement as proof.
- PHQ-4's two-week recall window makes it a periodic screener, not a per-session mood measure; the Affect Grid or a single mood item fits the per-session one-tap role.

### Gaps
- The verbatim Official Journal text of Art. 5(1)(f), Art. 50(3) and Annex III point 1(c) was not opened (host blocked); wording above is from secondary legal sources.
- Final adoption status and exact dates of the Digital Omnibus are disputed between sources.
- Whether the Commission guidelines explicitly name handwriting or keystrokes as behavioural biometrics for emotion recognition: the researcher recalls keystrokes being listed, but this is unverified.
- Current Safari behaviour for Apple Pencil pressure via Pointer Events was not confirmed; test on a device.
- UK, US-state (e.g., biometric privacy statutes) and GDPR analysis not covered.

---

## Evidence verdict table

| Claim | Verdict | Best supporting or refuting source | doi_or_url |
|---|---|---|---|
| Handwriting shape/style reveals personality or disposition (graphology) | Pseudoscience | Neter & Ben-Shakhar 1989 meta-analysis (17 studies, 1,223 scripts; graphologists no better than laypeople); Dazzi & Pedrabissi 2009 (N = 101, N = 102; no validity) | https://cris.huji.ac.il/en/publications/the-predictive-validity-of-graphological-inferences-a-meta-analyt/ ; https://journals.sagepub.com/doi/10.2466/PR0.105.F.1255-1268 |
| People believe graphology-style readings because of illusory correlation | Well-supported | King & Koehler 2000 | 10.1037/1076-898X.6.4.336 (DOI from memory) |
| Pen-tablet kinematics distinguish higher vs. lower DASS anxiety/stress/depression scorers | Promising-but-preliminary (60–71% baseline, N = 129, one dataset) | Likforman-Sulem et al. 2017 (EMOTHAW) | https://arxiv.org/abs/2202.12245 (preprint of the IEEE THMS paper) |
| Handwriting kinematics detect mood with 80–100% accuracy | Weak (same small dataset, noise augmentation, no external validation) | Nolazco-Flores et al. 2022 | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8875261/ (10.3390/s22041686) |
| Depression slows and de-regularises handwriting/drawing movement | Promising-but-preliminary (clinical groups, 37 vs. 37) | Mergl et al. 2004, Acta Psychiatr Scand 109:383–391 | https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi.dedup.....4fa04655d94540361c15837486fba8b2 (secondary; DOI unverified) |
| A 5–30 s finger drawing on a phone reveals momentary stress/anxiety | Unsupported (no study found) | — (hardware, task and construct all differ from the pen-tablet literature) | https://arxiv.org/abs/2202.12245 |
| Static images of handwriting/signatures reveal stress via deep learning | Weak (single group, about 77%, unreplicated) | Erbilek group, IWBF 2020 | https://avesis.ncc.metu.edu.tr/yayin/7e04dad5-6f73-4188-832e-a257562d3102/deep-learning-based-stress-prediction-from-offline-signatures |
| General-purpose vision LLMs can validly score a person's emotion from handwriting or a drawing | Unsupported (no peer-reviewed validation found; preprints measure similarity to expert interpretations, about 0.75) | arXiv 2512.21360 (preprint) | https://arxiv.org/abs/2512.21360v1 |
| Projective drawing signs (HTP, Draw-A-Person) indicate emotional disturbance | Weak | Lilienfeld, Wood & Garb 2000 | https://www3.nd.edu/~ghaeffel/Lilienfeld(2000).pdf (10.1111/1529-1006.002, DOI from memory) |
| Deep learning on HTP drawings screens for depression at 89–99% accuracy | Weak (small, internally validated) — contradicted by large null study, N = 4,196 | Acta Psychologica 2022 null result vs. Entropy 2023 FBANet | https://doaj.org/article/a1d067ec7ddd43ab98d127d84e4ee9e7 ; https://mdpi.com/1099-4300/25/9/1350 |
| When asked to draw a named emotion abstractly, people use systematic colour/line cues that others can decode above chance | Promising-but-preliminary (about 25–51% vs. 17% chance; one main study; instructed depiction) | Damiano et al. 2023, Journal of Vision 23(4) | https://pmc.ncbi.nlm.nih.gov/articles/PMC10080919/ |
| Colour–emotion associations are largely shared across cultures | Well-supported (as conceptual associations; N = 4,598, 30 nations, r = .88) | Jonauskaite et al. 2020 | 10.1177/0956797620948810 |
| Colours a person uses reveal the mood they are in | Weak / unsupported (associations ≠ felt state) | Jonauskaite et al. 2020 (measures concepts only) | 10.1177/0956797620948810 |
| Typing/touch dynamics track mood over weeks within a person | Promising-but-preliminary (N = 9; R² = .63 depression) | Zulueta et al. 2018 (BiAffect) | 10.2196/jmir.9775 |
| Pen pressure reliably rises with stress | Weak / inconsistent | Luria & Rosenblum-group workload study (pressure insensitive) vs. Longstaff & Heath 2000 | https://link.springer.com/content/pdf/10.3758/s13428-011-0159-8.pdf |
| Finger touch on phones gives usable pressure data in the browser | Refuted for most devices (spec mandates constant 0.5 when unsupported) | W3C Pointer Events via MDN | https://developer.mozilla.org/docs/Web/API/PointerEvent/pressure |
| Even well-studied expressive channels (faces) do not reliably diagnose emotion | Well-supported | Barrett et al. 2019 | https://www.psychologicalscience.org/publications/emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.html |
| Ultra-brief self-report (PHQ-4, Affect Grid, SAM, I-PANAS-SF) validly captures mood/affect | Well-supported | Kroenke et al. 2009; Russell et al. 1989; Bradley & Lang 1994; Thompson 2007 | 10.1176/appi.psy.50.6.613 ; 10.1037/0022-3514.57.3.493 ; 10.1016/0005-7916(94)90063-9 ; 10.1177/0022022106297301 (DOIs from memory) |
| EU AI Act bans emotion inference in workplace and education; consumer use is not banned but carries transparency duties | Well-supported (secondary legal sources) | FPF analysis; Goodwin Aug 2026 | https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/ ; https://www.goodwinlaw.com/en/insights/publications/2026/08/alerts-technology-dpc-eu-ai-act-transparency-obligations-now-in-force |

## Recommendations for the app

- **Reframe the claim.** Say "an expressive check-in that helps you notice how you feel", never "we detect your stress from your handwriting". No peer-reviewed evidence supports single-shot state detection from a short phone drawing, and graphology-style inference is discredited. — [Neter & Ben-Shakhar 1989](https://cris.huji.ac.il/en/publications/the-predictive-validity-of-graphological-inferences-a-meta-analyt/); [Dazzi & Pedrabissi 2009](https://journals.sagepub.com/doi/10.2466/PR0.105.F.1255-1268)
- **Make a one-tap self-report the operative input for recommendations.** Use an Affect Grid or single mood/stress item every session, with PHQ-4 as an optional periodic check; let the drawing enrich, not replace, it. — Russell et al. 1989 (10.1037/0022-3514.57.3.493, DOI from memory); Kroenke et al. 2009 (10.1176/appi.psy.50.6.613, DOI from memory)
- **Change the task to "draw how you feel right now" with a colour palette.** The only decoding evidence is for deliberate abstract depiction, and colour roughly doubled accuracy over line alone. Do not use handwriting copy tasks or house/tree/person prompts. — [Damiano et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10080919/); [Acta Psychologica 2022 HTP null result](https://doaj.org/article/a1d067ec7ddd43ab98d127d84e4ee9e7)
- **Present the AI output as a tentative guess the user confirms or corrects**, e.g. "This looks intense and dense to me — does 'tense' fit, or is it something else?" Best-case decoding is wrong about half the time. Log the correction; it is your ground truth. — [University of Toronto summary of Damiano et al.](https://www.utoronto.ca/news/researchers-explore-how-we-depict-and-perceive-emotions-through-colour-and-line-visual-art)
- **Drop decimal emotion scores.** Replace `stress: 0.72` with coarse, hedged labels plus the visible features that prompted them (colour, density, line quality). Numeric scores imply a measurement validity that does not exist for LLMs on this task. — [arXiv:2512.21360 (preprint; similarity to experts, not validity)](https://arxiv.org/abs/2512.21360v1); [Barrett et al. 2019](https://www.psychologicalscience.org/publications/emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.html)
- **Constrain the LLM prompt.** Forbid graphological and projective-sign reasoning explicitly; ask the model to describe observable features first and to relate them only to documented colour/line conventions. — [Lilienfeld, Wood & Garb 2000](https://www3.nd.edu/~ghaeffel/Lilienfeld(2000).pdf); [Jonauskaite et al. 2020](https://infoscience.epfl.ch/record/280269)
- **Capture stroke timing, not just a picture** — per-stroke duration, inter-stroke pauses, speed and speed variability, total ink, canvas coverage. Timing is the feature family with the most consistent support. Label it experimental and do not feed it into user-facing scores yet. — [EMOTHAW](https://arxiv.org/abs/2202.12245); [workload study, 10.3758/s13428-011-0159-8](https://link.springer.com/content/pdf/10.3758/s13428-011-0159-8.pdf)
- **Do not rely on pressure.** Record `pressure` and `pointerType`, but treat pressure as valid only for `pointerType === "pen"`; finger touch reports a constant and browsers are inconsistent. — [MDN PointerEvent.pressure](https://developer.mozilla.org/docs/Web/API/PointerEvent/pressure); [WebKit bug 206216](https://bugs.webkit.org/show_bug.cgi?id=206216)
- **Use each user as their own baseline over time.** The more credible passive-sensing results are within-person and longitudinal; show trends only after several check-ins. — [Zulueta et al. 2018](https://www.jmir.org/2018/7/e241)
- **Use multi-LLM agreement only as a suppression filter.** If models disagree, show no guess and just ask the user; do not present agreement as accuracy, since shared priors produce agreement without validity. — [King & Koehler 2000 on illusory correlation, via Wikipedia summary](https://en.wikipedia.org/wiki/Graphology)
- **Prefer the 30 s default and standardise it.** The supporting literature uses fixed, comparable tasks; a 5 s sample yields few strokes and no stable timing statistics. This is an inference from the task designs, not a tested threshold. — [EMOTHAW task design](https://researchportal.ip-paris.fr/en/publications/emothaw-a-novel-database-for-emotional-state-recognition-from-han/)
- **Stay inside general wellness.** No diagnostic terms ("depression", "anxiety disorder"), no treatment claims, a clear "not a medical device / not a diagnosis" statement, and a route to crisis resources when self-report is severe. — [FDA General Wellness guidance, updated 6 Jan 2026](https://www.fda.gov/media/90652/download); [Ropes & Gray summary](https://www.ropesgray.com/en/insights/alerts/2026/01/fda-adapts-with-the-times-on-digital-health-updated-guidances-on-general-wellness-products)
- **EU: disclose the emotion inference up front and never sell into workplaces or schools.** Art. 50(3) notice duties have applied since 2 August 2026; Art. 5(1)(f) prohibits emotion inference in workplace and education settings. Plan for possible high-risk (Annex III) classification. — [Goodwin](https://www.goodwinlaw.com/en/insights/publications/2026/08/alerts-technology-dpc-eu-ai-act-transparency-obligations-now-in-force); [FPF](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/)
- **Tell judges the validation plan.** Collect drawing + stroke data + same-session self-report (with consent), then test whether any feature predicts the self-report within person, on held-out users. This turns an unvalidated claim into a falsifiable study and avoids the small-sample inflation seen in the literature. — [Nolazco-Flores et al. 2022 as the cautionary example](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8875261/)
- **One-sentence pitch that survives scrutiny:** "Drawing is how you express it, a one-tap check is how we measure it, and the AI is a mirror, not a diagnostician." — grounded in [Damiano et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10080919/) and [Lilienfeld et al. 2000](https://www3.nd.edu/~ghaeffel/Lilienfeld(2000).pdf)
