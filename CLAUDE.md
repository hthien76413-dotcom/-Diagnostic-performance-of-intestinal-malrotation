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
- 改稿后必须重新构建，并运行 `python3 analysis/manuscript_source_jacr/jacr_check.py`。它会核对 JACR 的各项上限、盲审隐去信息、美式拼写和参考文献格式。
- 渲染 docx/pptx 需要 LibreOffice 的 writer/impress 组件。新环境里只有 core，需要先 `apt-get install libreoffice-writer libreoffice-impress poppler-utils`。
