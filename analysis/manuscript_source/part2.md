#H2 Statistical analysis

#N Report-level detection rates are presented with Wilson 95% confidence intervals (CIs) and with their denominators shown wherever the rate appears, including in figures. Characteristics of the children who received each index test, and of those who received none, are tabulated to display confounding by indication directly rather than to adjust it away.

#N Between-modality comparison used a generalised estimating equation (GEE) logistic model [16] with detection as the outcome, modality as the predictor (UGI series as reference), patient-level clustering, an exchangeable working correlation and cluster-robust standard errors, fitted to all children with at least one index test, then refitted with adjustment for era of operation (2012–2018 vs 2019–2026) and age category (≤28 days, 29 days–1 year, >1 year). These odds ratios describe indication-driven detection under routine test selection; adjustment for the few recorded covariates cannot remove confounding by indication.

#N A modality-by-volvulus interaction was pre-specified but could not be estimated across all three modalities: no ultrasound examination was positive among the six children without volvulus, producing complete separation and non-convergence of the full interaction model. We therefore report the interaction only for the comparison that is estimable (UGI series vs CT), present volvulus-stratified detection rates with exact CIs for all three modalities, and make no claim about interaction involving ultrasound.

#N As a confirmatory analysis restricted to children who received all three modalities, detection was compared with Cochran's Q and the exact McNemar test. Because the interval between examinations allows the disease state to evolve, this analysis was repeated in the subsets in which all three examinations fell within 48 h and within 24 h.

#N Determinants of the temporal change in detection were examined with modality-specific logistic models of detection on era, before and after adding the report-content variable specific to that modality (for ultrasound, whether the examination was recorded as a mesenteric-vessel study; for CT, contrast enhancement). Attenuation of the era coefficient after adding the content variable was interpreted as evidence that the temporal change operated through examination content rather than through calendar time.

#N Given the exploratory nature of the subgroup and content analyses, p values were not adjusted for multiplicity, and all subgroup findings are reported as hypothesis-generating. Analyses used Python 3.12 (statsmodels 0.15, SciPy 1.17).

#H1 Results

#H2 Cohort, and what the children without an index test actually received

#N Between December 2012 and June 2026, 465 children with surgically confirmed intestinal malrotation were included; 352 (75.7%) were male, the median age at operation was 13 days (interquartile range [IQR] 7 days to 2.8 months, range 0–14.2 years), 302 (64.9%) were neonates and 93 (20.0%) were older than 1 year. Midgut volvulus was documented at operation in 403 (86.7%). A preoperative index examination was available in 301 children for the UGI series, 320 for abdominal CT and 119 for ultrasound; 410 children had at least one (740 index examinations) and 59 had all three. Characteristics are shown in Table 1 and the study flow in Fig. 1.

#TAB1

#FIG1

#N Fifty-five children (11.8%) had none of the three index examinations. This does not mean that they were operated on without imaging: every one of them had preoperative imaging of some kind (Fig. 1). Forty-six had radiographs (44 including the abdomen), 12 had a contrast enema of the colon, 22 had ultrasound of another region and 7 had CT of another region. Only 5 had no in-hospital preoperative study of any type, and the admission record of each of those 5 documented imaging performed before transfer, three of which had already reported malrotation or volvulus. Across all 55, the admission record documented prior outside or outpatient imaging in 33, and that imaging had already reported malrotation or volvulus in 19. These children were operated on after the diagnosis had been made or strongly suggested elsewhere, or after a radiograph and contrast enema in an era when that combination was more often considered sufficient. They differed systematically from the imaged children (Table 1): older (median 63 vs 12 days), less often neonates (41.8% vs 68.0%), less often with documented bilious vomiting (21.8% vs 50.5%) and less often with volvulus (76.4% vs 88.0%). Their exclusion from the index-test denominators is informative missingness, not random loss.

#H2 The three modalities were used in different children

#N The three modality groups were broadly similar in age and sex but were not interchangeable (Table 1). Children who underwent ultrasound had volvulus more often (95.0%, vs 89.0% for the UGI series and 87.8% for CT) and were concentrated in the second era: 67.2% of ultrasound examinations were performed in 2019–2026, against 31.9% of UGI series and 32.8% of CT examinations. Ultrasound utilisation among operated children rose from 13% (39/299) in 2012–2018 to 48% (80/166) in 2019–2026, and no gastrointestinal ultrasound in this cohort predated 2016.

#N Test sequence also differed systematically. Among the 271 children who received more than one modality, CT was the first index test in 183 (67.5%) and the UGI series the last before operation in 184 (67.9%). Per modality, the UGI series was the final preoperative test in 184 of 245 children who received it (75.1%), against 48 of 250 (19.2%) for CT and 39 of 106 (36.8%) for ultrasound; its detection was higher in that position (80.4%) than when another examination followed (70.5%), with no comparable gradient for CT (47.9% vs 54.0%) or ultrasound (53.8% vs 58.2%). The UGI series thus functioned as the confirmatory study immediately preceding operation — a feature of the diagnostic pathway, not a property of the test.

#H2 Report-level detection, and the certainty of the wording

#N Report-level detection among surgically confirmed children was 237/301 (78.7%, 95% CI 73.8–83.0) for the UGI series, 171/320 (53.4%, 48.0–58.8) for abdominal CT and 65/119 (54.6%, 45.7–63.3) for ultrasound (Table 2, Fig. 3). These three proportions are computed on different, indication-selected denominators drawn from overlapping groups of children, and Fig. 3 is annotated accordingly; they should not be read as a ranking of the tests.

#TAB2

#FIG3

#N Tentative phrasing was common and differed by modality (Table 2). Of positive conclusions, 78 of 237 (32.9%) UGI, 34 of 171 (19.9%) CT and 16 of 65 (24.6%) ultrasound reports used unqualified wording; a further 32.1%, 43.9% and 26.2% used probable wording, and 35.0%, 36.3% and 49.2% used possible wording ("suspected", "cannot be excluded", "?"). Because every child had surgically confirmed malrotation, none of these tentative conclusions was a false positive: they were correct diagnoses expressed with hedging. Reclassifying all possible-tier conclusions as negative reduced detection to 51.2% (154/301) for the UGI series, 34.1% (109/320) for CT and 27.7% (33/119) for ultrasound, without changing the ordering; the largest proportional reduction fell on ultrasound.

#H2 What the ultrasound reports contained

#N The central finding concerns the content of the 119 ultrasound index reports (Table 3, Fig. 4). Not one documented the third portion of the duodenum or the duodenojejunal junction (0/119, 0%; 95% CI 0–3.1); six (5.0%) mentioned the duodenum at all. Ten (8.4%) described the superior mesenteric artery–vein relationship, and only one (0.8%) stated explicitly that the vessels were inverted, although vessel inversion was one of the two criteria defining a positive ultrasound. One report (0.8%) recorded enteric fluid and four (3.4%) the caecal position. By contrast, 59 (49.6%) recorded a whirlpool, swirl or spiral appearance, and bowel gas was reported as limiting the examination in 26 (21.8%).

#N Detection followed this content almost deterministically. Ultrasound reported malrotation in 59 of the 59 examinations documenting a whirlpool sign (100%, 95% CI 93.9–100) and in 6 of the 60 without one (10.0%, 4.7–20.1); where the mesenteric-vessel relationship was described, 10 of 10 were positive. Detection was 70.5% (43/61) for examinations recorded as abdominal great-vessel studies, 47.1% (32/68) for those recorded as gastrointestinal ultrasound and 22.2% for the nine bedside examinations. In this cohort, ultrasound diagnosed malrotation when, and essentially only when, it saw the twisted pedicle of an active volvulus; the anatomical assessment on which contemporary ultrasound accuracy rests was absent from the record of every examination.

#N The audits of CT and the UGI series show the same principle with different content (Online Resource 3). A mesenteric whirl was described in 116 of 320 CT reports (36.2%), of which 98.3% were positive, against 27.9% of those without. For the UGI series the duodenojejunal junction was described in 164 of 301 reports (54.5%), of which 98.2% were positive, against 55.5% of those without; jejunal position was described in 70.4% and a corkscrew appearance in 46.5%. Detection in each modality was governed by whether the diagnostic landmark was sought and recorded, and the UGI series was the only modality whose routine reports documented the landmark that defines malrotation itself in the majority of examinations.

#TAB3

#FIG4
