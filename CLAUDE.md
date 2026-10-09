# 项目记忆

## 用户的固定要求

- **不用管"论文投稿审查评议"。** 指医院投稿前审查用的答辩 PPT 及配套材料（如原始数据分析记录）。不要制作、更新，也不要在待办事项里提醒。（用户 2026-10-08 明确要求）

## 项目现状（2026-10-08）

- 稿件：Routine Ultrasound Reports for Pediatric Intestinal Malrotation Rarely Document Duodenal Landmarks: A Single-Center Audit。病例报告审计（case-only），结局是报告层面检出率，不是敏感度。
- 当前目标期刊：*Journal of the American College of Radiology*（JACR），Original Article。投稿经过：
  - *Pediatric Radiology*：外审后退稿。
  - *Insights into Imaging*：2026-09-30 因范围不符直接退稿，未送外审。
- 作者 7 人：Jun Shu, Fei Peng, Kai Zheng, Haiyan Lei, Zhengliang Meng, Hongqiang Bian, Jun Yang（通讯作者）。Guanghua Zhang、Hongxi Guo、Haibin Wang 在致谢里。
- 投稿文件在仓库根目录（`JACR_*`、`Supplement_1_classifier.py`）。文稿源文件在 `analysis/manuscript_source_jacr/`。构建命令见 `analysis/README.md`。
- JACR 作者须知以用户提供的 `analysis/manuscript_source_jacr/JACR_Guide_for_Authors_2026-10-08.pdf` 为准（图片版 PDF，需逐页看图读取）。要点：初投时图和表放在正文里；Title Page 必须有 Data Statement 固定句、领导职务、按 ICMJE 分项的贡献；利益冲突声明单独上传，不写在 Title Page 上。
- 生成式 AI 声明：用户决定如实声明（Claude 协助起草、语言润色和分析代码），按 JACR 模板写在参考文献之前。不要把声明改窄。
- 改稿后必须重新构建，并运行 `python3 analysis/manuscript_source_jacr/jacr_check.py`。它会核对 JACR 的各项上限、盲审隐去信息、美式拼写和参考文献格式。
- 渲染 docx/pptx 需要 LibreOffice 的 writer/impress 组件。新环境里只有 core，需要先 `apt-get install libreoffice-writer libreoffice-impress libreoffice-calc poppler-utils`（xlsx 公式重算需要 calc）。
- 审稿自查（2026-10-08）发现 S1 参考标准、S2 术前时间、S3 超声内容未人工验证三项严重问题。用户 2026-10-09 填回核对表（`analysis/review_returns/`），已并入分析：`analysis/review_merge.py` → `review_exclusions.csv`、`us_manual_coding.csv`，由 `core.py`、`usaudit4.py` 应用。复发再次手术 9 例主分析排除（用户决定，不做敏感性分析）；S3 的 5 格分歧按我提出的裁定（用户同意）。
- 重算后（2026-10-09）：队列 450，影像 398，索引检查 723；UGI 230/293、CT 165/313、US 64/117；D3/DJJ 3/117，SMA–SMV 关系 3/117，漩涡征 59/117；超声时代效应粗 AME +18.7（−0.2 至 +37.7），已不显著。
- S3 阅读者：甲为超声科医师，乙为小儿外科医师（用户 2026-10-09 告知，已写入 Methods、Table 3 注、补充材料 1 K3、Cover Letter）。姓名未告知，Title Page 贡献未改；S1/S2 由谁判定也未告知。
- 审稿自查 S4–S6 已改（2026-10-09）：Table 2 新增"只计点名旋转不良"一列（UGI 77.8%、CT 48.6%、US 53.8%；超声阳性报告无一只写扭转）；"超声是扭转检查"降为描述；删去"技术因素真实存在"，引言按 [13] 的实际设计重写，去掉 "under dedicated protocols"；时间趋势从摘要删除，正文、表 4、补充材料 2 均标为探索性，讨论中不再用科室说法佐证。正文 2,959 词，摘要 245 词。
- 审稿自查一般问题和语言问题已改（2026-10-09）：病例来源改为"科研数据库 711 例 → 559 条手术记录/499 例"，图 1 加了不符合标准的 34 例；锚定手术 = 首次符合条件的手术；超声由超声科医师、CT/UGI 由放射科医师报告；复核人注明是作者之一，kappa 0.83（95% CI 0.61–1.00）；GEE 比值比移出正文；表格模态名统一为 Ultrasound / UGI series；表 3 注补全预约重叠；表 4 平均边际效应加 bootstrap CI（UGI 用独立随机流）；表 1"反复"一行改名并注明；图内说明文字移到图注；P 值改 AMA 格式（斜体 P、无前导零）；新增参考文献 [25] El-Ali 2025（已核对）。正文 2,979 词，摘要 248 词。
- 用户已确认（2026-10-09）：科研数据库按诊断导出（正文写作 "a recorded diagnosis of intestinal malrotation"）；超声由超声科医师报告（正文写作 "Ultrasound was reported by ultrasound physicians"，只写"报告"，不写"完成"）。正文 2,977 词。
- 审稿自查中尚未处理：S7（期刊定位）。
