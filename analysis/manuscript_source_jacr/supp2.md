#T Supplement 2. Between-modality models, the selected paired subgroup, and detection stratified by volvulus and age

#N Supplement to: "Routine Ultrasound Reports for Pediatric Intestinal Malrotation Rarely Document Duodenal Landmarks: A Single-Center Audit"

#H1 S2.1 Between-modality comparison (generalized estimating equation)

#TABG

#N GEE logistic model with exchangeable working correlation and patient-level clustering (cluster-robust standard errors); 398 children, 723 preoperative index examinations. An odds ratio (OR) below 1 indicates lower report-level detection than the UGI series. These estimates describe indication-driven detection under routine test selection and are **not** estimates of comparative diagnostic accuracy: the modality coefficients absorb the indication for the test, its position in the diagnostic pathway and the content of the examination, which cannot be separated in these data.

#N The pre-specified modality-by-volvulus interaction could not be estimated across all three modalities. No ultrasound examination was positive among the five children without volvulus, so the model exhibits complete separation and does not converge; any p value from such a fit is uninterpretable and none is reported. For the estimable UGI-versus-CT comparison the interaction OR was 0.92 (95% CI 0.32–2.66, p=0.87), that is, the CT-versus-UGI difference did not vary with volvulus.

#H1 S2.2 The selected subgroup receiving all three examinations

#TABP

#N This subgroup was assembled by diagnostic uncertainty, not by sampling: 96.6% had midgut volvulus, 83.1% were neonates and 62.7% were operated on in 2019–2026, compared with 87.9%, 67.3% and 29.5% of the other 339 imaged children. It describes which examination named the diagnosis most often among children investigated intensively enough to receive all three, and is **not** a population-level comparison of test accuracy.

#N The interval is that between the first and last of the three examinations (median 0.9 days, interquartile range 0.6–1.6). Because active volvulus and its imaging signs can evolve over such an interval, the analysis is repeated in the subsets in which all three examinations fell within 48 h and within 24 h. Restricting to near-simultaneous examinations did not weaken the pattern, although no timing restriction can undo the selection that defines the subgroup. Discordant pairs are shown as first-positive/second-positive.

#FIGP

#N **Figure S1. Detection in the selected subgroup receiving all three examinations.** Report-level detection in the 59 children who underwent all three examinations preoperatively, shown for the whole subgroup and for the subsets in which all three fell within 48 h and within 24 h. Error bars are Wilson 95% confidence intervals.

#H1 S2.3 Detection stratified by midgut volvulus and by age category

#TABS2

#N Wilson 95% confidence intervals. All strata are computed among children with surgically confirmed malrotation who received that index test, and are not sensitivities. Note the ultrasound / volvulus-absent cell (0 of 5): ultrasound was performed in only 5 of the 53 children in the cohort who had malrotation without volvulus, and the corresponding interaction model does not converge because of this complete separation. No directional conclusion about ultrasound in uncomplicated malrotation can be drawn from these data.

#H1 S2.4 Detection of a volvulus-specific sign among children with confirmed midgut volvulus

#TABS2B

#N The sign is modality-specific. For ultrasound it is the whirlpool as coded by the two independent readers (Supplement 1, Section K), so the rate is identical to the whirlpool figure quoted in the manuscript (59 of 112). For CT it is a whirlpool or spiral appearance and for the upper gastrointestinal series a corkscrew or spring appearance, coded by the negation-aware patterns of the content audit (Supplement 1, Section H). Ultrasound and the UGI series reported such a sign at similar rates and both more often than CT, but the comparison is between different children, uses different coding methods and is not adjusted; it is reported as exploratory and no claim of a difference between modalities is made.

#N The finding that survives this sensitivity analysis is directional rather than comparative. Within ultrasound, the whirlpool sign was both the dominant documented finding and the near-exclusive determinant of a positive report (main manuscript, Table 3), consistent with its being a sign of volvulus rather than of malrotation.

#H1 S2.5 Sensitivity to the three principal analytic choices

#N **The era boundary.** The primary analysis splits the study period at 2019, but the department attributes the change in practice to growing awareness from about 2021. Table S9 repeats the ultrasound model with the boundary at 2019, 2020, 2021 and 2022. The crude era effect is unstable across boundaries, reaching conventional significance only with the boundary at 2020 and falling short of it at 2019, 2021 and 2022; the examination-type effect is stable throughout (odds ratio 3.21–4.04, all p≤0.005) and the adjusted era term is non-significant at every boundary. The association of examination type with detection therefore does not depend on where the boundary is placed, whereas the crude era difference does, and it does not survive a boundary chosen to match the department's own account. This is why the manuscript treats the temporal analysis as exploratory.

#TABS4

#N Odds ratios and average marginal effects are both shown because a conditional odds ratio attenuates when a predictive covariate is added even in the absence of mediation. On the risk-difference scale, adding the examination-type variable reduces the era difference by about half at the 2019 and 2020 boundaries and by most of it at 2021 and 2022; this describes attenuation, not mediation.

#N **The index unit.** The primary analysis takes the examination episode closest to operation. Table S10 repeats the ultrasound content audit taking the earliest preoperative episode instead. No conclusion changes: the duodenal landmarks remain documented in three of 117 examinations either way. The earliest episode was the same session as the closest in 106 children and inherits the two readers' coding. The other 11 earlier episodes were not read by them; none mentions D3, the duodenojejunal junction, the mesenteric vessels or enteric fluid, and two describe vessels encircling a mass, counted as a whirlpool.

#TABS5

#N **The definition of midgut volvulus.** The primary definition accepts an explicit operative statement of torsion or any documented degree of midgut or mesenteric rotation, with no minimum. Of the 397 children with volvulus, 322 had a stated degree (303 of at least 360° and 19 of 90–270°) and 75 had a torsion statement with no angle recorded. Table S11 tightens the definition in two ways: excluding only the 19 children whose record states a rotation below 360°, and additionally requiring a stated degree, which also excludes the 75 with no angle recorded. The second is not simply stricter, since it removes children for incomplete operative documentation rather than for a lesser degree of torsion; both are therefore shown.

#TABS6

#N Excluding the 19 children with a rotation below 360° lowers volvulus prevalence from 88.2% to 84.0% in the cohort and from 95.7% to 88.0% among the children who underwent ultrasound; additionally requiring a stated degree lowers it to 67.3% and 75.2%. Neither changes the manuscript's claims. The whirlpool sign remains documented in about half of the children with confirmed volvulus under all three definitions (52.7%, 54.4% and 59.1%), so the finding that ultrasound recorded a whirlpool in only about half of the children whose operation confirmed volvulus does not depend on where the definition is drawn. The group with malrotation but no volvulus remains too small under any definition for a conclusion about ultrasound in uncomplicated malrotation.

#H1 S2.6 Analyses added in response to statistical review

#N **Average marginal effects with confidence intervals.** The manuscript reports the era effect on the risk-difference scale because a conditional odds ratio attenuates when a predictive covariate is added even without mediation. Table S12 gives those marginal effects with percentile bootstrap 95% confidence intervals (2,000 resamples of children, seed fixed). For ultrasound, neither interval excludes zero: the crude effect's lower bound falls at −0.2 percentage points, so the era difference is itself imprecise, and the two intervals overlap heavily. On the point estimates, adding examination type reduces the era difference by more than half; this does not show that booking mediates the change, nor that the remainder is absent.

#TABS11

#N **Paired differences with confidence intervals.** Table S13 replaces the p-value-only presentation of the three-modality subgroup with the paired difference in detection and its bootstrap interval alongside the discordant pairs and the exact McNemar p. The UGI series exceeded both other modalities; ultrasound and CT did not differ. These are within-subgroup differences in what the report said, in 59 children selected by diagnostic uncertainty, and are not differences in accuracy.

#TABS12

#N **The separated contrast, and interaction terms.** The pre-specified modality-by-volvulus interaction cannot be estimated in the three-modality model because no ultrasound examination was positive among the five children without volvulus. Two things can be estimated and are given in Table S14. First, the same interaction restricted to the upper gastrointestinal series and CT, where no separation occurs, shows no evidence of effect modification by volvulus. Second, a Firth penalized logistic model of ultrasound detection on volvulus returns a finite estimate. Its interval must be a profile penalized-likelihood interval rather than a Wald one, because under separation the two disagree here: the Wald interval spans 0.60 to 357 and the profile interval 1.60 to 1938 (penalized likelihood-ratio p=0.013). The direction of the contrast is therefore supported, ultrasound having been far more often positive when volvulus was present, while its magnitude is not estimable to any useful precision from five children. With a single binary covariate the Firth estimate has a closed form, the odds ratio after adding 0.5 to each cell of the 2×2 table, (64.5 × 5.5)/(48.5 × 0.5) = 14.6, which the fitted value reproduces. Table S14 also reports era-by-content interaction terms for ultrasound and CT; neither is significant, so the additive models used in Table 4 are not obviously misspecified.

#TABS13

#N **What was pre-specified and what was not.** Pre-specified: the outcome definition, the modality comparison and its GEE structure, the modality-by-volvulus interaction, the era dichotomy at 2019, and the certainty-tier sensitivity analysis. Decided after inspecting the data: the content-audit patterns (fixed by enumerating the corpus vocabulary, Supplement 1), the manual two-reader coding of ultrasound content and the review of anchor operations and examination timing (Supplement 1, Section K), the pooling of same-day reports into one index episode, the era boundary sensitivity analysis, the marginal-effect presentation, and every analysis in this section. The paper's claims should be read accordingly: the content rates and the era analysis are descriptive and hypothesis-generating, not confirmatory tests of pre-registered hypotheses.
