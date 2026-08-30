# Re-analysis for the revised manuscript

All figures, tables and in-text numbers in `诊断效能_英文稿_修回版_v3.docx`,
`Online_Resource_1_NLP_and_report_audit.docx` and
`Online_Resource_2_and_3_supplementary_tables.docx` are produced by the scripts here
from the raw export `全部肠旋转不良数据.xlsx`, the operative cohort
`诊断效能_手术确诊队列_465例.xlsx` and the adjudicated per-patient matrix
`诊断效能_逐患者矩阵_当前版v3.xlsx` in the repository root.

## Requirements

    pip install pandas openpyxl statsmodels scipy matplotlib python-docx

## Reproduction

    python3 core.py        # not run directly; exec'd by the others
    python3 a55b.py        # the 55 children without an index test
    python3 clin.py        # Table 1: characteristics by imaging group
    python3 usaudit.py     # Table 3: ultrasound report-content audit
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
    python3 figs.py figs2.py                    # writes Figure1-4 PNGs

`ALL_RESULTS.txt` is the concatenated console output of the analysis scripts.

## Building the documents

    cd manuscript_source
    python3 build.py    # manuscript from part1-4.md + tables*.json + figures
    python3 build2.py   # Online Resources from or1.md / or23.md

## Validation against the previously submitted version

The rebuilt dataset reproduces exactly: 465 children, 352 male, 301 UGI / 320 CT /
119 ultrasound index tests, 59 with all three, 410 imaged, 740 index examinations,
detection 237 / 171 / 65, unadjusted GEE odds ratios 0.31 (0.22-0.44) and
0.33 (0.21-0.50), Cochran's Q p=0.001 and the three exact McNemar p values.

It differs in the cohort descriptors that depend on age, because each operative
record is now linked to the admission containing that operation (verified for all
465). See section 4 of `修改说明_中文.docx`.
