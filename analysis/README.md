# Re-analysis for the revised manuscript

All figures, tables and in-text numbers in
`诊断效能_英文稿_InsightsIntoImaging投稿版_v4.docx` and the three Online Resources
are produced by the scripts here
from the raw export `全部肠旋转不良数据.xlsx`, the operative cohort
`诊断效能_手术确诊队列_465例.xlsx` and the adjudicated per-patient matrix
`诊断效能_逐患者矩阵_当前版v3.xlsx` in the repository root.

## Requirements

    pip install pandas openpyxl statsmodels scipy matplotlib python-docx

## Reproduction

    python3 core.py        # not run directly; exec'd by the others
    python3 a55b.py        # the 55 children without an index test
    python3 clin.py        # Table 1: characteristics by imaging group
    python3 usaudit.py     # first-pass ultrasound content audit (superseded)
    python3 usaudit4.py    # Table 3: definitive ultrasound content audit
    python3 temporal2.py   # era models and the CT / UGI audits on pooled episodes
    python3 tables_final.py # Tables 2 and 4
    python3 or_sens.py     # Online Resource 2 sensitivity analyses (S8-S10)
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
    python3 figs.py figs2.py                    # writes Fig1-3 and FigS1 PNGs

`ALL_RESULTS.txt` is the concatenated console output of the analysis scripts.

## Building the documents

    cd manuscript_source_iii
    python3 build_iii.py    # manuscript from p1-3.md + tables*.json + figures
    python3 build_or.py     # the three Online Resources
    python3 build_docs.py   # cover letter, submission sheet, Chinese notes
    python3 wc.py           # main-text word count against the 3,000-word limit

`manuscript_source/` holds the earlier Pediatric Radiology revision sources;
`or1.md` there is still the source of Online Resource 1.

## The index unit, and the report-content audit patterns

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

The rebuilt dataset reproduces exactly: 465 children, 352 male, 301 UGI / 320 CT /
119 ultrasound index tests, 59 with all three, 410 imaged, 740 index examinations,
detection 237 / 171 / 65, unadjusted GEE odds ratios 0.31 (0.22-0.44) and
0.33 (0.21-0.50), Cochran's Q p=0.001 and the three exact McNemar p values.

It differs in the cohort descriptors that depend on age, because each operative
record is now linked to the admission containing that operation (verified for all
465). See section 4 of `修改说明_中文.docx`.

## Analyses added after statistical review

`addstats.py` produces Online Resource 2 Tables S11-S13:

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
agrees to six decimal places (OR 17.56), but the Wald interval (0.77-401) and the
profile interval (2.00-2310, penalised LR p=0.006) disagree on whether unity is
excluded. The profile interval is the correct one and is what the supplement
reports. R's `logistf` itself could not be installed here because CRAN is blocked
by the environment's network policy.

`volsign2.py` replaces the volvulus-specific-sign table. The earlier version used
one pooled sign pattern across all three modalities with no negation handling and
reported 59/113 for ultrasound, which contradicted the 58/113 in the manuscript;
the harmonised rule is modality-specific and negation-aware.
