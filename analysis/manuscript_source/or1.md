#T Online Resource 1. Text-classification algorithm and report-content audit

#N Supplement to: "Routine ultrasound reports for intestinal malrotation rarely document duodenal landmarks: a report-level audit of 740 preoperative examinations in 465 surgically confirmed children"

#N ⟦AUTHORS: sections A–F below express the classification rules as applied in this study. Please verify each entry against the production script before submission and add any term used by your department that is not listed.⟧

#H1 A. Purpose and scope

#N Radiology reports at the study institution are free text in Chinese. Each preoperative index report was assigned a binary label (positive / negative for intestinal malrotation) by a rule-based, clause-level algorithm, and was separately coded for documented technical content. The two operations are independent: content coding never influenced the positive/negative label, and vice versa. Labels were subsequently adjudicated by a blinded paediatric surgeon (Section G); adjudicated labels superseded algorithmic labels in all analyses.

#H1 B. Unit of analysis and text segmentation

#N Each report was split into a findings section (检查所见 / 超声检查所见) and a conclusion section (检查结论 / 超声检查结论). The positive/negative label was determined from the conclusion section; the findings section was used only for content coding and for the targeted adjudication sample. Conclusions were segmented into clauses at the characters 。；;、and at line breaks. Each clause was evaluated independently, and the report label was the disjunction over clauses (any positive clause makes the report positive), subject to the negation and exclusion rules below.

#H1 C. Positive-evidence dictionary

#N A clause was a candidate positive if it matched any term below. Terms are given as they appear in the source text, with English glosses.

#N **Common to all modalities (diagnosis named):** 肠旋转不良 (intestinal malrotation); 中肠旋转不良 (midgut malrotation); 旋转不良 (malrotation); 肠扭转 (intestinal volvulus); 中肠扭转 (midgut volvulus); 肠系膜扭转 (mesenteric volvulus).

#N **Ultrasound-specific signs:** 漩涡征 / 旋涡征 / 涡流 (whirlpool sign); 螺旋 (spiral); 肠系膜上动脉与肠系膜上静脉换位 / 反位 / 倒置 / 关系异常 (inversion or abnormal relationship of the superior mesenteric artery and vein); 静脉位于动脉左侧 (vein to the left of the artery).

#N **UGI-series-specific signs:** 十二指肠空肠曲位置异常 / 位置偏低 / 位于中线 (abnormally positioned duodenojejunal junction); 弹簧征 (spring or corkscrew sign); 螺旋状 / 盘曲 (corkscrew or coiled course of proximal small bowel); 空肠位于右腹 / 右中腹 (jejunum lying on the right).

#N **CT-specific signs:** 漩涡征 / 旋涡样改变 (mesenteric whirl); 十二指肠位置异常 (abnormal duodenal position); 肠系膜血管走行异常 (abnormal mesenteric-vessel course).

#H1 D. Certainty qualifiers

#N A candidate positive clause was retained as positive irrespective of certainty, and its certainty tier was recorded separately:

#N **Definite** — no qualifier (e.g. 中肠旋转不良。 "midgut malrotation.").
#N **Probable** — 多考虑, 首先考虑, 考虑, 倾向, 符合…表现 ("most likely", "first consideration", "consistent with").
#N **Possible** — 可疑, 可能, 不除外, 不排除, 待排, 待除外, 建议…除外/排除/进一步检查, 似, ？/? ("suspected", "cannot be excluded", "recommend further study to exclude", "?").

#N Certainty tiers are reported by modality in Table 2 of the main manuscript, and the principal analyses are repeated with possible-tier conclusions reclassified as negative.

#H1 E. Negation, scope and exclusion rules

#N **E1 Negation.** A candidate positive was cancelled if a negation cue appeared in the same clause and governed the diagnostic term: 未见 (not seen), 无 (absent), 未 (not), 排除 (excluded), 正常 (normal), 阴性 (negative), 未见明显异常 (no significant abnormality). Negation scope was the clause, not the sentence or report, so 未见明显梗阻征象。中肠旋转不良考虑。 ("no obstruction seen. Midgut malrotation considered.") remains positive.

#N **E2 Distinction between negation and hedged exclusion.** 建议进一步检查除外肠旋转不良 ("recommend further study to exclude malrotation") is not a negation: it raises the diagnosis. Such clauses were labelled positive at possible-tier certainty. This rule was applied consistently and is the single most consequential interpretive decision in the algorithm; the sensitivity analysis in Table 2 exists because of it.

#N **E3 Organ exclusions.** 胃扭转 and 胃翻转 (gastric volvulus / organoaxial gastric rotation) are benign findings unrelated to midgut rotation and never make a report positive, even though they contain 扭转. Likewise excluded: 睾丸扭转, 卵巢扭转, 附件扭转, 精索扭转, 大网膜扭转, 阑尾扭转 (testicular, ovarian, adnexal, spermatic-cord, omental and appendiceal torsion). A report may still be positive on other grounds — for example 中肠旋转不良并十二指肠不全性梗阻考虑。胃翻转。 is positive on its first clause.

#N **E4 Non-index anatomy.** Clauses concerned with other organ systems in a combined report (e.g. cranial CT findings in a report covering head and abdomen) were ignored.

#H1 F. Priority order

#N Rules were applied in this order, first match winning: (1) organ exclusions (E3); (2) clause-level negation (E1); (3) hedged-exclusion recognition (E2); (4) positive-evidence dictionary (C); (5) certainty tagging (D). Reports with no matching clause were labelled negative. Technically non-diagnostic studies were not coded separately as indeterminate and were labelled by their stated conclusion.

#H1 G. Validation, and the errors we found

#N A paediatric surgeon blinded to the operative findings adjudicated 32 reports in two independent samples.

#N **Sample 1 (validation).** A stratified random sample of 24 reports with positive and negative machine labels balanced across the three modalities. Agreement 22/24 (92%); Cohen kappa 0.83; per-modality agreement 88% (UGI), 88% (CT) and 100% (ultrasound). These are the only figures used to characterise algorithm performance.

#N **Sample 2 (targeted).** The 8 reports in which a malrotation sign appeared in the findings section while the machine label was negative. Five were confirmed as machine under-calls and corrected. Because this sample was selected on suspected discordance, it is **excluded** from the agreement statistics above; including it would bias them.

#N **Direction of error.** All 7 discordances across both samples were machine under-calls (a true positive labelled negative). No machine over-call was identified. Reported detection rates are therefore conservative.

#N **Typical failure modes observed:** (i) the diagnosis stated only in the findings section and not carried into the conclusion; (ii) a diagnostic sign described morphologically without the diagnosis being named (e.g. 中上腹异常光团回声，内呈强弱相间的漩涡状回声 — "abnormal mass-like echo in the upper abdomen with alternating whirled echogenicity" — without the words 旋转不良); (iii) the diagnosis embedded in a long multi-organ conclusion after several unrelated clauses.

#N **Limitation.** Validation rested on one adjudicator, so interobserver agreement between two independent adjudicators could not be estimated. The agreement figures describe algorithm-versus-adjudicator concordance only.

#H1 H. Report-content audit patterns

#N Content coding was applied to the concatenated findings and conclusion text of each index report. Patterns are given as regular expressions over the source text; a report was coded positive for an element if the pattern matched anywhere in that text.

#TABH

#N Two properties of this audit should be kept in mind. First, it records what was written, and is a lower bound on what was performed. Second, the whirlpool sign appears in the main manuscript both as an adjudicated study variable (59 of 119 reports) and as a text-pattern variable (57 of 119); the small difference reflects two reports in which the adjudicator recognised a whirlpool described in words the pattern did not capture, and both figures are reported for transparency.

#H1 I. Distribution of labels by modality

#TABS1
