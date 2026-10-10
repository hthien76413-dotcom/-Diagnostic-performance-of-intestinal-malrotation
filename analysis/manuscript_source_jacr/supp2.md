#T Supplement 2. Between-modality models, the selected paired subgroup, and detection stratified by volvulus and age

#N Supplement to: "Routine Ultrasound Reports for Pediatric Intestinal Malrotation Rarely Document Duodenal Landmarks: A Single-Center Audit"

#H1 S2.1 Between-modality comparison (generalized estimating equation)

#TABG

#N GEE logistic model with exchangeable working correlation and patient-level clustering (cluster-robust standard errors); 398 children, 723 preoperative index examinations. An odds ratio (OR) below 1 indicates lower report-level detection than the UGI series. These estimates describe indication-driven detection under routine test selection and are **not** estimates of comparative diagnostic accuracy: the modality coefficients absorb the indication for the test, its position in the diagnostic pathway and the content of the examination, which cannot be separated in these data.

#N The pre-specified modality-by-volvulus interaction could not be estimated across all three modalities. No ultrasound examination was positive among the five children without volvulus, so the model shows complete separation and does not converge; any p value from such a fit is uninterpretable and none is reported. For the estimable UGI-versus-CT comparison the interaction OR was 0.92 (95% CI 0.32–2.66, p=0.87), that is, the CT-versus-UGI difference did not vary with volvulus.

#H1 S2.2 The selected subgroup receiving all three examinations

#TABP

#N This subgroup was presumably assembled by diagnostic uncertainty, not by sampling: 96.6% had midgut volvulus, 83.1% were neonates and 62.7% were operated on in 2019–2026, compared with 87.9%, 67.3% and 29.5% of the other 339 imaged children. It describes which examination named the diagnosis most often among children investigated intensively enough to receive all three, and is **not** a population-level comparison of test accuracy.

#N The interval is that between the first and last of the three examinations (median 0.9 days, interquartile range 0.6–1.6). Because active volvulus and its imaging signs can evolve over such an interval, the analysis is repeated in the subsets in which all three examinations fell within 48 h and within 24 h. Restricting to near-simultaneous examinations did not weaken the pattern, although no timing restriction can remove the selection that defines the subgroup. Discordant pairs are shown as first-positive/second-positive.

#FIGP

#N **Figure S1. Detection in the selected subgroup receiving all three examinations.** Report-level detection in the 59 children who underwent all three examinations preoperatively, shown for the whole subgroup and for the subsets in which all three fell within 48 h and within 24 h. Error bars are Wilson 95% confidence intervals.

#H1 S2.3 Detection stratified by midgut volvulus and by age category

#TABS2

#N Wilson 95% confidence intervals. All strata are computed among children with surgically confirmed malrotation who received that index test, and are not sensitivities. In the ultrasound / volvulus-absent cell (0 of 5), ultrasound was performed in only 5 of the 53 children in the cohort who had malrotation without volvulus, and the corresponding interaction model does not converge because of this complete separation. No directional conclusion about ultrasound in uncomplicated malrotation can be drawn from these data.

#H1 S2.4 Detection of a volvulus-specific sign among children with confirmed midgut volvulus

#TABS2B

#N The sign is modality-specific. For ultrasound it is the whirlpool as coded by the two independent readers (Supplement 1, Section K), so the rate is identical to the whirlpool figure quoted in the manuscript (59 of 112). For CT it is a whirlpool or spiral appearance and for the upper gastrointestinal series a corkscrew or spring appearance, coded by the negation-aware patterns of the content audit (Supplement 1, Section H). Ultrasound and the UGI series reported such a sign at similar rates and both more often than CT, but the comparison is between different children, uses different coding methods and is not adjusted; it is reported as exploratory and no claim of a difference between modalities is made.

#N The finding that survives this sensitivity analysis is directional rather than comparative. Within ultrasound, the whirlpool sign was both the most often documented finding and the finding described in almost all positive reports (main manuscript, Table 3), consistent with its being a sign of volvulus rather than of malrotation.

#H1 S2.5 Sensitivity to the three principal analytic choices

#N **The era boundary.** The primary analysis splits the study period at 2019. Table S9 repeats the ultrasound model with the boundary at 2019, 2020, 2021 and 2022. The crude era effect is unstable across boundaries, reaching conventional significance only with the boundary at 2020 and falling short of it at 2019, 2021 and 2022; the examination-type effect is stable throughout (odds ratio 3.21–4.04, all p≤0.005) and the adjusted era term is non-significant at every boundary. The association of examination type with detection therefore does not depend on where the boundary is placed, whereas the crude era difference does. This is why the manuscript treats the temporal analysis as exploratory.

#TABS4

#N Odds ratios and average marginal effects are both shown because a conditional odds ratio attenuates when a predictive covariate is added even in the absence of mediation. On the risk-difference scale, adding the examination-type variable reduces the era difference by about half at the 2019 and 2020 boundaries and by most of it at 2021 and 2022; this describes attenuation, not mediation.

#N **The index unit.** The primary analysis takes the examination episode closest to operation. Table S10 repeats the ultrasound content audit taking the earliest preoperative episode instead. No conclusion changes: the duodenal landmarks remain documented in three of 117 examinations either way. The earliest episode was the same session as the closest in 106 children and inherits the two readers' coding. The other 11 earlier episodes were not read by them; none mentions D3, the duodenojejunal junction, the mesenteric vessels or enteric fluid, and two describe vessels encircling a mass, counted as a whirlpool.

#TABS5

#N **The definition of midgut volvulus.** The primary definition accepts an explicit operative statement of torsion or any documented degree of midgut or mesenteric rotation, with no minimum. Of the 397 children with volvulus, 322 had a stated degree (303 of at least 360° and 19 of 90–270°) and 75 had a torsion statement with no angle recorded. Table S11 tightens the definition in two ways: excluding only the 19 children whose record states a rotation below 360°, and additionally requiring a stated degree, which also excludes the 75 with no angle recorded. The second is not simply stricter, since it removes children for incomplete operative documentation rather than for a lesser degree of torsion; both are therefore shown.

#TABS6

#N Excluding the 19 children with a rotation below 360° lowers volvulus prevalence from 88.2% to 84.0% in the cohort and from 95.7% to 88.0% among the children who underwent ultrasound; additionally requiring a stated degree lowers it to 67.3% and 75.2%. Neither changes the manuscript's claims. The whirlpool sign remains documented in about half of the children with confirmed volvulus under all three definitions (52.7%, 54.4% and 59.1%), so the finding that ultrasound recorded a whirlpool in only about half of the children whose operation confirmed volvulus does not depend on where the definition is drawn. The group with malrotation but no volvulus remains too small under any definition for a conclusion about ultrasound in uncomplicated malrotation.

#H1 S2.6 Marginal effects, paired differences, the separated contrast and interaction terms

#N **Average marginal effects with confidence intervals.** The manuscript reports the era effect on the risk-difference scale because a conditional odds ratio attenuates when a predictive covariate is added even without mediation. Table S12 gives those marginal effects with percentile bootstrap 95% confidence intervals (2,000 resamples of children, seed fixed). For ultrasound, neither interval excludes zero: the crude effect's lower bound falls at −0.2 percentage points, so the era difference is itself imprecise, and the two intervals overlap heavily. On the point estimates, adding examination type reduces the era difference by more than half; this does not show that booking mediates the change, nor that the remainder is absent.

#TABS11

#N **Paired differences with confidence intervals.** Table S13 replaces the p-value-only presentation of the three-modality subgroup with the paired difference in detection and its bootstrap interval alongside the discordant pairs and the exact McNemar p. The UGI series exceeded both other modalities; ultrasound and CT did not differ. These are within-subgroup differences in what the report said, in 59 children presumably selected by diagnostic uncertainty, and are not differences in accuracy.

#TABS12

#N **The separated contrast, and interaction terms.** The pre-specified modality-by-volvulus interaction cannot be estimated in the three-modality model because no ultrasound examination was positive among the five children without volvulus. Two things can be estimated and are given in Table S14. First, the same interaction restricted to the upper gastrointestinal series and CT, where no separation occurs, shows no evidence of effect modification by volvulus. Second, a Firth penalized logistic model of ultrasound detection on volvulus returns a finite estimate. Its interval must be a profile penalized-likelihood interval rather than a Wald one, because under separation the two disagree here: the Wald interval spans 0.60 to 357 and the profile interval 1.60 to 1938 (penalized likelihood-ratio p=0.013). The direction of the contrast is therefore supported, ultrasound having been far more often positive when volvulus was present, while its magnitude is not estimable to any useful precision from five children. With a single binary covariate the Firth estimate has a closed form, the odds ratio after adding 0.5 to each cell of the 2×2 table, (64.5 × 5.5)/(48.5 × 0.5) = 14.6, which the fitted value reproduces. Table S14 also reports era-by-content interaction terms for ultrasound and CT; neither is significant, so the additive models used in Table 4 are not obviously misspecified.

#TABS13

#N **What was pre-specified and what was not.** Pre-specified: the outcome definition, the modality comparison and its GEE structure, the modality-by-volvulus interaction, the era dichotomy at 2019, and the certainty-tier sensitivity analysis. Decided after inspecting the data: the content-audit patterns (fixed by enumerating the corpus vocabulary, Supplement 1), the manual two-reader coding of ultrasound content and the review of anchor operations and examination timing (Supplement 1, Section K), the pooling of same-day reports into one index episode, the era boundary sensitivity analysis, the marginal-effect presentation, and every analysis in this section and in S2.7 to S2.10. The paper's claims should be read accordingly: the content rates and the era analysis are descriptive and hypothesis-generating, not confirmatory tests of pre-registered hypotheses.

#H1 S2.7 Effect sizes and the definition of a positive report

#N Table S4 is repeated in Tables S16 and S17 with the primary definition of a positive report and with three others: a conclusion that names malrotation (Table 2, last column), possible-tier conclusions counted negative, and the label returned by the published conclusion-only classifier (Supplement_1_classifier.py), which agrees with the final label in 716 of 723 index examinations. Every model has the specification of Table S4: GEE, exchangeable correlation, era and three age categories. Table S17 gives detection standardized to the 398 children who underwent at least one index test, that is, the detection each modality would show if every child had undergone it, with the observed distribution of era and age. Its intervals are percentile intervals from 2,000 resamples of children (seed 20261010), the model being refitted in each. Because detection is common, odds ratios exaggerate the absolute differences, and the standardized differences are the measure to read.

#TABHP16

#TABHP17

#N Adjusted for era and age, detection under the primary definition was 25.5 percentage points lower for CT than for the UGI series (95% CI −32.2 to −18.8) and 26.4 lower for ultrasound (−35.9 to −16.8); CT and ultrasound did not differ (−0.9, −10.5 to +8.7). The difference from the UGI series was present under all four definitions. The relation between CT and ultrasound was not. When possible-tier conclusions were counted negative, ultrasound was 8.7 percentage points lower than CT (−16.9 to −0.5; adjusted odds ratio 0.62, 0.38–1.01), whereas under the primary definition and the other two the odds ratios were 0.96, 1.05 and 0.97. Tentative wording was more frequent among positive ultrasound reports (53.1%) than among positive CT reports (37.6%) or UGI reports (36.1%; Table 2), which is why the comparison of CT with ultrasound depends on how that wording is counted. These estimates describe reporting among children who underwent each test and are not estimates of accuracy; the models adjust for neither the indication nor the position of the test in the pathway.

#H1 S2.8 Timing of the index examination and the choice of index examination

#N Operative times are recorded as dates only, so the intervals in Table S18 are calendar days. The index examination was a median of 2 days before operation for the UGI series and CT and 1 day for ultrasound; 4.1%, 2.9% and 4.3% were more than 7 days before. Detection within 2 calendar days of operation (186, 196 and 89 examinations) was 79.6%, 56.6% and 57.3%, and the adjusted odds ratios were close to those of Table S4 (CT 0.33, 95% CI 0.21–0.51; ultrasound 0.28, 0.16–0.48; ultrasound against CT 0.87, 0.55–1.38). Only 28 child-modality combinations had more than one preoperative episode (UGI series 6, CT 11, ultrasound 11), so the choice of index examination can change at most these. Labeled by the conclusion-only classifier, detection with the closest episode was 228, 161 and 63; with the earliest 225, 158 and 60; and when a child counted as detected if any preoperative episode was positive, 228, 161 and 64. The final adjudicated label exists only for the closest episode, so these three definitions are compared with one another under the classifier and not with the final label.

#TABHP18

#H1 S2.9 Ultrasound content by booking category

#N The booking category is the only indicator of the purpose of the examination, because the indication on the request was not retrievable. Table S19 gives the documentation of four elements, and the proportion of positive reports, by booking category and in two further denominators: examinations booked as gastrointestinal or great-vessel studies, and children aged 28 days or younger. The three examinations that documented D3 or the duodenojejunal junction were all among the 112 booked as gastrointestinal or great-vessel studies (2.7%, 95% CI 0.9–7.6). The five booked only as pyloric studies documented none of the elements, so excluding them does not change the finding. Among the 90 children aged 28 days or younger, in whom an examination directed at malrotation is most likely, D3 or the junction was documented in 2 (2.2%, 0.6–7.7). Booking categories overlap (Table 3), so the first three rows of Table S19 are not exclusive.

#TABHP19

#N These four analyses were decided after the principal analyses had been run and the results were inspected; each was run once and every result is shown. They leave the principal findings unchanged: D3 or the duodenojejunal junction was documented in between 2.2% and 3.0% of ultrasound examinations in the whole series, in each of the two main booking categories and in neonates, and detection by CT and ultrasound was lower than that by the UGI series by 17.1 to 28.9 percentage points under every definition of a positive report. They do not address the selection of the cohort, the part that imaging plays in the decision to operate, or the missing indication, none of which can be removed by any analysis of these data.
