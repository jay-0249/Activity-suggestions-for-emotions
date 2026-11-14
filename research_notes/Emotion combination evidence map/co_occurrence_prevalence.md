# Co-occurrence prevalence of specific emotion pairs and triples

Scope: which of the app's 12 classes (stressed, anxious, angry, restless, sad, lonely, tired, bored, calm, content, energetic, neutral) actually co-occur, and how strongly. This builds on, and does not repeat, the taxonomy and "mixed emotions" sections of `research_notes/Emotion to activity evidence map/emotion_models_and_matching_logic.md`. That note established that mixed emotions are common (Berrios 2015; Trampe 2015) but had no pair-level numbers.

Verification tags: **[PM-abs]** = read in the PubMed abstract (NCBI E-utilities) this session; **[PM-full]** = read in the PMC full text or a table fetched via E-utilities efetch db=pmc this session; **[web]** = seen only in a web-search summary or snippet, not the primary text; **[memory]** = from prior knowledge, not verified this session. "Derived" means arithmetic I did on numbers from the cited table.

Construct mapping used throughout: depression / dejection / low mood / anhedonic depression → sad; DASS stress / POMS-BRUMS tension → stressed (note: BRUMS "tension" items are anxiety words such as anxious, nervous, worried, panicky [memory], so they could just as well map to anxious); worry / GAD / anxious arousal → anxious; irritability / frustration / hostility / anger → angry; fatigue / exhaustion / burnout → tired; vigor → energetic; loneliness → lonely; boredom → bored; happy / joy / satisfaction → content; psychomotor agitation / "restlessness, keyed up" → restless.

---

## 1. Everyday (experience-sampling, day-reconstruction) co-occurrence of momentary emotions

### Takeaway
In daily life, about a third of sampled moments contain both a positive and a negative emotion (Trampe 2015: 33%). Negative emotions co-occur with each other at moderate within-person strength: worried–sad r = .45, frustrated–worried r = .40, frustrated–sad r = .30 (Lucas 2018 DRM). Lonely and bored form their own factor, separate from a stressed/worried/angry/sad factor. Trampe et al. did publish a full pairwise co-occurrence table (S1 Table), but it could not be retrieved from this session.

### Cited Findings
- **Trampe, Quoidbach & Taquet 2015 (PLoS ONE 10:e0145450; PMID 26698124; PMC4689475)**, smartphone experience sampling, >11,000 people, 18 mDES emotions recorded as binary present/absent. Of all sampled moments, 41% had positive emotions only, 16% negative only, **33% mixed** (≥1 positive and ≥1 negative at once), and 90% at least one emotion — [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4689475/) [PM-full].
  - Frequencies relevant to the 12 classes (Table 2): joy 35%, satisfaction 27% (→ content), alertness 24% (closest to energetic, an approximation), **anxiety 29%**, **sadness 20%**, **anger 10%**, fear 5% — [PM-full].
  - "The emotions that most frequently co-occurred with an opposite valence emotion were **anxiety and love**", and the paper sends readers to S1 Table for details — [PM-full].
  - The network edges are **correlation coefficients between binary emotion vectors** (phi coefficients) and are shown only as colours in Fig 4. Text descriptions: joy and satisfaction co-occur with positive emotions and inhibit sadness, anxiety, disgust and anger. Sadness, anxiety, disgust and anger are "connector" emotions that co-occur with guilt and fear and inhibit joy and satisfaction. Alertness, embarrassment and contempt are "distal" (largely independent of the others). Degree centrality: joy 3.0, satisfaction 2.7, sadness 2.6, anger 2.2, anxiety 1.7, alertness 1.3 — [PM-full].
  - **S1 Table, "Co-occurrence of emotions" (DOCX, pone.0145450.s001.docx)** holds the pairwise numbers. Retrieval failed: PMC returned a proof-of-work challenge page, and journals.plos.org, ncbi.nlm.nih.gov/pmc, Europe PMC and osf.io (open data: https://osf.io/h2jp3/) were all blocked by this session's network. **The pairwise values were not obtained** [PM-full for the table's existence and title].
- **Lucas, Freedman, Carr & Anusic 2018 (Measuring experiential well-being among older adults; J Posit Psychol; PMID 31182970; PMC6555425; doi 10.1080/17439760.2018.1497686)**, PSID 2013 Disability and Use of Time (DUST) supplement, adults aged ≥60, day reconstruction method (DRM). **Within-person (episode-level) correlations** — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6555425/) [PM-full]:
  - calm–happy **.44**; frustrated–worried **.40**; worried–sad **.45**; frustrated–sad **.30**
  - calm–frustrated −.33; calm–worried −.24; calm–sad −.19; happy–frustrated −.35; happy–worried −.28; happy–sad −.28
  - Between-person correlations are much larger: worried–sad .85, frustrated–worried .84, frustrated–sad .75, calm–happy .71, calm–frustrated −.73 [PM-full]. **Within-person values are the ones to use for momentary co-occurrence.**
  - Factor analysis of 12 whole-day items (Table 3) — [PM-full]:
    - Factor 1, positive: calm .62, happy .72, enthusiastic .79, content .72, interested .74.
    - Factor 2, negative arousal: stressed .80, frustrated .78, worried .67, angry .66, sad .58.
    - Factor 3: **lonely .735, bored .685**, with sad cross-loading .33.
    - Calm also loads −.43 on the negative factor.
- **Moeller, Ivcevic, Brackett & White 2018 (Emotion 18:1106; PMID 29389203; doi 10.1037/emo0000419)**, high-school students: N = 21,678 retrospective and N = 472 experience sampling. Within-person co-occurrence networks showed "frequent co-occurrences between both positive and negative emotions". **"Happy, tired, and stressed were among the most frequent emotions that occurred together with emotions of opposite valence"** — [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/29389203/) [PM-abs]. A 2016 preprint version reportedly named tired, stressed and bored as the most frequently mentioned feelings, with 75% of open-ended feelings negative — [web summary](https://osf.io/8mj84) [web; preprint, unverified against the published paper].
- **Grossmann et al. 2016 (JPSP; PMID 26692354; doi 10.1037/pspp0000084)**: the prevalence of mixed positive–negative emotions differs across cultures and is explained more by interdependence than by dialecticism. The abstract gives no prevalence numbers — [PubMed](https://pubmed.ncbi.nlm.nih.gov/26692354/) [PM-abs].
- **Shin et al. 2022 (Br J Clin Psychol; PMID 33963538; PMC8572316)**, EMA (9/day × 8 days, N = 119) and daily diary (50 days, N = 169). Greater negative-emotion network density and lower positive-emotion network density predicted anxiety/depression diagnoses at the intra-day level only — [PubMed](https://pubmed.ncbi.nlm.nih.gov/33963538/) [PM-abs]. In other words, negative emotions "carry over" into one another more in clinical groups.
- **Vansteelandt, Van Mechelen & Nezlek 2005 (J Res Pers 39:325–335)**, "The co-occurrence of emotions in daily life: a multilevel approach". Its framework predicts that same-valence emotions blend and opposite-valence emotions are discrete. Pair-level results could not be retrieved — [author page](https://jbnezl.people.wm.edu/abstract/co-occur.html) [web].
- **Cowen & Keltner 2017 (PNAS; PMID 28874542; doi 10.1073/pnas.1702247114)**: 27 categories with fuzzy boundaries and continuous gradients, e.g. "anxiety to fear to horror", "calmness to aesthetic appreciation to awe". These are similarity gradients for video-elicited states, not everyday co-occurrence rates — [PubMed](https://pubmed.ncbi.nlm.nih.gov/28874542/) [PM-abs].

### Inferences
- With binary presence, roughly 1 sampled moment in 3 is mixed-valence. A detector returning two moderately high scores of opposite valence (e.g. anxious + content) is therefore normal, not noise.
- In everyday data, anxious is the negative state most likely to sit alongside positive states (Trampe), and tired and stressed are the negative states that most often co-occur with happiness (Moeller). For the app, **anxious + content**, **tired + content** and **stressed + content** are realistic mixed pairs to support.
- Lonely + bored should be treated as a natural cluster (a "disconnected / under-stimulated" state). The Lucas factor structure separates it from the stressed / anxious / angry / sad "tense distress" cluster.

### Gaps
- No published pairwise matrix for the 12 classes was obtained. The single most valuable missing artefact is Trampe et al.'s S1 Table and its OSF data (18 × 18 phi coefficients, >11,000 people), blocked here; it would give anxious, sad, angry and joy/satisfaction pairs directly.
- Kuppens-style ESM valence–arousal studies and PANAS-X intercorrelations were not retrieved.
- No ESM study found reports within-person correlations involving tired, bored, lonely, restless, energetic or neutral alongside stressed/anxious.
- Thayer's "tense-tiredness" state (high tension + low energy) is described in his book *The Origin of Everyday Moods* (1996) [memory], but no prevalence figure was found. Thayer 1987 (PMID 3820066) only shows that a sugar snack raised tension at 1 h and tiredness later, while a 10-min walk raised energy and lowered tension, in 18 people [PM-abs].

---

## 2. Mood-scale intercorrelations (POMS, BRUMS, DASS, PANAS)

### Takeaway
On standard mood scales, the negative states are strongly intercorrelated:
- DASS stress, anxiety and depression r ≈ .77–.83.
- POMS/BRUMS dejection, anger, tension and fatigue r ≈ .37–.75.

Fatigue ties most closely to dejection (POMS r = .73 in the German general population). Vigor is only weakly or moderately negatively related to the negative states (−.06 to −.46).

### Cited Findings
- **Petrowski et al. 2021 (Front Psychol 12:631668; PMID 34135805; PMC8200627)**, representative German general population, N = 2,006, POMS-35 (four scales: dejection, vigor, fatigue, anger; no tension scale). Observed correlations — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8200627/) [PM-full]:
  - **dejection–fatigue .733**, **dejection–anger .754**, **fatigue–anger .612**
  - vigor–fatigue −.461, vigor–dejection −.382, vigor–anger −.167
  - Latent correlations are higher (e.g. dejection–anger .82, dejection–fatigue .78).
- **Quartiroli, Terry et al. 2017, Italian Mood Scale (ITAMS = Italian BRUMS) (Front Psychol 8:1483; PMID 28936185; PMC5594224)**, N = 950 sport participants. Subscale correlations — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5594224/) [PM-full]:
  - **tension–anger .65**, **tension–depression .63**, **anger–depression .65**
  - tension–fatigue .42, depression–fatigue .38, anger–fatigue .37
  - vigor–fatigue −.31, vigor–depression −.22, vigor–tension −.11, vigor–anger −.06
  - ITAMS depression–DASS depression .62; ITAMS tension–PANAS NA .74.
- **Kakemam et al. 2022, Persian DASS-21 (BMC Health Serv Res; PMID 35078477; PMC8789546)**, health professionals, n = 1,135: **depression–anxiety .77, depression–stress .83, anxiety–stress .82** — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8789546/) [PM-full]. This is a stressed occupational group, so the values may be above general-population levels.
- **Henry & Crawford 2005 (Br J Clin Psychol; PMID 16004657; doi 10.1348/014466505X29657)**, UK non-clinical, N = 1,794. The best-fitting DASS-21 model is a general distress factor plus specific depression, anxiety and stress factors — [PubMed](https://pubmed.ncbi.nlm.nih.gov/16004657/) [PM-abs]. Scale intercorrelations were not in the abstract.
- **Nyenhuis et al. 1999 (J Clin Psychol; PMID 10100834)**: US POMS norms, adults N = 400 and older adults N = 170. Intercorrelations were not in the abstract — [PM-abs].

### Inferences
- Sad + tired (r ≈ .7 on POMS in the general population) and sad + angry (≈ .65–.75) are as realistic as sad + anxious. The app should treat "low and drained" and "irritable-low" as default combinations, not edge cases.
- Stressed / anxious / sad move together strongly on the DASS. The detector will often fire all three; one "tense distress" rule family is justified.
- Energetic is only weakly opposed to angry (−.06 to −.17) and to tension (−.11). Energetic + angry and energetic + stressed (Thayer's "tense-energy") are plausible. Energetic + tired is the only clearly antagonistic pair (−.31 to −.46).

### Gaps
- No normative POMS table with tension included was retrieved (the German POMS-35 omits tension). PANAS-X fatigue/serenity/hostility intercorrelations were not retrieved.

---

## 3. Clinical and sub-clinical co-occurrence rates

### Takeaway
Clinically, sad + anxious is the dominant combination: roughly two-thirds to three-quarters comorbidity in both directions. Fatigue appears in about 80–95% of depression and GAD cases. Restlessness/agitation is near-universal in GAD (≈92%). Irritability/anger accompanies about half of major depressive episodes (54.5%) and about three-quarters of GAD. Loneliness correlates about r = .40–.50 with depression and anxiety, and in highly lonely people about 29% meet thresholds for depression, anxiety and anger together.

### Cited Findings
- **Anxiety + depression (NESDA)**: of people with a depressive disorder, **67% had a current and 75% a lifetime anxiety disorder**; of people with an anxiety disorder, **63% had a current and 81% a lifetime depressive disorder**; N = 1,783. Anxiety preceded depression in 57% of comorbid cases — Lamers et al. 2011, J Clin Psychiatry 72(3):341–348 — [web summary of abstract](https://research.rug.nl/en/publications/comorbidity-patterns-of-anxiety-and-depressive-disorders-in-a-lar/) [web]. The PMID could not be confirmed (a PubMed title search returned 0 hits).
- **GAD + MDD in primary care (CALM sample)**: Zbozinek et al. 2012, Depress Anxiety; PMID 23184657; PMC3629816; doi 10.1002/da.22026 — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3629816/) [PM-full].
  - Group sizes: GAD+MDD N = 671, GAD-only N = 298, MDD-only N = 249. Derived: **72.9% of MDD cases had GAD**; **69.2% of GAD cases had MDD**.
  - Symptom endorsement in GAD-only (Table 2): psychomotor agitation 91.6% (→ restless), **fatigue 81.2%**, **irritability 74.2%**, muscle tension 95%, sleep difficulty 81.5%.
  - In GAD+MDD (Table 2): fatigue 92.4%, irritability 84.5%, agitation 93.7%.
  - MDD symptoms (Table 3): MDD-only **fatigue 92.8%**, psychomotor agitation/retardation 84.3%, depressed mood 75.9%; GAD+MDD fatigue 94.2%.
- **Irritability/anger in depression**: overt irritability/anger in **54.5% (292/536)** of unipolar major depressive episodes at intake. It was associated with greater severity, chronicity and comorbid anxiety — Judd et al. 2013, JAMA Psychiatry; PMID 24026579; doi 10.1001/jamapsychiatry.2013.1957 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/24026579/) [PM-abs].
- **Fatigue in depression (adolescents)**: clinically significant fatigue in **73%** of 465 adolescents with MDD (IMPACT trial) — Higson-Sweeney et al. 2026, BMC Psychol; PMID 42286687; doi 10.1186/s40359-026-04942-3 [PM-abs].
- **Burnout (stress + exhaustion) with depression and anxiety**: burnout–depression **r = .520** (95% CI .492–.547), burnout–anxiety **r = .460** (.421–.497); studies 2007–2018. Effects were lower in studies using the MBI and in higher-quality studies — Koutsimani, Montgomery & Georganta 2019, Front Psychol; PMID 30918490; doi 10.3389/fpsyg.2019.00284 [PM-abs].
- **Loneliness + depression**: meta-analysis of 88 studies, N = 40,068, "moderately significant effect" — Erzen & Çikrikci 2018, Int J Soc Psychiatry; PMID 29792097; doi 10.1177/0020764018776349 [PM-abs]. The pooled value **r = 0.50** is reported only by a secondary source citing it (Dunn & Sicouri) — [web](https://econpapers.repec.org/RePEc:sae:socpsy:v:64:y:2018:i:5:p:427-435) [web].
- **Loneliness + depression / anxiety (COVID-era meta-analysis)**: 73 studies; pooled **r = 0.49 (depression), 0.40 (anxiety), 0.38 (PTSS)**; I² ≈ 98–99% — Gabarrell-Pascuet et al. 2023, IJERPH 20(4):2765; PMID 36833463; PMC9957328 — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9957328/) [PM-full]. The same paper cites a systematic review giving loneliness–anxiety r = 0.42 [PM-full, secondary].
- **Loneliness + depression + anxiety + anger (Korea national survey)**: N = 2,699; UCLA loneliness, PHQ-9, GAD-7, PROMIS-Anger. 20.7% had moderately high and 2.1% high loneliness. Adjusted prevalence at **high loneliness** (Table 1): depression 63.5%, anxiety 51.8%, anger 31.9%; **depression+anxiety 48.1%, depression+anger 30.6%, anxiety+anger 28.8%, all three 28.7%**. At moderately high loneliness: depression+anxiety 27.3%, depression+anger 19.4%, anxiety+anger 22.2%, all three 18.4%. At low loneliness: all ≈0–1% — Cho et al. 2025, BMJ Open; PMID 40633948; PMC12258374; doi 10.1136/bmjopen-2024-088590 — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12258374/) [PM-full]. Note: the abstract also gives "11.8%, 5.9% and 11.8%" for single outcomes among the highly lonely, which conflicts with Table 1. The table values (adjusted) are used here.
- **Loneliness and anger in older adults**: loneliness was the most consistent correlate of depression, anxiety and trait anger (N = 190, Spain). Models explained 27.4%, 23.4% and 17.7% of variance — Ruiz-Sancho et al. 2026, BMC Geriatr; PMID 42141390 [PM-abs].
- **Anxiety–depression latent profiles (clinical)**: in adults with elevated anxiety and/or depression (N = 248), the profiles were:
  - high anhedonic depression with low anxious arousal and general distress: **76.2%**
  - high on all three: **12.9%**
  - low anhedonic depression with elevated anxious arousal and distress: 10.9%

  Profiles did not map onto the primary diagnosis — Adams et al. 2026, Psychiatry Res; PMID 43003023; doi 10.1016/j.psychres.2026.117566 [PM-abs]. Profile labels follow the abstract wording, which is ambiguous.

### Inferences
- Priority clinical triples: **sad + anxious + tired** (fatigue in ≈94% of comorbid GAD+MDD), **sad + anxious + angry** (irritability in ≈85% of comorbid GAD+MDD) and **anxious + restless** (≈92% in GAD).
- **Lonely + sad + anxious (± angry)** is a realistic high-loneliness profile. In the Korean data, about half of highly lonely people screen positive for both depression and anxiety.
- Burnout correlations suggest that **stressed + tired** spills over into sad (r ≈ .52) and anxious (r ≈ .46).

### Gaps
- Kessler NCS-R comorbidity percentages (Kessler 2003 JAMA; Kessler 2005 Arch Gen Psychiatry) could not be verified this session. A specific "72.1% / 59.2%" claim was searched for and **not confirmed**, so it is excluded.
- No meta-analysis of state anger with anxiety or depression was found. No odds ratios for irritability in GAD in the general population were found.

---

## 4. Boredom with loneliness, depression, anxiety and anger

### Takeaway
Boredom and loneliness correlate about r = .36–.57 across six samples. Boredom correlates more strongly with depression (r ≈ .60) than with social anxiety (≈ .42). The link between boredom and anger/aggression is supported experimentally, but no clean r was retrieved.

### Cited Findings
- Hager, Milam et al. 2026 (J Clin Psychol; PMID 42541734; PMC13630348), N = 523; MSBS disengagement, PHQ-9, Mini-SPIN, UCLA-10 — [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/) [PM-full]:
  - **boredom–depression .60**, **boredom–loneliness .53**, **loneliness–depression .52**, boredom–social anxiety .42
  - loneliness–social anxiety .35, depression–social anxiety .39 (all p < .001)
- Yuan, Zhou et al. 2026 (Aust J Psychol; PMID 42807895; PMC13618079): boredom proneness (T1) – loneliness (T2) **r = .57** [PM-full].
- Yan, Yang et al. 2025 (Psychol Res Behav Manag; PMID 39925766; PMC11804224), N = 699 Chinese first-year undergraduates: loneliness–boredom proneness **.48** (T1) and **.50** (T2 same-wave) [PM-full].
- Janke, An et al. 2026 (Innov Aging; PMID 42158459; PMC13180649), older adults: boredom–loneliness **.36**; boredom–negative affect .33; loneliness–negative affect .41 [PM-full].
- Takayama, Uehara et al. 2026 (Health Qual Life Outcomes; PMID 41639676; PMC12958760), Japanese older adults, N = 3,731–4,124, Spearman: boredom proneness–UCLA loneliness **.382**, –GDS-15 depression **.599**, –K6 distress .516 [PM-full].
- Lucas et al. 2018 (above): lonely and bored load on the same day-level factor (.735 and .685) [PM-full].
- **Boredom → aggression**: across 9 studies (total N ≈ 7,600), boredom proneness correlated with sadistic tendencies. Induced boredom increased sadistic behaviour and also reactive aggression (Study 9) — Pfattheicher et al. 2021, JPSP; PMID 33030934; doi 10.1037/pspi0000335 [PM-abs]. Boredom proneness added prediction of driving anger expression beyond trait driving anger (N = 224) — Dahlen et al. 2005, Accid Anal Prev; PMID 15667821 [PM-abs]. Neither abstract gives an r for boredom–anger.
- A 2021 Chinese college sample (N = 590) reportedly found boredom tendency–depression r ≈ 0.65 and –anxiety ≈ 0.56 — [web snippet](https://search.bvsalud.org/gim/resource/es/wpr-909498) [web, unverified]. No meta-analysis of boredom with depression or anxiety was found. A 2026 meta-analysis on digital use reportedly states that none exists [web].

### Inferences
- Bored + lonely is one of the best-evidenced pairs outside the classic distress triad. Bored + sad is also strong, which supports the existing R19/R20 rules and suggests adding a **bored + lonely + sad** check.

### Gaps
- No r was found for bored–angry, bored–tired, bored–restless or bored–stressed. Lekkas 2022 (PMID 34776600) models work fatigue and boredom jointly but reports no correlation between them [PM-abs].

---

## 5. Positive–negative blends (bittersweet, excited + anxious, calm + tired, content + tired, energetic + anxious)

### Takeaway
Mixed-valence moments are common (33% of ESM moments, Trampe), and anxiety is one of the two emotions that most often blends with positive states. Happy + tired and happy + stressed are among the most frequent opposite-valence co-occurrences in adolescents (Moeller). Excited + anxious and bittersweet / nostalgia are well-described phenomena, but **no prevalence or correlation was retrieved** for them, nor for calm + tired or energetic + anxious.

### Cited Findings
- Trampe 2015: 33% mixed moments; anxiety (and love) most often co-occurring with an opposite-valence emotion [PM-full].
- Moeller 2018: happy, tired and stressed were among the most frequent emotions co-occurring with opposite-valence emotions, both within situations and within individuals [PM-abs].
- Lucas 2018: calm–happy within-person r = .44, so calm and content co-occur [PM-full].
- Brooks 2014 (J Exp Psychol Gen; PMID 24364682; doi 10.1037/a0035325): anxiety and excitement are both high-arousal states. Reappraising pre-performance anxiety as excitement ("I am excited") raised felt excitement and performance more than trying to calm down, across karaoke, public speaking and maths tasks [PM-abs]. This supports anxious → energetic/excited as a cheap reappraisal, not a co-occurrence rate.
- Batcho 2020 (Front Psychol; PMID 32547466; doi 10.3389/fpsyg.2020.01186): earlier daily-diary data "highlighted nostalgia's mixed valence" and suggested nostalgia is more strongly associated with negative feelings. Anticipatory nostalgia is linked with sadness and worry. N = 144 [PM-abs].
- Larsen et al. 2001/2011 (bittersweet happy + sad) are already covered in the earlier note and not repeated.

### Inferences
- Realistic mixed pairs to support first: **anxious + content**, **tired + content**, **stressed + content**, **calm + content** (same valence). Excited + anxious maps to energetic + anxious in this taxonomy and is plausible from appraisal theory and Brooks's data, but no frequency is available.

### Gaps
- No co-occurrence statistics were found for calm + tired, content + tired (beyond Moeller's qualitative statement), energetic + anxious, or sad + content in daily life. The Trampe S1 Table would partly answer this for joy/satisfaction × anxiety/sadness.

---

## 6. Network-analysis / latent-profile studies of typical emotion profiles

### Takeaway
Empirical profile work points to three broad recurring profiles:
- a "tense distress" cluster (stressed / anxious / angry / sad)
- a "disconnected" cluster (lonely / bored, sometimes sad)
- a "depleted" pairing (sad / tired, POMS r ≈ .73)

Prevalence of named profiles such as "tense-tired" or "anxious-lonely" in the general population was not found.

### Cited Findings
- Lucas 2018 three-factor DRM structure (positive; stressed / frustrated / worried / angry / sad; lonely / bored) [PM-full].
- Adams 2026 clinical LPA profile prevalences (76.2% / 12.9% / 10.9%) [PM-abs].
- Cho 2025 co-occurrence of depression, anxiety and anger by loneliness level (all-three 28.7% at high loneliness) [PM-full].
- Henry & Crawford 2005: a general distress factor underlies DASS stress, anxiety and depression [PM-abs].
- Shin 2022: emotion-network density (inertia) is higher for negative emotions in anxious/depressed groups [PM-abs].

### Inferences
- A pragmatic grouping for the recommender:
  - (a) tense distress: stressed, anxious, angry, restless
  - (b) low / depleted: sad, tired
  - (c) disconnected: lonely, bored
  - (d) positive / low-arousal: calm, content
  - (e) energetic

  Within-group pairs are high-prior. Cross-group pairs most supported by data: sad × anxious, sad × lonely, tired × stressed/anxious, bored × sad, content × anxious/tired/stressed.

### Gaps
- No ESM latent-profile study naming "tense-tired", "irritable-low" or "anxious-lonely" with population prevalence was retrieved. Searches for POMS/DASS LPA returned only off-topic or clinical-subgroup studies.

---

## Pair prevalence table

Rows are directional where marked. "within-r" = within-person correlation; "r" = between-person or scale-level correlation unless noted.

| emotion_a | emotion_b | emotion_c | measure | value | sample & method | citation | pmid | doi_or_url | verification_tag |
|---|---|---|---|---|---|---|---|---|---|
| (any positive) | (any negative) | | % of moments mixed | 33% | ESM, >11,000 smartphone users, binary 18 mDES items | Trampe et al. 2015 | 26698124 | 10.1371/journal.pone.0145450 | PM-full |
| anxious | content | | qualitative: most frequent opposite-valence co-occurrer | anxiety & love top | ESM, >11,000 | Trampe et al. 2015 | 26698124 | 10.1371/journal.pone.0145450 | PM-full |
| tired | content | | qualitative: among most frequent opposite-valence co-occurrences | "happy, tired, stressed" | ESM N=472 + survey N=21,678 adolescents | Moeller et al. 2018 | 29389203 | 10.1037/emo0000419 | PM-abs |
| stressed | content | | qualitative: among most frequent opposite-valence co-occurrences | "happy, tired, stressed" | ESM N=472 + survey N=21,678 adolescents | Moeller et al. 2018 | 29389203 | 10.1037/emo0000419 | PM-abs |
| anxious | sad | | within-r (worried–sad) | .45 | DRM episodes, PSID DUST adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| angry | anxious | | within-r (frustrated–worried) | .40 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| angry | sad | | within-r (frustrated–sad) | .30 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| calm | content | | within-r (calm–happy) | .44 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| calm | angry | | within-r (calm–frustrated) | −.33 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| calm | anxious | | within-r (calm–worried) | −.24 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| calm | sad | | within-r | −.19 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| content | angry | | within-r (happy–frustrated) | −.35 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| content | anxious | | within-r (happy–worried) | −.28 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| content | sad | | within-r (happy–sad) | −.28 | DRM, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| lonely | bored | | shared factor (loadings) | .735 / .685 (own factor) | whole-day ratings, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| stressed | angry | anxious | shared factor (loadings) | .80 / .66 / .67 (+ sad .58) | whole-day ratings, adults ≥60 | Lucas et al. 2018 | 31182970 | 10.1080/17439760.2018.1497686 | PM-full |
| sad | tired | | r (POMS dejection–fatigue) | .733 | survey, German general population N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| sad | angry | | r (POMS dejection–anger) | .754 | survey, N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| tired | angry | | r (POMS) | .612 | survey, N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| energetic | tired | | r (POMS vigor–fatigue) | −.461 | survey, N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| energetic | sad | | r (POMS vigor–dejection) | −.382 | survey, N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| energetic | angry | | r (POMS vigor–anger) | −.167 | survey, N=2,006 | Petrowski et al. 2021 | 34135805 | 10.3389/fpsyg.2021.631668 | PM-full |
| stressed | angry | | r (BRUMS tension–anger) | .65 | survey, N=950 sport participants (ITAMS) | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| stressed | sad | | r (BRUMS tension–depression) | .63 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| angry | sad | | r (BRUMS anger–depression) | .65 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| stressed | tired | | r (BRUMS tension–fatigue) | .42 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| sad | tired | | r (BRUMS depression–fatigue) | .38 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| angry | tired | | r (BRUMS) | .37 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| energetic | tired | | r (BRUMS vigor–fatigue) | −.31 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| energetic | stressed | | r (BRUMS vigor–tension) | −.11 | survey, N=950 | Quartiroli et al. 2017 | 28936185 | 10.3389/fpsyg.2017.01483 | PM-full |
| sad | anxious | | r (DASS-21 D–A) | .77 | survey, n=1,135 health professionals | Kakemam et al. 2022 | 35078477 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8789546/ | PM-full |
| sad | stressed | | r (DASS-21 D–S) | .83 | survey, n=1,135 | Kakemam et al. 2022 | 35078477 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8789546/ | PM-full |
| anxious | stressed | | r (DASS-21 A–S) | .82 | survey, n=1,135 | Kakemam et al. 2022 | 35078477 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8789546/ | PM-full |
| sad | anxious | | % depressed with current anxiety disorder | 67% (lifetime 75%) | clinical cohort NESDA N=1,783 | Lamers et al. 2011 J Clin Psychiatry | not confirmed | https://research.rug.nl/en/publications/comorbidity-patterns-of-anxiety-and-depressive-disorders-in-a-lar/ | web |
| anxious | sad | | % anxious with current depressive disorder | 63% (lifetime 81%) | clinical cohort NESDA N=1,783 | Lamers et al. 2011 | not confirmed | https://research.rug.nl/en/publications/comorbidity-patterns-of-anxiety-and-depressive-disorders-in-a-lar/ | web |
| sad | anxious | | % MDD with GAD (derived 671/920) | 72.9% | primary care, CALM sample | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| anxious | sad | | % GAD with MDD (derived 671/969) | 69.2% | primary care | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| anxious | restless | | % GAD endorsing psychomotor agitation | 91.6% | clinical, GAD-only N=298 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| anxious | tired | | % GAD endorsing fatigue | 81.2% | clinical, GAD-only N=298 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| anxious | angry | | % GAD endorsing irritability | 74.2% | clinical, GAD-only N=298 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | tired | | % MDD endorsing fatigue | 92.8% | clinical, MDD-only N=249 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | restless | | % MDD endorsing psychomotor agitation/retardation | 84.3% (mixes agitation and slowing) | clinical, MDD-only N=249 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | anxious | tired | % comorbid GAD+MDD with fatigue | 94.2% (MDD criterion) / 92.4% (GAD criterion) | clinical N=671 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | anxious | angry | % comorbid GAD+MDD with irritability | 84.5% | clinical N=671 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | anxious | restless | % comorbid GAD+MDD with psychomotor agitation | 93.7% | clinical N=671 | Zbozinek et al. 2012 | 23184657 | 10.1002/da.22026 | PM-full |
| sad | angry | | % MDE with overt irritability/anger | 54.5% (292/536) | clinical, NIMH CDS | Judd et al. 2013 | 24026579 | 10.1001/jamapsychiatry.2013.1957 | PM-abs |
| sad | tired | | % adolescent MDD with clinically significant fatigue | 73% | clinical trial N=465 | Higson-Sweeney et al. 2026 | 42286687 | 10.1186/s40359-026-04942-3 | PM-abs |
| tired | sad | | r (burnout–depression) | .52 | meta-analysis of surveys 2007–2018 | Koutsimani et al. 2019 | 30918490 | 10.3389/fpsyg.2019.00284 | PM-abs |
| tired | anxious | | r (burnout–anxiety) | .46 | meta-analysis | Koutsimani et al. 2019 | 30918490 | 10.3389/fpsyg.2019.00284 | PM-abs |
| lonely | sad | | pooled r | .50 | meta-analysis 88 studies, N=40,068 | Erzen & Çikrikci 2018 | 29792097 | 10.1177/0020764018776349 | web (r); PM-abs (study) |
| lonely | sad | | pooled r | .49 | meta-analysis 73 studies, COVID-era adults | Gabarrell-Pascuet et al. 2023 | 36833463 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9957328/ | PM-full |
| lonely | anxious | | pooled r | .40 | meta-analysis 73 studies | Gabarrell-Pascuet et al. 2023 | 36833463 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9957328/ | PM-full |
| lonely | sad | | % depression at high loneliness (adjusted) | 63.5% | national survey Korea N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| lonely | anxious | | % anxiety at high loneliness | 51.8% | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| lonely | angry | | % anger at high loneliness | 31.9% | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| lonely | sad | anxious | % depression+anxiety at high loneliness | 48.1% (27.3% moderately high) | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| lonely | sad | angry | % depression+anger at high loneliness | 30.6% | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| lonely | anxious | angry | % anxiety+anger at high loneliness | 28.8% | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| sad | anxious | angry | % all three at high loneliness (lonely as 4th) | 28.7% | national survey N=2,699 | Cho et al. 2025 | 40633948 | 10.1136/bmjopen-2024-088590 | PM-full |
| bored | sad | | r (state boredom–PHQ-9) | .60 | survey N=523 | Hager et al. 2026 | 42541734 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/ | PM-full |
| bored | lonely | | r | .53 | survey N=523 | Hager et al. 2026 | 42541734 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/ | PM-full |
| lonely | sad | | r | .52 | survey N=523 | Hager et al. 2026 | 42541734 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/ | PM-full |
| bored | anxious | | r (boredom–social anxiety) | .42 | survey N=523 | Hager et al. 2026 | 42541734 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/ | PM-full |
| lonely | anxious | | r (loneliness–social anxiety) | .35 | survey N=523 | Hager et al. 2026 | 42541734 | https://pmc.ncbi.nlm.nih.gov/articles/PMC13630348/ | PM-full |
| bored | lonely | | r (boredom proneness T1–loneliness T2) | .57 | longitudinal survey | Yuan et al. 2026 | 42807895 | 10.1080/00049530.2026.2737094 | PM-full |
| bored | lonely | | r (same wave) | .48 (T1), .50 (T2) | survey N=699 undergraduates | Yan et al. 2025 | 39925766 | 10.2147/PRBM.S498142 | PM-full |
| bored | lonely | | r | .36 | survey, older adults | Janke et al. 2026 | 42158459 | 10.1093/geroni/igag024 | PM-full |
| bored | lonely | | Spearman r | .382 | survey N=3,731 older adults Japan | Takayama et al. 2026 | 41639676 | 10.1186/s12955-026-02490-3 | PM-full |
| bored | sad | | Spearman r (BPS–GDS-15) | .599 | survey N=4,124 older adults | Takayama et al. 2026 | 41639676 | 10.1186/s12955-026-02490-3 | PM-full |
| bored | angry | | experimental: induced boredom ↑ aggression | effect, no r | 9 studies, N≈7,600 | Pfattheicher et al. 2021 | 33030934 | 10.1037/pspi0000335 | PM-abs |
| sad | anxious | stressed | latent profile prevalence: high on all three tripartite dimensions | 12.9% (vs 76.2% high anhedonic depression only) | clinical LPA N=248 | Adams et al. 2026 | 43003023 | 10.1016/j.psychres.2026.117566 | PM-abs |

**Pairs with at least some quantitative data (approx. 33 of 66):** stressed–anxious, stressed–angry, stressed–sad, stressed–tired, stressed–energetic, stressed–content (qualitative only), anxious–angry, anxious–restless, anxious–sad, anxious–lonely, anxious–tired, anxious–bored, anxious–calm, anxious–content, angry–sad, angry–lonely, angry–tired, angry–calm, angry–content, angry–energetic, angry–bored (experimental only), restless–sad (clinical only), sad–lonely, sad–tired, sad–bored, sad–calm, sad–content, sad–energetic, lonely–bored, tired–energetic, tired–content (qualitative only), calm–content.

**Pairs with no data found:** every pair involving **neutral** (11 pairs). **restless** with stressed, angry, lonely, tired, bored, calm, content and energetic. stressed–lonely, stressed–bored, stressed–calm; anxious–energetic (Brooks reappraisal only, no co-occurrence rate); lonely–tired, lonely–calm, lonely–content, lonely–energetic; tired–bored, tired–calm; bored–calm, bored–content, bored–energetic; calm–energetic, content–energetic.

**Highest-value missing source:** Trampe et al. 2015 S1 Table ("Co-occurrence of emotions") and the OSF dataset (https://osf.io/h2jp3/). Both were blocked in this session (PMC proof-of-work page; plos.org and osf.io not on the allowlist). They would add ESM phi coefficients for anxiety, sadness, anger, joy, satisfaction and alertness pairs.
