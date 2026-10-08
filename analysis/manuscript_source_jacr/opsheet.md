#T JACR 投稿操作单

#N 稿件：Routine Ultrasound Reports for Pediatric Intestinal Malrotation Rarely Document Duodenal Landmarks: A Single-Center Audit

#N 目标期刊：*Journal of the American College of Radiology*（JACR，Elsevier 出版），文章类型 Original Article。以下字段内容可直接复制粘贴。

#H1 一、相对 Insights into Imaging 版改了什么

#N **科学内容一个数字都没改。** IiI 是因"不在期刊关注范围"直接退稿，没有任何针对方法或数据的意见。四张表逐格比对过，除拼写外完全一致；FigS1 重新生成后与原图逐像素相同。

#N **按 JACR 要求改的格式：**
#N 1. **标题**改为 Title Case，并压到 121 个字符（JACR 上限 129，且不得用问句）。
#N 2. **摘要**段名改为 Objective / Methods / Results / Conclusion，共 245 词（上限 250），摘要内无引文。
#N 3. **删去 IiI 专属内容**：Key Points、Critical relevance statement、图文摘要（Graphical Abstract）和缩略语表。
#N 4. **结论段换成 Take-Home Points**：JACR 原创论文用 3–6 条要点代替讨论末尾的结论段，现为 4 条。
#N 5. **Limitations** 保留为讨论下的独立小节（JACR 要求原创研究必须有）。
#N 6. **全文改为美式拼写**：paediatric→pediatric、centre→center、randomised→randomized 等。图 3 里的 "Caecal" 也改成 "Cecal"，并已重新出图；面板字母改为大写 A/B。
#N 7. **参考文献改为 AMA 格式**（JACR 遵循 AMA Manual of Style）：作者. 题目. *期刊*. 年;卷:页码. doi:。正文图号写作 "Figure 1"。
#N 8. **"Online Resource" 统一改名为 "Supplement 1–3"**，脚本改名为 `Supplement_1_classifier.py`。
#N 9. **作者减到 7 位**：Guanghua Zhang、Hongxi Guo、Haibin Wang 移到致谢（Acknowledgments），贡献声明同步改为 "JS, FP, KZ and HL acquired the clinical and operative data"。
#N 10. **新增生成式 AI 使用声明**：Elsevier 要求在正文参考文献前单独声明，正文与 Title Page 都已写入（见第五节）。
#N 11. **正文字数 2,990**（Introduction 至 Take-Home Points，上限 3,000）。表 4 张 + 图 3 张 = 7，正好达到 JACR "图表合计不超过 7" 的上限，不能再加图表。
#N 12. **讨论第 2 段对文献 [13] 的表述更精确**：原写 "93–97%"，现写明 93% 来自原始临床报告、97% 来自盲法复读，且该研究排除了无法诊断和结果不确定的检查。这三点都已与该文摘要核对，也更有力地支撑本文的论点：差距在于检查内容，而不是"研究阅片"和"日常报告"之别。

#H1 二、上传文件清单（按此顺序）

#N **1. Cover Letter** —— `JACR_1_CoverLetter.docx`
#N 日期填的是 2026 年 10 月 8 日；若实际投稿日不同，改成投稿当天。

#N **2. Title Page** —— `JACR_2_TitlePage.docx`
#N 含 7 位作者、单位、ORCID、通讯作者邮寄地址、伦理批件号、致谢和全部声明。**这是唯一含作者身份信息的文件**，与正文分开上传。

#N **3. Manuscript（masked，隐去作者信息的正文）** —— `JACR_3_Manuscript_masked.docx`
#N 含 4 表 3 图（图内嵌，方便审稿人阅读）。文中无医院名、作者名或伦理批件号。

#N **4. Figures（单独上传，300 dpi TIFF）**
#N • `JACR_Figure1.tif` → Figure 1（研究流程图）
#N • `JACR_Figure2.tif` → Figure 2（各模态检出率，分母醒目）
#N • `JACR_Figure3.tif` → Figure 3（超声报告内容审计，核心图）
#N 同名 PNG（`Fig1_study_flow.png` 等）是备份；系统若不收 TIFF 就传 PNG。

#N **5. Supplementary material**
#N • `JACR_Supplement_1_NLP_and_report_audit.docx` —— 算法规则、验证、内容审计正则表
#N • `Supplement_1_classifier.py` —— 规则集的可运行实现，正文按这个文件名引用，**不要改名**；若系统不收 .py，压成 zip 上传
#N • `JACR_Supplement_2_models_and_subgroups.docx` —— GEE 模型、配对亚组、分层与敏感性分析（内含 Figure S1）
#N • `JACR_Supplement_3_CT_and_UGI_content_audit.docx` —— CT 与造影报告内容审计

#N **6. Reporting checklist** —— `JACR_STROBE_checklist.docx`

#N **7. Declaration of Interest statement** —— 需要通讯作者用 Elsevier Declarations tool 在线生成后上传（第四节）。

#H1 三、表单字段（可直接复制）

#N **Article type**：Original Article

#N **Title**：Routine Ultrasound Reports for Pediatric Intestinal Malrotation Rarely Document Duodenal Landmarks: A Single-Center Audit

#N **Short / running title**（若问）：Duodenal Landmarks in Routine Malrotation Ultrasound Reports

#N **Abstract**：从正文复制 Objective / Methods / Results / Conclusion 四段（含段名），共 245 词。**Keywords 不要粘进摘要框。**

#N **Keywords**（JACR 要求 3–5 个）：Intestinal malrotation; Intestinal volvulus; Infant, Newborn; Ultrasonography; Radiology report
#N 注意 "Infant, Newborn" 中间是逗号，算一个词。

#N **Summary sentence**（若系统要求；JACR 要求不超过 35 词，且必须逐字取自正文。这里用的是第 1 条 Take-Home Point，32 词、241 字符）：
#N Routine ultrasound reports for children with surgically confirmed malrotation documented the duodenal landmarks underpinning published accuracy in 2.5% of examinations and reported the diagnosis almost only when a whirlpool sign was present.

#N **Take-Home Points**（若系统要求单独填；JACR 写明初投不强制、修回时必交。已写入正文，逐字复制即可）：
#N • Routine ultrasound reports for children with surgically confirmed malrotation documented the duodenal landmarks underpinning published accuracy in 2.5% of examinations and reported the diagnosis almost only when a whirlpool sign was present.
#N • In practice, routine ultrasound served as a test for volvulus rather than for malrotation: a whirlpool sign was recorded in only 58 of 113 children in whom operation confirmed volvulus.
#N • These are report-level detection rates among surgically confirmed children, not sensitivities; they establish no specificity, predictive value or ranking of modalities, and are no argument against ultrasound-first pathways.
#N • Before assuming that published ultrasound performance applies locally, departments should audit whether their own reports document the duodenal landmarks; a structured report would make the gap auditable.

#N **Authors**（按此顺序录入，共 7 位；第一作者 Jun Shu，通讯作者 Jun Yang）：
#N 1. Jun Shu —— 单位 ①（第一作者）
#N 2. Fei Peng —— 单位 ①
#N 3. Kai Zheng —— 单位 ①
#N 4. Haiyan Lei —— 单位 ①
#N 5. Zhengliang Meng —— 单位 ②
#N 6. Hongqiang Bian —— 单位 ①
#N 7. Jun Yang —— 单位 ①（通讯作者）

#N **单位 ①**：Department of General Surgery, Wuhan Children's Hospital (Wuhan Maternal and Child Healthcare Hospital), Tongji Medical College, Huazhong University of Science & Technology, Wuhan 430016, Hubei Province, China

#N **单位 ②**：Department of Ultrasound Imaging, Wuhan Children's Hospital (Wuhan Maternal and Child Healthcare Hospital), Tongji Medical College, Huazhong University of Science & Technology, Wuhan 430016, Hubei Province, China

#N **Corresponding author**：Jun Yang，yjun201602@163.com，+86 186 2713 9911，ORCID 0009-0006-0669-4340

#N **Funding / Ethics / Data availability / Acknowledgments**：与 Title Page 逐条一致，直接照抄，不要另写一版。

#N **是否曾投过其他期刊**：若系统问到，据实回答。投稿信里不主动提。

#N **开放获取（Open Access）**：JACR 是混合模式期刊。选订阅模式（subscription）发表一般不收版面费，选 OA 才收费；金额以系统显示为准。

#N **推荐审稿人 / 回避审稿人**：非必填，建议跳过。

#H1 四、Elsevier Declarations tool（利益冲突声明）

#N JACR 从 2023 年 6 月起改用 Elsevier Declarations tool 收集利益冲突声明：由通讯作者在线填写，代表全体作者声明，生成文件后作为 "Declaration of Interest Statement" 上传。

#N 本文选 "The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."（与 Title Page 一致）。

#N 工具入口一般在投稿流程中有链接；找不到就搜索 "Elsevier Declarations tool"。

#H1 五、需要你决定或确认的事项

#N **1. 三位移出作者的知情同意（必须做）。** Guanghua Zhang、Hongxi Guo、Haibin Wang 现在在致谢里。按 ICMJE 规定，被致谢的人需本人同意被列名；同时应当面告知他们不再是作者。投稿后再改作者名单很麻烦，期刊会要求全体作者签字。

#N **2. 生成式 AI 使用声明（不要删）。** Elsevier 规定写作中使用了生成式 AI 必须声明，未声明属于违规，被发现可导致撤稿。本文的撰写、润色和分析代码都使用了 Claude，所以已按 Elsevier 的标准句式写入。措辞可以按你们的实际使用情况调整，但不要删掉。

#N **3. 通讯作者邮寄地址（已确认）。** JACR 要求 Title Page 写通讯作者的完整邮寄地址，已填 "100 Hong Kong Road, Jiang'an District, Wuhan 430016"（香港路 100 号），经你核对无误。

#N **4. 参考文献作者全名（已补全）。** AMA 格式要求：作者 6 位及以下全部列出，超过 6 位列前 3 位加 et al.。我逐条检索了 PubMed 和出版社记录：[4]、[15]、[16] 各 5 位作者，[10]、[19] 各 6 位，已补全；其余标 et al. 的条目都超过 6 位作者，写法正确。本次检索核对的 12 条（[2]–[5]、[10]–[16]、[20]）题目、期刊、年份、卷和页码均与记录一致；[19] 是 STROBE 声明，按其公开的 6 位作者名单补全；其余条目在此前的外部核对中已确认。

#N **5. 医院审查材料。** 答辩 PPT 和原始数据分析记录里如果写了 "拟投期刊：Insights into Imaging"，需要改成 JACR，作者名单也要改成 7 位。请把你手上已填好的 PPT 发回来，我只改期刊和作者相关内容。

#H1 六、以下 JACR 要求在这里无法打开官网核实，系统里以实际显示为准

#N 下面这些要求是检索 JACR 作者须知得到的，期刊官网在这里打不开：
#N • 原创论文正文少于 3,000 词（不含参考文献）
#N • 图表合计不超过 7 个
#N • 摘要不超过 250 词，按 objective / methods / results 等结构
#N • 关键词 3–5 个
#N • 标题不超过 129 字符，不得用问句
#N • 原创论文作者不超过 7 位
#N • 必须有正式的 Limitations 部分
#N • 修回时须提交 summary sentence（不超过 35 词）和 3–6 条 Take-Home Points
#N • 初投提交隐去作者信息的正文（修回版的文件清单写的是 "Main Manuscript File (Unmasked)"，由此推断初投为盲审）

#N 投稿时如果系统要求与上面不同，以系统为准，把截图发我即可。

#H1 七、投稿前最后自检

#N 1. 盲审正文中无 "Wuhan"、"Yang"、"Shu"、"Bian" 等身份信息；全部 docx 的文档属性（作者、上次保存者）已清空。
#N 2. 标题 121 字符；摘要 245 词；正文 2,990 词；图表 7 个；作者 7 位。
#N 3. Title Page、投稿系统表单和正文 Declarations 三处内容一致。
#N 4. Cover Letter 日期已改为实际投稿日。
