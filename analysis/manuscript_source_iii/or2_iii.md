#T Online Resource 2. Between-modality models, the selected paired subgroup, and detection stratified by volvulus and age

#N Supplement to: "Routine ultrasound reports for intestinal malrotation rarely document duodenal landmarks: an audit of 740 preoperative index examinations in 410 surgically confirmed children"

#H1 S2.1 Between-modality comparison (generalised estimating equation)

#TABG

#N GEE logistic model with exchangeable working correlation and patient-level clustering (cluster-robust standard errors); 410 children, 740 preoperative index examinations. An odds ratio (OR) below 1 indicates lower report-level detection than the UGI series. These estimates describe indication-driven detection under routine test selection and are **not** estimates of comparative diagnostic accuracy: the modality coefficients absorb the indication for the test, its position in the diagnostic pathway and the content of the examination, which cannot be separated in these data.

#N The pre-specified modality-by-volvulus interaction could not be estimated across all three modalities. No ultrasound examination was positive among the six children without volvulus, so the model exhibits complete separation and does not converge; any p value from such a fit is uninterpretable and none is reported. For the estimable UGI-versus-CT comparison the interaction OR was 0.90 (95% CI 0.33–2.43, p=0.84), that is, the CT-versus-UGI difference did not vary with volvulus.

#H1 S2.2 The selected subgroup receiving all three examinations

#TABP

#N This subgroup was assembled by diagnostic uncertainty, not by sampling: 96.6% had midgut volvulus, 83.1% were neonates and 62.7% were operated on in 2019–2026, compared with 86.6%, 65.5% and 31.3% of the other 351 imaged children. It describes which examination named the diagnosis most often among children investigated intensively enough to receive all three, and is **not** a population-level comparison of test accuracy.

#N The interval is that between the first and last of the three examinations (median 0.9 days, interquartile range 0.6–1.6). Because active volvulus and its imaging signs can evolve over such an interval, the analysis is repeated in the subsets in which all three examinations fell within 48 h and within 24 h. Restricting to near-simultaneous examinations did not weaken the pattern, although no timing restriction can undo the selection that defines the subgroup. Discordant pairs are shown as first-positive/second-positive.

#FIGP

#N **Fig. S1 Detection in the selected subgroup receiving all three examinations.** Report-level detection in the 59 children who underwent all three examinations preoperatively, shown for the whole subgroup and for the subsets in which all three fell within 48 h and within 24 h. Error bars are Wilson 95% confidence intervals.

#H1 S2.3 Detection stratified by midgut volvulus and by age category

#TABS2

#N Wilson 95% confidence intervals. All strata are computed among children with surgically confirmed malrotation who received that index test, and are not sensitivities. Note the ultrasound / volvulus-absent cell (0 of 6): ultrasound was performed in only 6 of the 62 children in the cohort who had malrotation without volvulus, and the corresponding interaction model does not converge because of this complete separation. No directional conclusion about ultrasound in uncomplicated malrotation can be drawn from these data.

#H1 S2.4 Detection of a volvulus-specific sign among children with confirmed midgut volvulus

#TABS2B

#N The sign is modality-specific and uses the same negation-aware rules as the main content audit: a whirlpool or spiral appearance for ultrasound and CT, a corkscrew or spring appearance for the upper gastrointestinal series. The rates are therefore identical in definition to the whirlpool figure quoted in the manuscript (58 of 113). Ultrasound and the UGI series reported such a sign at similar rates and both more often than CT, but the comparison is between different children and is not adjusted; it is reported as exploratory and no claim of a difference between modalities is made. An earlier version of this table applied one pooled sign pattern across all three modalities without negation handling, giving 59/113 for ultrasound; the harmonised rule used here is the one implemented in `Online_Resource_1_classifier.py` and in the audit script.

#N The finding that survives this sensitivity analysis is directional rather than comparative. Within ultrasound, the whirlpool sign was both the dominant documented finding and the near-exclusive determinant of a positive report (main manuscript, Table 3), consistent with its being a sign of volvulus rather than of malrotation.

#H1 S2.5 Sensitivity to the three principal analytic choices

#N **The era boundary.** The primary analysis splits the study period at 2019, but the department attributes the change in practice to growing awareness from about 2021. Table S8 repeats the ultrasound model with the boundary at 2019, 2020, 2021 and 2022. The crude era effect is unstable across boundaries and loses significance at 2021 and 2022; the examination-type effect is stable throughout (odds ratio 3.07–3.85, all p≤0.007) and the adjusted era term is non-significant at every boundary. The temporal claim in the manuscript therefore does not depend on where the boundary is placed, and the crude era difference alone does not survive a boundary chosen to match the department's own account.

#TABS4

#N Odds ratios and average marginal effects are both shown because a conditional odds ratio attenuates when a predictive covariate is added even in the absence of mediation. On the risk-difference scale the examination-type variable accounts for roughly half of the era difference at each boundary, not all of it.

#N **The index unit.** The primary analysis takes the examination episode closest to operation. Table S9 repeats the ultrasound content audit taking the earliest preoperative episode instead. No conclusion changes: the duodenal landmarks remain documented in three of 119 examinations either way.

#TABS5

#N **The definition of midgut volvulus.** The primary definition accepts an explicit operative statement of torsion or any documented degree of midgut or mesenteric rotation, with no minimum. Of the 327 children with a stated degree, 308 had a rotation of at least 360° and 19 had 90–270°. Table S10 shows the effect of restricting volvulus to the former.

#TABS6

#N Restricting the definition lowers volvulus prevalence from 86.7% to 82.6% in the cohort and from 95.0% to 87.4% among the children who underwent ultrasound. It does not change the manuscript's claims: the whirlpool sign remains documented in about half of the children with confirmed volvulus under either definition, and the group with malrotation but no volvulus remains too small for any conclusion about ultrasound in uncomplicated malrotation.

#H1 S2.6 Analyses added in response to statistical review

#N **Average marginal effects with confidence intervals.** The manuscript reports the era effect on the risk-difference scale because a conditional odds ratio attenuates when a predictive covariate is added even without mediation. Table S11 gives those marginal effects with percentile bootstrap 95% confidence intervals (2,000 resamples of children, seed fixed). For ultrasound, the crude effect excludes zero and the adjusted effect does not; the two intervals overlap heavily, so the analysis shows that examination type accounts for about half the era difference, not that the remainder is absent.

#TABS11

#N **Paired differences with confidence intervals.** Table S12 replaces the p-value-only presentation of the three-modality subgroup with the paired difference in detection and its bootstrap interval alongside the discordant pairs and the exact McNemar p. The UGI series exceeded both other modalities; ultrasound and CT did not differ. These are within-subgroup differences in what the report said, in 59 children selected by diagnostic uncertainty, and are not differences in accuracy.

#TABS12

#N **The separated contrast, and interaction terms.** The pre-specified modality-by-volvulus interaction cannot be estimated in the three-modality model because no ultrasound examination was positive among the six children without volvulus. Two things can be estimated and are given in Table S13. First, the same interaction restricted to the upper gastrointestinal series and CT, where no separation occurs, shows no evidence of effect modification by volvulus. Second, a Firth penalised logistic model of ultrasound detection on volvulus returns a finite estimate. Its interval must be a profile penalised-likelihood interval rather than a Wald one, because under separation the two disagree here: the Wald interval spans 0.77 to 401 and the profile interval 2.00 to 2310 (penalised likelihood-ratio p=0.006). The direction of the contrast is therefore supported, ultrasound having been far more often positive when volvulus was present, while its magnitude is not estimable to any useful precision from six children. The estimate was reproduced to six decimal places by an independent implementation. Table S13 also reports era-by-content interaction terms for ultrasound and CT; neither is significant, so the additive models used in Table 4 are not obviously misspecified.

#TABS13

#N **What was pre-specified and what was not.** Pre-specified: the outcome definition, the modality comparison and its GEE structure, the modality-by-volvulus interaction, the era dichotomy at 2019, and the certainty-tier sensitivity analysis. Decided after inspecting the data: the content-audit patterns (fixed by enumerating the corpus vocabulary, Online Resource 1), the pooling of same-day reports into one index episode, the era boundary sensitivity analysis, the marginal-effect presentation, and every analysis in this section. The paper's claims should be read accordingly: the content rates and the era analysis are descriptive and hypothesis-generating, not confirmatory tests of pre-registered hypotheses.
