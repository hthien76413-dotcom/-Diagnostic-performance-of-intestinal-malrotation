#T Online Resource 1. Text-classification algorithm and report-content audit

#N Supplement to: "Routine ultrasound reports for intestinal malrotation rarely document duodenal landmarks: an audit of 740 preoperative index examinations in 410 surgically confirmed children"

#N Sections A–F specify the classification rules. Section J reports a reference implementation of those rules as a runnable script, together with its agreement with the final adjudicated labels, so that the specification below can be executed rather than only read.

#H1 A. Purpose and scope

#N Radiology reports at the study institution are free text in Chinese. Each preoperative index report was assigned a binary label (positive / negative for intestinal malrotation) by a rule-based, clause-level algorithm, and was separately coded for documented technical content. The two operations are independent: content coding never influenced the positive/negative label, and vice versa. Labels were subsequently adjudicated by a blinded paediatric surgeon (Section G); adjudicated labels superseded algorithmic labels in all analyses.

#H1 B. Unit of analysis and text segmentation

#N Each report was split into a findings section (检查所见 / 超声检查所见) and a conclusion section (检查结论 / 超声检查结论). The positive/negative label was determined from the conclusion section; the findings section was used only for content coding and for the targeted adjudication sample. Conclusions were segmented into clauses at the characters 。；;、and at line breaks. Each clause was evaluated independently, and the report label was the disjunction over clauses (any positive clause makes the report positive), subject to the negation and exclusion rules below.

#H1 C. Positive-evidence dictionary

#N A clause was a candidate positive if it matched any term below. Terms are given as they appear in the source text, with English glosses.

#N **Common to all modalities (diagnosis named):** 肠旋转不良 (intestinal malrotation); 中肠旋转不良 (midgut malrotation); 旋转不良 (malrotation); 肠扭转 (intestinal volvulus); 中肠扭转 (midgut volvulus); 肠系膜扭转 (mesenteric volvulus).

#N **Ultrasound-specific signs:** 漩涡征 / 旋涡征 / 涡流 (whirlpool sign); 螺旋 (spiral); 肠系膜上动脉与肠系膜上静脉换位 / 反位 / 倒置 / 关系异常 (inversion or abnormal relationship of the superior mesenteric artery and vein); 静脉位于动脉左侧 (vein to the left of the artery).

#N **UGI-series-specific signs:** 十二指肠空肠曲位置异常 / 位置偏低 / 位于中线 (abnormally positioned duodenojejunal junction); 弹簧征 (spring or corkscrew sign); 螺旋状 / 盘曲 (corkscrew or coiled course of proximal small bowel).

#N **CT-specific signs:** 漩涡征 / 旋涡样改变 (mesenteric whirl); 十二指肠位置异常 (abnormal duodenal position).

#N This dictionary is exactly the positivity definition given in the Methods. Jejunal position on the right and the course of the mesenteric vessels are audited as documented content (Section H) but are not positivity criteria, because the reporting radiologist may describe either without concluding that malrotation is present.

#H1 D. Certainty qualifiers

#N A candidate positive clause was retained as positive irrespective of certainty, and its certainty tier was recorded separately:

#N **Definite**: no qualifier (e.g. 中肠旋转不良。 "midgut malrotation.").
#N **Probable**: 多考虑, 首先考虑, 考虑, 倾向, 符合…表现 ("most likely", "first consideration", "consistent with").
#N **Possible**: 可疑, 可能, 不除外, 不排除, 待排, 待除外, 建议…除外/排除/进一步检查, 似, ？/? ("suspected", "cannot be excluded", "recommend further study to exclude", "?").

#N Certainty tiers are reported by modality in Table 2 of the main manuscript, and the principal analyses are repeated with possible-tier conclusions reclassified as negative.

#H1 E. Negation, scope and exclusion rules

#N **E1 Negation.** A candidate positive was cancelled when a negation cue governed the diagnostic term: 未见 / 未探及 / 未显示 / 未发现 (not seen), 无 / 无明显 (absent), 不考虑 (not considered), 正常 (normal), 阴性 (negative). A cue governs the term only when it stands in the twelve characters preceding it, so 未见明显梗阻征象。中肠旋转不良考虑。 remains positive, and so does 中肠旋转不良术后：未见明显梗阻征象, where the negation governs the obstruction rather than the rotation. 无 is not read as a cue inside 有无 ("whether or not"), which raises the question rather than answering it. 排除 and 除外 are not negation cues in this corpus: every occurrence with the diagnosis is a request to exclude it, which rule E2 treats as raising it.

#N **E2 Distinction between negation and hedged exclusion.** 建议进一步检查除外肠旋转不良 ("recommend further study to exclude malrotation") is not a negation: it raises the diagnosis. Such clauses were labelled positive at possible-tier certainty. This rule was applied consistently. It is the most consequential interpretive decision in the algorithm, and it is the reason for the sensitivity analysis in Table 2.

#N **E3 Organ exclusions.** 胃扭转 and 胃翻转 (gastric volvulus / organoaxial gastric rotation) are benign findings unrelated to midgut rotation and never make a report positive, even though they contain 扭转. Likewise excluded: 睾丸扭转, 卵巢扭转, 附件扭转, 精索扭转, 大网膜扭转, 阑尾扭转 (testicular, ovarian, adnexal, spermatic-cord, omental and appendiceal torsion). A report may still be positive on other grounds: 中肠旋转不良并十二指肠不全性梗阻考虑。胃翻转。 is positive on its first clause.

#N **E4 Non-index anatomy.** Clauses concerned with other organ systems in a combined report (e.g. cranial CT findings in a report covering head and abdomen) were ignored.

#H1 F. Priority order

#N Rules were applied in this order: (1) organ exclusions (E3); (2) positive-evidence dictionary (C); (3) hedged-exclusion recognition (E2); (4) negation (E1); (5) certainty tagging (D). E2 is read before E1 because a request to exclude the diagnosis raises it and must not be cancelled as a negation; a hedged cue is read in the twelve characters before the term or, up to the next punctuation, after it. Reports with no matching clause were labelled negative. Technically non-diagnostic studies were not coded separately as indeterminate and were labelled by their stated conclusion.

#H1 G. Validation and adjudication

#N A paediatric surgeon blinded to the operative findings adjudicated 32 reports in two independent samples.

#N **Sample 1 (validation).** A stratified random sample of 24 reports with positive and negative machine labels balanced across the three modalities. Agreement 22/24 (92%); Cohen kappa 0.83; per-modality agreement 88% (UGI), 88% (CT) and 100% (ultrasound). These are the only figures used to characterise algorithm performance.

#N **Sample 2 (targeted).** The 8 reports in which a malrotation sign appeared in the findings section while the machine label was negative. Five were confirmed as machine under-calls and corrected. Because this sample was selected on suspected discordance, it is **excluded** from the agreement statistics above; including it would bias them.

#N **Direction of error.** All 7 discordances across both samples were machine under-calls (a true positive labelled negative). No machine over-call was identified. Reported detection rates are therefore conservative.

#N **Typical failure modes observed:** (i) the diagnosis stated only in the findings section and not carried into the conclusion; (ii) a diagnostic sign described morphologically without the diagnosis being named, as in 中上腹异常光团回声，内呈强弱相间的漩涡状回声 ("abnormal mass-like echo in the upper abdomen with alternating whirled echogenicity"), which does not contain the words 旋转不良; (iii) the diagnosis embedded in a long multi-organ conclusion after several unrelated clauses.

#N **Limitation.** Validation rested on one adjudicator, so interobserver agreement between two independent adjudicators could not be estimated. The agreement figures describe algorithm-versus-adjudicator concordance only.

#H1 J. Reference implementation and its agreement with the final labels

#N The rules in Sections C–F are provided as a runnable Python script (`classifier.py`, deposited with this Online Resource) so that they can be inspected and re-applied. The script takes a report conclusion and a modality and returns a binary label and a certainty tier, implementing clause segmentation (B), the positive-evidence dictionary (C), certainty tiering (D), negation, hedged-exclusion and organ-exclusion handling (E), and the priority order (F).

#N Applied to all 740 preoperative index reports and compared with the final labels used in the analysis (the algorithmic labels after blinded surgeon adjudication), the reference implementation agreed on 726 of 740 (98.1%): 98.7% for the UGI series, 98.1% for CT and 96.6% for ultrasound. All fourteen disagreements were reference-implementation under-calls; there was no over-call.

#N The residual under-calls are dominated by the failure modes listed in Section G: the diagnosis stated in the findings section but not carried into the conclusion; a conclusion consisting only of a cross-reference to another report; and a diagnostic sign described morphologically without the diagnosis being named. These are the reports that adjudication corrected upward, so the direction of error is consistent with a rule set of this kind under-detecting rather than over-detecting, and the detection rates reported in the manuscript are conservative.

#N This exercise has two limitations. First, agreement is measured against labels that were themselves partly produced by rule-based classification, so it demonstrates that the published rules reproduce the analysis, not that either is correct against blinded image review. Second, the certainty tiers in Table 2 of the manuscript are computed over the adjudicated positive reports, whereas the reference implementation tiers its own positives; the two sets differ by the seventeen reports above, so tier counts differ by small numbers.

#H1 G2. Cohort retrieval strings

#N Children were retrieved from the institutional surgical records database by matching, case-insensitively, the operative diagnosis field (术中诊断) against `肠旋转不良` or the procedure-name field (手术名称) against `Ladd`. Applied to the 559 operative records of 499 children held for the study period, this returns 503 records in 465 children; every retrieved record was read before inclusion. The 34 children not returned had operative diagnoses unrelated to malrotation (appendicitis, hypertrophic pyloric stenosis, Hirschsprung disease, diaphragmatic and cardiac procedures among them).

#H1 H. Report-content audit patterns

#N Content coding was applied to the concatenated findings and conclusion text of each index unit. The index unit is the examination episode closest to operation: all reports of that modality issued on that calendar day are pooled, because the department routinely issues separate gastrointestinal and great-vessel reports for one ultrasound session. Patterns are given as regular expressions over the source text. Technique elements (duodenal segments, the mesenteric vessels, enteric fluid, dynamic and compression technique, colour Doppler, caecal position) are coded on mention, whether the finding was normal or abnormal, because an examination that states the vessel relationship is normal did assess the vessels. Findings and adequacy statements (the whirlpool sign, limiting bowel gas) are coded clause-by-clause with negation and co-occurrence handling, as noted in the table.

#TABH

#N Three properties of this audit qualify its interpretation. First, it records what was written, and is a lower bound on what was performed. The D3 pattern accepts the four terms used for the third portion in this corpus (水平部, 水平段, 横部, 第三段); the negative lookbehind excludes 主动脉弓横部, and the enteric-fluid pattern requires a statement that fluid was given, so observed luminal fluid without a stated route was not counted. Second, patterns were fixed only after enumerating every occurrence of the relevant vocabulary in the corpus and inspecting each match: a pattern for the abdominal aorta was discarded because two of its three matches were cardiac or renal-vein findings, the mesenteric-vessel pattern was extended to 肠系膜上动、静脉 and 肠系膜上动静脉 and excludes an isolated left-renal-vein measurement, and the duodenojejunal-junction pattern was extended to the 交界 wording used in this corpus. Third, the whirlpool text variable agrees with the separately adjudicated whirlpool variable in 118 of the 119 ultrasound examinations; the single disagreement is a child whose whirlpool was documented on an ultrasound performed on a different day from the index episode.

#H1 I. Distribution of labels by modality

#TABS1
