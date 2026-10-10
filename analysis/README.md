# Re-analysis for the revised manuscript

All figures, tables and in-text numbers in
`JACR_3_Manuscript_masked.docx` and the three Supplements (Supplement 1-3)
are produced by the scripts here
from the raw export `全部肠旋转不良数据.xlsx`, the operative cohort
`诊断效能_手术确诊队列_465例.xlsx` and the adjudicated per-patient matrix
`诊断效能_逐患者矩阵_当前版v3.xlsx` in the repository root.

## Requirements

    pip install pandas openpyxl statsmodels scipy matplotlib python-docx

## Reproduction

    python3 review_merge.py # S1-S3 review decisions -> review_exclusions.csv, us_manual_coding.csv
    python3 core.py        # not run directly; exec'd by the others
    python3 a55b.py        # the 52 children without an index test (a55b.json feeds Figure 1)
    python3 clin.py        # Table 1: characteristics by imaging group
    python3 usaudit.py     # first-pass ultrasound content audit (superseded)
    python3 usaudit4.py    # Table 3: definitive ultrasound content audit
    python3 temporal2.py   # era models and the CT / UGI audits on pooled episodes
    python3 or_sens.py     # Supplement 2 sensitivity analyses (S8-S10)
    python3 revcheck.py    # report-flow, index-unit and volvulus-definition checks
    python3 volsign2.py    # volvulus-specific sign, harmonised with the main audit rules
    python3 firth.py       # Firth penalised logistic, with a validation check vs the MLE
    python3 addstats.py    # bootstrap AME CIs, paired differences, Firth, interaction terms
    python3 audit2.py      # CT / UGI content audit, hedged phrasing
    python3 cert.py        # certainty tiers of positive conclusions
    python3 paired.py      # paired subgroup, timing, McNemar / Cochran Q
    python3 volsign.py     # volvulus-specific sign
    python3 temporal.py    # era trends
    python3 mediate.py     # era vs examination-content mediation models
    python3 order.py       # test sequence / pathway position
    python3 final.py       # subgroup detection, sensitivity analyses
    python3 gee.py gee2.py # GEE models and the interaction/separation issue
    python3 tables.py tables2.py or_tables.py   # writes tables*.json
    python3 tables_final.py # Tables 2 and 4; reads tables123.json, so run it AFTER tables.py
    python3 classifier_agreement.py  # agreement of the published script with the final labels
    python3 or_add.py      # assembles or_add.json; run after addstats.py and volsign2.py
    python3 figs.py figs2.py                    # writes Fig1-3 and FigS1 PNGs
    python3 graphabs.py    # graphical abstract for Insights into Imaging (not used by JACR)

`ALL_RESULTS.txt` is the concatenated console output of the analysis scripts.

## Building the documents

    cd manuscript_source_jacr
    python3 build_manuscript.py  # masked manuscript (double-spaced, line-numbered; legends, tables and figures after the references) and JACR_Figure1-3.tif
    python3 build_supplements.py # Supplements 1-3 from supp1-3.md, and Supplement_1_classifier.py
    python3 build_strobe.py      # JACR_STROBE_checklist.docx from strobe.json
    python3 build_docs.py        # cover letter, title page, Chinese submission sheet
    python3 wc.py                # main-text word count against the 3,000-word limit
    python3 jacr_check.py        # every JACR limit, masking, spelling and stale-term check

The manuscript is formatted for the *Journal of the American College of
Radiology*: AMA references, American spelling, an Objective / Methods /
Results / Conclusion abstract of at most 250 words, Take-Home Points in place
of a Conclusion section, at most 7 tables and figures and at most 7 authors.
`docstyle.py` gives every document black Times New Roman headings in place of
python-docx's blue defaults, and the manuscript its page and line numbers.
`usspell.py` holds the spelling map: the Markdown sources were converted with
it once, and the builders apply it to table text read from the analysis JSON,
which the analysis scripts still write in British spelling. Reference titles
are quoted as published and are never converted.

The Insights into Imaging submission (desk-rejected on scope, 30 September
2026) is kept as built in `archive/InsightsIntoImaging_desk-rejected_2026-09-30/`;
its sources are this folder's history before the JACR conversion.
`manuscript_source/` holds the earlier Pediatric Radiology revision sources.

All tables in the manuscript, the three Supplements and the STROBE
checklist are built by `threeline.py` as open (three-line) tables — a rule
above the header, a rule under the header, a rule at the foot, no vertical
rules and no rules between data rows, which is the convention scientific
journals expect (equivalent to the Chinese academic 三线表) and is not what
Word's built-in "Light Grid Accent 1" style draws. Every table calls
`make_three_line_table()`; do not add a table via `doc.add_table()` with a
named style instead.

## The index unit, and the report-content audit patterns

(The counts in this and the next three sections predate the S1-S3 review; the
current numbers are in the last section.)

`usaudit4.py` is the definitive audit and supersedes `usaudit.py` and `usaudit2.py`.
Two things changed and both matter.

**The index unit is an examination episode, not a report.** The department
routinely issues two reports for one ultrasound session (胃肠道彩超 and
腹部大血管彩超, minutes apart). Taking "the single report closest to operation"
picked the negative companion report in three patients, one of which concluded
腹膜后未见明显异常 while the patient carried a positive, whirlpool-positive label
from the same session. All reports of a modality issued on the index day are now
pooled: 812 eligible preoperative reports -> 778 pooled into 740 episodes, with
the per-modality denominators (301 / 320 / 119) unchanged.

**The patterns were fixed against the corpus vocabulary, not from memory.**
Corrections made after enumerating every occurrence and inspecting each match:
D3 needed 水平部 and 横部 (the commonest local terms, missed by the first pass);
the mesenteric-vessel pattern needed 肠系膜上动、静脉 and 肠系膜上动静脉 and must
exclude an isolated left-renal-vein measurement; the duodenojejunal junction
needed the 交界 wording; the UGI pattern 十二指肠.{0,6}空肠 was too loose and is
now 空肠曲; the whirlpool must not count negated mentions (未见明显旋涡状回声);
bowel-gas limitation must require a gas term and a limitation term in the same
clause, or a cardiac report's 肺气严重…显示不清 is counted.

Resulting headline rates: D3 or duodenojejunal junction 3/119 (2.5%), mesenteric
vessels 12/119 (10.1%), enteric fluid 2/119, whirlpool reported 58/119 (48.7%).
`or_h.json` holds the published pattern table and must stay in step with
`usaudit4.py`.

## Validation against the previously submitted version

The rebuilt dataset reproduced the previously submitted version exactly: 465
children, 352 male, 301 UGI / 320 CT / 119 ultrasound index tests, 59 with all
three, 410 imaged, 740 index examinations, detection 237 / 171 / 65, unadjusted
GEE odds ratios 0.31 (0.22-0.44) and 0.33 (0.21-0.50), Cochran's Q p=0.001 and
the three exact McNemar p values.

Three of those labels were subsequently corrected (see **Label corrections**
below), so the current pipeline produces detection 237 / 169 / 64, unadjusted GEE
odds ratios 0.30 (0.22-0.42) and 0.32 (0.21-0.48), and Cochran's Q p=0.0007. The
denominators, the cohort counts and the report flow are unchanged.

It differs in the cohort descriptors that depend on age, because each operative
record is now linked to the admission containing that operation (verified for all
465). See section 4 of `修改说明_中文.docx`.

## Analyses added after statistical review

`addstats.py` produces Supplement 2 Tables S11-S13:

* percentile bootstrap CIs for the average marginal effect of era (2,000 resamples
  of children, seed 20260903), because the manuscript reports the era effect on the
  risk-difference scale;
* paired differences in detection with bootstrap CIs for the three-modality
  subgroup, replacing a p-value-only presentation;
* a Firth penalised estimate of the separated ultrasound-by-volvulus contrast, plus
  the same interaction restricted to UGI and CT where it is estimable;
* era-by-content interaction terms.

`firth.py` is a self-contained Jeffreys-penalised logistic fit reporting profile
penalised-likelihood intervals and penalised likelihood-ratio p-values, as R's
`logistf` does. Running it as a script checks it against `statsmodels` on
non-separated data and prints the separated example.

Do not use its Wald interval for the separated contrast. `firth_check.py` compares
the fit against `firthlogist`, an independent implementation: the coefficient
agrees to six decimal places (OR 16.94), but the Wald interval (0.74-387) and the
profile interval (1.93-2229, penalised LR p=0.006) disagree on whether unity is
excluded. The profile interval is the correct one and is what the supplement
reports. R's `logistf` itself could not be installed here because CRAN is blocked
by the environment's network policy.

`volsign2.py` replaces the volvulus-specific-sign table. The earlier version used
one pooled sign pattern across all three modalities with no negation handling and
reported 59/113 for ultrasound, which contradicted the 58/113 in the manuscript;
the harmonised rule is modality-specific and negation-aware.

## Label corrections

`labelaudit.py` screens every index unit in both directions: positive labels whose
pooled report text matches no diagnostic term and no modality-specific sign, and
negative labels whose text names the diagnosis. It found nine of the first kind and
none of the second. All nine were read against the source reports; three were
over-calls.

`label_corrections.csv` lists those three with their reasons, and `core.py` applies
it to the matrix immediately after reading it, asserting that each row still matches
the value it claims to replace. The raw export `诊断效能_逐患者矩阵_当前版v3.xlsx`
is never modified, so the correction is visible and reversible.

    4331826   CT_detected  1 -> 0
    35807877  CT_detected  1 -> 0
    10140565  US_detected  1 -> 0

Consequences: CT detection 171/320 -> 169/320, ultrasound 64/119; the upper
gastrointestinal series is unaffected. The crude era effect for ultrasound falls
just below conventional significance (odds ratio 2.16, 0.99-4.70, p=0.053) while
its bootstrap marginal effect still excludes zero at +19.0 pp (+0.6 to +37.6);
both are reported as borderline. `待核标签清单_9例_已裁定.xlsx` is the worksheet the
adjudication was recorded on.

## Review of the anchor operations, timing and ultrasound content (S1-S3)

Three steps were checked by hand on worksheets written by
`build_review_checklists.py`; the filled-in copies are in `review_returns/`.
`review_merge.py` transcribes them, asserting the expected decision counts, and
writes `review_exclusions.csv`, `us_manual_coding.csv` and
`review_agreement.json` (all tracked, so the decisions are visible).

* **S1 reference standard.** 34 anchor operations were read against all of the
  child's operative records. 6 did not confirm malrotation and 9 were
  reoperations after earlier malrotation surgery; `core.py` drops these 15
  children (11 of them had an index test). Cohort 465 -> 450.
* **S2 timing.** Operative times are dates only. Of the same-day and >7-day
  index reports, three were postoperative and one belonged to an unrelated
  earlier illness. `core.py` drops them before choosing the index unit and
  asserts the consequences: 1426267 gets an earlier, negative UGI as its index
  (label 0, unchanged), 3826010 loses its only ultrasound and moves to the
  no-index group, and 8696516 keeps CT only. The fourth report belongs to an
  excluded child.
* **S3 ultrasound content.** Two readers coded the twelve content items of all
  119 ultrasound episodes independently; 5 of 1,428 cells differed and were
  adjudicated (the `ADJ` dictionary in `review_merge.py`). `usaudit4.py` now takes
  the twelve items from `us_manual_coding.csv` and keeps the regex columns as
  `*_rx` for comparison; `core.py` replaces `US_whirlpool` with the consensus
  whirlpool. The vessel pattern had counted any mention of the mesenteric
  vessels (12 vs 3 by manual reading).

Headline numbers after the review: 450 children, 398 imaged, 723 index
examinations from 793 eligible reports (761 in index episodes, 32 earlier),
52 without an index test; detection UGI 230/293, CT 165/313, ultrasound 64/117.
Ultrasound content: D3 or DJJ 3/117, artery-vein relationship 3/117, enteric
fluid 2/117, whirlpool 59/117, limiting gas 36/117; whirlpool among the 112
children with volvulus 59. The crude ultrasound era effect is now OR 2.13
(0.97-4.67) with bootstrap marginal effect +18.7 pp (-0.2 to +37.7), so neither
excludes zero. Firth OR 14.6 (profile 1.60-1938, p=0.013); with one binary
covariate this equals the odds ratio after adding 0.5 to each cell,
(64.5 x 5.5)/(48.5 x 0.5). `firth_check.py` could not be re-run because
`firthlogist` is not installable in this environment.

Scripts that hard-coded the old denominators (cert, final, or_sens, or_tables,
tables, tables2, or_add, figs, figs2) now compute them, and Figure 1 is drawn
from the data. `or_sens.py` codes the earliest-episode sensitivity analysis from
the manual reading where the earliest episode is the index session (106
children) and checks the other 11 by pattern: none mentions D3, the DJJ, the
vessels or fluid, and the two whirlpool matches describe vessels encircling a
mass. `gee.py` no longer crashes on the separated interaction model, and
`classifier_agreement.py` reads `Supplement_1_classifier.py`.


## Presentation changes after the self-review (general and language items)

* Modality labels in every table and figure are "UGI series", "Abdominal CT"
  and "Ultrasound" (the ultrasound sessions include great-vessel and pyloric
  bookings, so "gastrointestinal ultrasound" was inaccurate).
* P values follow AMA style: `usspell.ama_p()` rewrites `p=0.060` as `*P* = .060`
  in every table cell and paragraph, and `threeline.py` and the paragraph
  writers render `*...*` as italic. P columns carry no leading zero.
* Table 4 shows the bootstrap intervals of the marginal effects from
  `addstats.json`. The UGI interval uses its own random stream (seed 20261009),
  so every interval already reported is unchanged.
* Figure 1 starts from the 711 children in the database export and shows the 34
  children whose operations did not meet the criterion. The explanatory text
  that used to sit inside Figures 1, 2 and S1 has moved to the legends.
* `export_refs.py` writes `参考文献_{N}条*` for however many references there are
  (now 25, with El-Ali et al., Pediatr Radiol 2025).

## Number-by-number check (数字核对表.xlsx)

`verify_facts.py` recomputes every reported number from the analysis dataset with
separately written code (Wilson intervals, logistic regression by IRLS, Cochran Q,
exact McNemar, Cohen kappa); GEE, bootstrap and Firth profile results are refitted
with the original software and seed. `verify_numbers.py` compares every number in
the abstract, text, tables, figures, legends, Supplements 1-3, cover letter and
title page against it, checks that every numeric token in the text has a check
row, and writes `../数字核对表.xlsx` (sheets 说明, 核对表, 问题汇总, 专项检查).
Run it after any rebuild: `python3 verify_numbers.py`.

The first run of the check found that `cert.py` read the certainty tier from the
single closest report rather than the pooled episode, which mis-tiered four
positive episodes; `cert.py` now tiers the pooled conclusion. After that and the
text corrections listed on the workbook's 更正记录 sheet, every row is consistent
except one statement that only the department can confirm.
