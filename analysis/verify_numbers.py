# -*- coding: utf-8 -*-
"""Number-by-number check of the JACR manuscript, tables, figures, supplements
and cover letter against an independent recomputation (verify_facts.py).

Every numeric token in the text is either matched to a check row here or is
reported as unchecked when the script runs, so nothing is skipped silently.
Writes ../数字核对表.xlsx.

    python3 verify_numbers.py
"""
import re, io, math, json
import docx
exec(open('verify_facts.py').read())

MS = 'manuscript_source_jacr/'
OUT_XLSX = ROOT + '数字核对表.xlsx'
ROWS = []          # (loc, orig, result, issue, fix, status, para)
COVER = {}         # para -> list of tokens claimed


def num(s):
    return float(str(s).replace(',', '').replace('−', '-').replace('–', '-'))


def close(printed, value, nd=1):
    """printed value equals value rounded to nd decimals (half-up or half-even)."""
    p = num(printed)
    return abs(p - value) <= 0.5 * 10 ** -nd + 1e-9


def pc(k, n):
    return 100 * k / n


def add(loc, orig, result, ok=True, issue='', fix='', status=None, para=None, toks=()):
    if status is None:
        status = '一致' if ok else '不一致'
    if not issue:
        issue = '无' if status in ('一致', '定义/描述性数字') else issue
    if not fix:
        fix = '无需修改' if status in ('一致', '定义/描述性数字') else fix
    result = re.sub(r'\((\d+), (\d+)\)', r'\1/\2', str(result))
    ROWS.append((loc, orig, f'【{status}】{result}', issue, fix, status, para))
    if para:
        COVER.setdefault(para, []).extend(str(t) for t in toks)


def rate(k, n, printed_pct, nd=1):
    v = pc(k, n)
    return close(printed_pct, v, nd), f'{k}/{n} = {v:.3f}%'


def wil(k, n, lo, hi, nd=1):
    a, b = wilson(k, n)
    return close(lo, a, nd) and close(hi, b, nd), f'Wilson {a:.2f}–{b:.2f}'


def para_of(path, startswith):
    for i, l in enumerate(io.open(path, encoding='utf-8').read().split('\n'), 1):
        if l.startswith(startswith):
            return f'{path.split("/")[-1]}:{i}'
    raise KeyError(startswith)


T1, T2, T3, T4 = F['T1'], F['T2'], F['T3'], F['T4']
LIT13 = '文献 [13]（Nguyen 等，AJR 2025，PMID 40499019）摘要：旋转不良敏感度原始报告 93%、盲法复读 97%；D3 位置为最准确单一征象（98%）。2026-10-10 检索核对'
LIT11 = '文献 [11]（Nguyen 等，Arch Dis Child 2021）：17 项研究、2,257 例、合并敏感度 94%（95% CI 89–97）。2026-10-10 检索核对'
LITACR = ('文献 [19]（ACR Appropriateness Criteria Vomiting in Infants，J Am Coll Radiol 2020;17(11S):S505-S515，PMID 33153561）：'
          '出生 2 天后的胆汁性呕吐（疑似旋转不良）一项，UGI 造影 "usually appropriate"、超声 "may be appropriate"（文中称超声在此人群中有争议）；'
          '"predate most of this evidence"：[11] 2021、[12] 2022、[13] 2025、[14] 2021 均晚于 2020 年 11 月。题录（题目、卷页、DOI、PMID）2026-10-10 检索核对；评级未能对照原文')
LIT14 = '文献 [14]（Binu 等，J Pediatr Surg 2021，单中心 Adelaide）：539 例因临床怀疑行超声。2026-10-10 检索核对'

# =============================================================== ABSTRACT
P = para_of(MS + 'p1.md', '#N **Objective:**')
add('摘要 · Objective', '93–97%', LIT13, True, para=P, toks=('93', '97'))
P = para_of(MS + 'p1.md', '#N **Methods:**')
add('摘要 · Methods', 'December 2012–June 2026', f'队列首次手术日期 {coh.op_dt.min():%Y-%m-%d} 至 {coh.op_dt.max():%Y-%m-%d}，均在研究期内', para=P, toks=('2012', '2026'))
add('摘要 · Methods', 'Wilson 95% CIs', '方法描述；全文检出率区间均按 Wilson 法复算（见下）', status='定义/描述性数字', para=P, toks=('95',))
P = para_of(MS + 'p1.md', '#N **Results:**')
add('摘要 · Results', '450 children', f'队列 {F["cohort"]} 例（465 例经复核排除 {F["excluded"]} 例）', F['cohort'] == 450, para=P, toks=('450',))
ok, r = rate(F['volvulus'], F['cohort'], '88.2')
add('摘要 · Results', 'volvulus in 88.2%', f'{r}', ok, para=P, toks=('88.2',))
add('摘要 · Results', '398 underwent at least one index test', f'有索引检查者 {F["imaged"]} 例；{F["imaged"]} + 无索引检查 {F["none"]} = {F["imaged"] + F["none"]} = 队列', F['imaged'] == 398, para=P, toks=('398',))
ok1, r1 = rate(T3['d3_or_djj']['n'], F['n_US'], '2.6'); ok2, r2 = wil(3, 117, '0.9', '7.3')
add('摘要 · Results', 'Three of 117 ultrasound examinations (2.6%, 95% CI 0.9–7.3) documented D3 or DJJ',
    f'{r1}；{r2}；两位阅读者裁定后编码', ok1 and ok2 and T3['d3_or_djj']['n'] == 3, para=P, toks=('Three', '117', '2.6', '95', '0.9', '7.3'))
ok, r = rate(T3['sma_smv']['n'], 117, '2.6')
add('摘要 · Results', '3 (2.6%) the mesenteric artery–vein relationship', r, ok and T3['sma_smv']['n'] == 3, para=P, toks=('3', '2.6'))
ok, r = rate(T3['fluid']['n'], 117, '1.7')
add('摘要 · Results', '2 (1.7%) enteric fluid', r, ok and T3['fluid']['n'] == 2, para=P, toks=('2', '1.7'))
ok, r = rate(T3['whirl_pos']['n'], 117, '50.4')
add('摘要 · Results', 'a whirlpool sign was reported in 50.4%', f'{T3["whirl_pos"]["n"]}/117；{r}', ok, para=P, toks=('50.4',))
ok1, r1 = rate(T2['US']['k'], T2['US']['n'], '54.7'); ok2, r2 = wil(64, 117, '45.7', '63.4')
add('摘要 · Results', '64 of 117 examinations (54.7%, 45.7–63.4)', f'{r1}；{r2}', ok1 and ok2 and T2['US']['k'] == 64, para=P, toks=('64', '117', '54.7', '45.7', '63.4'))
add('摘要 · Results', 'in all 59 recording a whirlpool … and in 5 of 58 without one',
    f'记录漩涡征 {T3["whirl_pos"]["det_yes"][0]}/{T3["whirl_pos"]["det_yes"][1]} 检出；未记录 {T3["whirl_pos"]["det_no"][0]}/{T3["whirl_pos"]["det_no"][1]}；59+58=117，59+5=64 与总检出一致',
    T3['whirl_pos']['det_yes'] == (59, 59) and T3['whirl_pos']['det_no'] == (5, 58), para=P, toks=('59', '5', '58'))
add('摘要 · Results', 'whirlpool … in 59 of 112 children with operatively confirmed volvulus',
    f'做超声且术中扭转者 {F["whirl_in_volv"][1]} 例，其中记录漩涡征 {F["whirl_in_volv"][0]} 例；分母为扭转患儿，与上句分母 117 不同，用法正确',
    F['whirl_in_volv'] == (59, 112), para=P, toks=('59', '112'))
ok, r = rate(T2['US']['named'], 117, '53.8')
add('摘要 · Results', 'Detection was 53.8% counting only conclusions naming malrotation', f'{T2["US"]["named"]}/117；{r}', ok, para=P, toks=('53.8',))
us_ex = T2['US']['k'] - T2['US']['poss']
ok, r = rate(us_ex, 117, '25.6')
add('摘要 · Results', '25.6% excluding tentative wording',
    f'按合并同日报告（索引单位）的结论复算："可能"级 {T2["US"]["poss"]} 份，(64−{T2["US"]["poss"]})/117 = {us_ex}/117 = {pc(us_ex,117):.1f}%（2026-10-10 已由 27.4% 更正）',
    ok, para=P, toks=('25.6',))

# =============================================================== INTRODUCTION
P = para_of(MS + 'p1.md', '#N The upper gastrointestinal (UGI) contrast series')
add('引言 第2段', '93–97%；17 studies and 2,257 children；pooled sensitivity of 94%；539 children',
    LIT13 + '；' + LIT11 + '；' + LIT14, True, para=P, toks=('93', '97', '17', '2,257', '94', '539'))
add('引言 第2段', 'The 2020 ACR Appropriateness Criteria … "may be appropriate" … "usually appropriate" … infants older than 2 days [19]', LITACR, status='需核对原始文献', para=P, toks=('2020', '2'),
    issue='未能打开原文；检索摘录之间有出入（JACR 网页版表格与 ACR 检索页不一致）', fix='投稿前打开 acsearch.acr.org 的 Vomiting in Infants，核对 Variant 5 的评级；若不同，改引言与投稿信各一句')
P = para_of(MS + 'p1.md', '#N The 2025 multicenter series')
add('引言 第3段', '2025 multicenter series', '文献 [13] 发表年份 2025（参考文献列表一致）', status='定义/描述性数字', para=P, toks=('2025',))
P = para_of(MS + 'p1.md', '#N We therefore audited')
add('引言 第4段', '13.6 years', f'2012 年 12 月至 2026 年 6 月共 {F["study_months"]} 个月 = {F["study_months"]/12:.2f} 年（2026-10-10 由 13.5 更正）',
    close('13.6', F['study_months'] / 12), para=P, toks=('13.6',))

# =============================================================== METHODS
P = para_of(MS + 'p1.md', '#N This was a retrospective')
add('方法 · 设计', 'STROBE [21]', '引文编号，非数据', status='定义/描述性数字', para=P, toks=())
P = para_of(MS + 'p1.md', '#N The institutional clinical research database')
add('方法 · 研究对象', '711 children', f'原始导出"病案首页基本信息"唯一患者 {F["db_children"]} 例；按诊断导出（用户 2026-10-09 确认）', F['db_children'] == 711, para=P, toks=('711',))
add('方法 · 研究对象', 'December 2012 and June 2026', '同摘要', para=P, toks=('2012', '2026'))
add('方法 · 研究对象', '559 operative records in 499 children', f'手术记录表 {F["ops_all_records"]} 条、{F["ops_all_children"]} 例', (F['ops_all_records'], F['ops_all_children']) == (559, 499), para=P, toks=('559', '499'))
add('方法 · 研究对象', '503 records in 465 children', f'入选 {F["ops_sel_records"]} 条、{F["ops_sel_children"]} 例；未入选 {F["not_eligible_records"]} 条、{F["not_eligible_children"]} 例（559−503=56；499−465=34）',
    (F['ops_sel_records'], F['ops_sel_children']) == (503, 465), para=P, toks=('503', '465'))
add('方法 · 研究对象', 're-read for 34 children … 19 were retained and 15 excluded, 6 … and 9',
    f'S1 核对表 {F["s1_reviewed"]} 例：保留 {F["s1_keep"]}、非本次确认 {F["s1_notconf"]}、复发再手术 {F["s1_reop"]}；{F["s1_keep"]}+{F["s1_notconf"]}+{F["s1_reop"]}={F["s1_keep"]+F["s1_notconf"]+F["s1_reop"]}',
    (F['s1_reviewed'], F['s1_keep'], F['excluded'], F['s1_notconf'], F['s1_reop']) == (34, 19, 15, 6, 9),
    para=P, toks=('34', '19', '15', '6', '9'))
add('方法 · 研究对象', 'The remaining 450 consecutive children', f'465 − 15 = {465-15}；队列 {F["cohort"]}', F['cohort'] == 450, para=P, toks=('450',))
P = para_of(MS + 'p1.md', '#N Three modalities were evaluated')
add('方法 · 索引检查', 'Three modalities', 'UGI、CT、超声', status='定义/描述性数字', para=P, toks=('Three',))
add('方法 · 索引检查', 'the 154 same-day reports and the 27 index examinations more than 7 days before operation',
    f'S2 核对表：手术当日 {F["s2_same_day"]} 份、距术 >7 天 {F["s2_over7"]} 份（最长 {F["s2_max_gap"]} 天）。注意这是在排除前 465 例中核对的数量',
    (F['s2_same_day'], F['s2_over7']) == (154, 27), para=P, toks=('154', '27', '7'))
add('方法 · 索引检查', 'three issued after the operation or for an unrelated earlier illness were removed',
    f'术后 {F["s2_postop"]} 份 + 无关病程 {F["s2_unrelated"]} 份 = 4 份；其中 1 份属 S1 已排除患儿，队列内实际删除 {F["reports_removed_in_cohort"]} 份',
    F['reports_removed_in_cohort'] == 3, para=P, toks=('three',))
add('方法 · 索引检查', '723 index examinations from 761 reports; 32 earlier repeat examinations',
    f'索引检查次 {F["index_exams"]} = 293+313+117；纳入索引检查次的报告 {F["reports_in_index"]}；更早的重复报告 {F["earlier_reports"]}；761+32 = {F["eligible_reports"]}（图 1 的 793）',
    (F['index_exams'], F['reports_in_index'], F['earlier_reports']) == (723, 761, 32), para=P, toks=('723', '761', '32'))
P = para_of(MS + 'p1.md', '#N Ultrasound was reported by ultrasound physicians')
P = para_of(MS + 'p1.md', '#N Each ultrasound index examination was coded by two readers')
add('方法 · 内容编码', 'two readers … twelve elements', f'阅读表 12 个条目；两位阅读者（超声科医师、小儿外科医师，用户确认）', len(items) == 12, para=P, toks=('two', 'twelve'))
P = para_of(MS + 'p1.md', '#N An examination was classified as positive')
add('方法 · 阳性定义', '—', '本段无数字', status='定义/描述性数字', para=P, toks=())
P = para_of(MS + 'p1.md', '#N Report text was classified using')
v = F['val']
add('方法 · 复核', 'adjudicated 32 reports … random sample of 24 … targeted review of 8',
    f'抽查验证 {v["n"]} 份 + 潜在漏判 {F["targeted"]["unique"]} 份（表中 {F["targeted"]["rows"]} 行，其中 2 行为同一份报告 4921963）= {v["n"]+F["targeted"]["unique"]}',
    (v['n'], F['targeted']['unique']) == (24, 8), para=P, toks=('32', '24', '8'))
add('方法 · 复核', 'agreement was 92% (Cohen kappa 0.83, 95% CI 0.61–1.00)',
    f'{v["agree"]}/{v["n"]} = {pc(v["agree"],v["n"]):.1f}%；kappa {v["kappa"]:.3f}；渐近 95% CI {v["ci"][0]:.2f}–{v["ci"][1]:.2f}（上限截断为 1）',
    close('92', pc(v['agree'], v['n']), 0) and close('0.83', v['kappa'], 2) and close('0.61', v['ci'][0], 2), para=P, toks=('92', '0.83', '95', '0.61', '1.00'))
add('方法 · 复核', 'found 5 further under-calls', f'潜在漏判中医师判阳 {F["targeted"]["undercalls"]} 份', F['targeted']['undercalls'] == 5, para=P, toks=('5',))
add('方法 · 复核', 'returned nine positives … three of which … over-calls',
    f'待核清单 {F["nine"]} 例；label_corrections.csv 更正 {len(pd.read_csv("label_corrections.csv"))} 例', F['nine'] == 9 and len(pd.read_csv('label_corrections.csv')) == 3,
    para=P, toks=('nine', 'three'))
P = para_of(MS + 'p1.md', '#N Detection rates are presented')
add('方法 · 统计', 'Wilson 95% … era (2012–2018 vs 2019–2026)', '分期边界 2019 年（op_year ≥ 2019 为后期）', status='定义/描述性数字', para=P, toks=('95', '2012', '2018', '2019', '2026'))
add('方法 · 统计', 'no ultrasound examination was positive among the five children without volvulus',
    f'超声且无扭转 {F["ST"][("US","novolv")][1]} 例，检出 {F["ST"][("US","novolv")][0]} 例', F['ST'][('US', 'novolv')] == (0, 5), para=P, toks=('five',))
add('方法 · 统计', 'the era boundary was varied from 2019 to 2022', '补充表 S9 含 2019/2020/2021/2022 四个边界', status='定义/描述性数字', para=P, toks=('2019', '2022'))
add('方法 · 统计', 'Python 3.11 (statsmodels 0.15, SciPy 1.17)',
    f'运行环境：Python {F["software"]["python"]}，statsmodels {F["software"]["statsmodels"]}，SciPy {F["software"]["scipy"]}（2026-10-10 由 3.12 更正）',
    F['software']['python'].startswith('3.11') and F['software']['statsmodels'].startswith('0.15') and F['software']['scipy'].startswith('1.17'), para=P, toks=('3.11', '0.15', '1.17'))

# =============================================================== RESULTS
P = para_of(MS + 'p2.md', '#N Of 450 children')
ok1, r1 = rate(F['neonates'], 450, '66.7'); ok2, r2 = rate(F['volvulus'], 450, '88.2')
add('结果 · 队列 第1段', '450 children, 300 (66.7%) neonates and 397 (88.2%) volvulus', f'新生儿 {F["neonates"]}：{r1}；扭转 {F["volvulus"]}：{r2}',
    ok1 and ok2 and (F['neonates'], F['volvulus']) == (300, 397), para=P, toks=('450', '300', '66.7', '397', '88.2'))
add('结果 · 队列 第1段', 'UGI 293, CT 313, ultrasound 117; 398 at least one; 59 all three',
    f'UGI {F["n_UGI"]}、CT {F["n_CT"]}、超声 {F["n_US"]}；≥1 项 {F["imaged"]}；三项均做 {F["all_three"]}。三组有重叠，相加 723 ≠ 398 属正常',
    (F['n_UGI'], F['n_CT'], F['n_US'], F['imaged'], F['all_three']) == (293, 313, 117, 398, 59), para=P, toks=('293', '313', '117', '398', '59'))
ok, r = rate(F['none'], 450, '11.6')
add('结果 · 队列 第1段', 'The remaining 52 (11.6%) … in four documented before transfer',
    f'{F["none"]} = 450 − 398；{r}；无院内影像 {F["a55_none"]} 例，均有院外影像记录（{F["a55_none_outside"]}/{F["a55_none"]}）',
    ok and F['none'] == 52 and F['a55_none'] == 4 == F['a55_none_outside'], para=P, toks=('52', '11.6', 'four'))
P = para_of(MS + 'p2.md', '#N The modality groups were not interchangeable')
e, l = F['us_rate_early'], F['us_rate_late']
add('结果 · 队列 第2段', 'its use rising from 13% to 51% of operated children',
    f'前期 {e[0]}/{e[1]} = {pc(*e):.1f}%；后期 {l[0]}/{l[1]} = {pc(*l):.1f}%（分母为该期全部手术患儿，与表 1 "Operated 2019–2026" 的分母不同）',
    close('13', pc(*e), 0) and close('51', pc(*l), 0), para=P, toks=('13', '51'))
add('结果 · 队列 第2段', 'Ultrasound was performed more often in children with volvulus',
    f'扭转患儿做超声 {F["us_given_volv"][0]}/{F["us_given_volv"][1]} = {pc(*F["us_given_volv"]):.1f}%；无扭转 {F["us_given_novolv"][0]}/{F["us_given_novolv"][1]} = {pc(*F["us_given_novolv"]):.1f}%（未做检验，描述性）',
    True, para=P, toks=())
po = F['POS']
add('结果 · 队列 第2段', 'UGI last in 75.0% … against 19.2% for CT … 80.0% [144/180] vs 70.0% [42/60]',
    f'≥2 项索引检查者中：UGI 为最后一项 {po["UGI"]["last"]}/{po["UGI"]["had"]} = {pc(po["UGI"]["last"],po["UGI"]["had"]):.1f}%；CT {po["CT"]["last"]}/{po["CT"]["had"]} = {pc(po["CT"]["last"],po["CT"]["had"]):.1f}%；UGI 检出 最后 {po["UGI"]["det_last"]:.1f}% vs 较早 {po["UGI"]["det_earlier"]:.1f}%',
    close('75.0', pc(po['UGI']['last'], po['UGI']['had'])) and close('19.2', pc(po['CT']['last'], po['CT']['had'])) and close('80.0', po['UGI']['det_last']) and close('70.0', po['UGI']['det_earlier']),
    para=P, toks=('75.0', '19.2', '80.0', '144', '180', '70.0', '42', '60'))
P = para_of(MS + 'p2.md', '#N Detection was 230/293')
for m, s, k_, n_, pct_, lo_, hi_ in [('UGI', 'UGI series', 230, 293, '78.5', '73.4', '82.8'), ('CT', 'CT', 165, 313, '52.7', '47.2', '58.2'), ('US', 'ultrasound', 64, 117, '54.7', '45.7', '63.4')]:
    ok1, r1 = rate(T2[m]['k'], T2[m]['n'], pct_); ok2, r2 = wil(T2[m]['k'], T2[m]['n'], lo_, hi_)
    add('结果 · 检出率 段', f'{k_}/{n_} ({pct_}%, {lo_}–{hi_}) for {s}', f'{r1}；{r2}', ok1 and ok2 and (T2[m]['k'], T2[m]['n']) == (k_, n_),
        para=P, toks=(f'{k_}/{n_}'.split('/')[0], str(n_), pct_, lo_, hi_) + (('95',) if m == 'UGI' else ()))
g = F['GEE']
add('结果 · 检出率 段', 'In a GEE model adjusted for era and age group, CT and ultrasound remained less often positive',
    f'GEE 调整 OR：CT {g["ct_a"][0]:.2f} ({g["ct_a"][1]:.2f}–{g["ct_a"][2]:.2f}) P={g["ct_a"][3]:.2g}；超声 {g["us_a"][0]:.2f} ({g["us_a"][1]:.2f}–{g["us_a"][2]:.2f}) P={g["us_a"][3]:.2g}；文字与 P 值一致（同一软件重拟合）',
    g['ct_a'][2] < 1 and g['us_a'][2] < 1, para=P, toks=())
ugi_ex = T2['UGI']['k'] - T2['UGI']['poss']; ct_ex = T2['CT']['k'] - T2['CT']['poss']
add('结果 · 检出率 段', 'Reclassifying possible-tier conclusions … 50.2%, 32.9% and 25.6%',
    f'按合并检查次结论复算："可能"级 UGI {T2["UGI"]["poss"]}、CT {T2["CT"]["poss"]}、超声 {T2["US"]["poss"]}；'
    f'{ugi_ex}/293 = {pc(ugi_ex,293):.1f}%，{ct_ex}/313 = {pc(ct_ex,313):.1f}%，{us_ex}/117 = {pc(us_ex,117):.1f}%',
    close('50.2', pc(ugi_ex, 293)) and close('32.9', pc(ct_ex, 313)) and close('25.6', pc(us_ex, 117)), para=P, toks=('50.2', '32.9', '25.6'))
add('结果 · 检出率 段', 'counting only conclusions that named malrotation gave 77.8%, 48.6% and 53.8%',
    f'{T2["UGI"]["named"]}/293 = {pc(T2["UGI"]["named"],293):.1f}%；{T2["CT"]["named"]}/313 = {pc(T2["CT"]["named"],313):.1f}%；{T2["US"]["named"]}/117 = {pc(T2["US"]["named"],117):.1f}%',
    close('77.8', pc(T2['UGI']['named'], 293)) and close('48.6', pc(T2['CT']['named'], 313)) and close('53.8', pc(T2['US']['named'], 117)), para=P, toks=('77.8', '48.6', '53.8'))
P = para_of(MS + 'p2.md', '#N Of the 117 ultrasound index examinations')
ok2, r2 = wil(3, 117, '0.9', '7.3')
add('结果 · 超声内容 第1段', 'Of the 117 … three (2.6%; 95% CI 0.9–7.3) D3/DJJ and seven (6.0%) duodenum',
    f'D3/DJJ {T3["d3_or_djj"]["n"]}；{r2}；十二指肠 {T3["duodenum"]["n"]}/117 = {pc(T3["duodenum"]["n"],117):.2f}%',
    ok2 and T3['d3_or_djj']['n'] == 3 and T3['duodenum']['n'] == 7 and close('6.0', pc(7, 117)), para=P, toks=('117', 'three', '2.6', '95', '0.9', '7.3', 'seven', '6.0'))
add('结果 · 超声内容 第1段', 'Three (2.6%) … artery–vein relationship, and only one … inverted, one of the two … positivity criteria',
    f'动静脉关系 {T3["sma_smv"]["n"]}；换位 {T3["inversion"]["n"]}；超声阳性标准为漩涡征与换位两项（方法）', T3['sma_smv']['n'] == 3 and T3['inversion']['n'] == 1,
    para=P, toks=('Three', '2.6', 'one', 'two'))
add('结果 · 超声内容 第1段', 'Enteric fluid twice, graded compression once; whirlpool 59 (50.4%); bowel gas 36 (30.8%)',
    f'给液 {T3["fluid"]["n"]}；加压 {T3["compress"]["n"]}；漩涡征 {T3["whirl_pos"]["n"]} ({pc(59,117):.2f}%)；肠气 {T3["gas_limit"]["n"]} ({pc(36,117):.2f}%)',
    (T3['fluid']['n'], T3['compress']['n'], T3['whirl_pos']['n'], T3['gas_limit']['n']) == (2, 1, 59, 36) and close('30.8', pc(36, 117)),
    para=P, toks=('twice', 'once', '59', '50.4', '36', '30.8'))
add('结果 · 超声内容 第1段', 'Reader agreement was 1,423 of 1,428 item codes in the 119 episodes read (kappa 0.80–1.00)',
    f'一致 {F["cells_agree"]}/{F["cells"]}；各项 kappa 最小 {min(v["kappa"] for v in F["KAP"].values()):.2f}、最大 {max(v["kappa"] for v in F["KAP"].values()):.2f}',
    (F['cells_agree'], F['cells']) == (1423, 1428) and close('0.80', min(v['kappa'] for v in F['KAP'].values()), 2),
    para=P, toks=('1,423', '1,428', '119', '0.80', '1.00'))
P = para_of(MS + 'p2.md', '#N Of these three, only one, in 2022')
add('结果 · 超声内容 第2段', 'Of these three, only one, in 2022, followed D3 between the artery and the aorta and identified the duodenojejunal junction',
    f'记录 D3/DJJ 的 3 次检查年份 {F["d3_years"]}；记录十二指肠空肠曲的只有 1 次（DJJ {int(u["djj"].astype(bool).sum())}），即 2022 年那次', F['d3_years'] == [2018, 2022, 2024] and pd.to_datetime(u.loc[u['djj'].astype(bool), '检查时间']).dt.year.tolist() == [2022],
    para=P, toks=('three', 'one', '2022'))
P = para_of(MS + 'p2.md', '#N The diagnosis was named in all 59')
ok2, r2 = wil(5, 58, '3.7', '18.6')
add('结果 · 超声内容 第3段', 'all 59 … 5 of the 58 without one (8.6%, 95% CI 3.7–18.6); all 59 conclusions also named malrotation',
    f'{T3["whirl_pos"]["det_yes"]}、{T3["whirl_pos"]["det_no"]}；5/58 = {pc(5,58):.2f}%；{r2}；记录漩涡征且结论点名旋转不良 {F["whirl_named_mal"]}/59',
    ok2 and close('8.6', pc(5, 58)) and F['whirl_named_mal'] == 59, para=P, toks=('59', '5', '58', '8.6', '95', '3.7', '18.6', '59'))
add('结果 · 超声内容 第3段', 'whirlpool … in only 59 of the 112 children (52.7%)', f'{F["whirl_in_volv"]}；{pc(59,112):.2f}%', close('52.7', pc(59, 112)), para=P, toks=('59', '112', '52.7'))
P = para_of(MS + 'p2.md', '#N In this exploratory analysis')
u4 = T4['US']; bu = F['AME_boot']
add('结果 · 时间趋势', 'ultrasound 42.1% (16/38) in 2012–2018 and 60.8% (48/79) in 2019–2026',
    f'{u4["early"]} = {pc(*u4["early"]):.2f}%；{u4["late"]} = {pc(*u4["late"]):.2f}%；38+79 = 117，16+48 = 64',
    u4['early'] == (16, 38) and u4['late'] == (48, 79), para=P, toks=('42.1', '16', '38', '2012', '2018', '60.8', '48', '79', '2019', '2026'))
add('结果 · 时间趋势', '+18.7 percentage points whose 95% CI (−0.2 to +37.7) includes zero',
    f'自写 logistic 的平均边际效应 {u4["ame_crude"]:+.2f}；bootstrap 区间 {bu["Ultrasound, crude"][1][0]:+.2f} 至 {bu["Ultrasound, crude"][1][1]:+.2f}（原程序固定种子，2,000 次）；"includes zero"与区间一致；粗 OR P = {u4["or_crude"][3]:.3f}，亦不显著',
    close('18.7', u4['ame_crude']) and close('-0.2', bu['Ultrasound, crude'][1][0]), para=P, toks=('18.7', '95', '0.2', '37.7'))
add('结果 · 时间趋势', 'CT detection rose and UGI detection did not',
    f'CT 粗 OR {T4["CT"]["or_crude"][0]:.2f}，P = {T4["CT"]["or_crude"][3]:.3f}；UGI 粗 OR {T4["UGI"]["or_crude"][0]:.2f}，P = {T4["UGI"]["or_crude"][3]:.3f}；文字与 P 值一致', True, para=P, toks=())
vs = F['ves_share']
add('结果 · 时间趋势', 'great-vessel study rose from 34.2% to 68.4%', f'{vs[0][0]}/{vs[0][1]} = {pc(*vs[0]):.2f}%；{vs[1][0]}/{vs[1][1]} = {pc(*vs[1]):.2f}%',
    close('34.2', pc(*vs[0])) and close('68.4', pc(*vs[1])), para=P, toks=('34.2', '68.4'))
add('结果 · 时间趋势', 'reduced the ultrasound difference to +8.4 (−10.6 to +29.2)',
    f'调整后平均边际效应 {u4["ame_adj"]:+.2f}；bootstrap {bu["Ultrasound, adjusted for great-vessel session"][1][0]:+.2f} 至 {bu["Ultrasound, adjusted for great-vessel session"][1][1]:+.2f}',
    close('8.4', u4['ame_adj']) and close('-10.6', bu['Ultrasound, adjusted for great-vessel session'][1][0]) and close('29.2', bu['Ultrasound, adjusted for great-vessel session'][1][1]),
    para=P, toks=('8.4', '10.6', '29.2'))
wh = T3['whirl_pos']; dj = T3['d3_or_djj']
add('结果 · 时间趋势', 'Whirlpool reporting rose from 39.5% to 55.7%, whereas D3/DJJ … one and two examinations',
    f'漩涡征 前期 {wh["early"]}/38 = {pc(wh["early"],38):.2f}%，后期 {wh["late"]}/79 = {pc(wh["late"],79):.2f}%；D3/DJJ {dj["early"]} 与 {dj["late"]}',
    close('39.5', pc(wh['early'], 38)) and close('55.7', pc(wh['late'], 79)) and (dj['early'], dj['late']) == (1, 2), para=P, toks=('39.5', '55.7', 'one', 'two'))
P = para_of(MS + 'p2.md', '#N Fifty-nine children underwent all three')
pcs = F['paired_chars']
add('结果 · 亚组', 'Fifty-nine … other 339 imaged children (volvulus 96.6% vs 87.9%; neonates 83.1% vs 67.3%)',
    f'三项均做 {pcs["three"][3]}，其余 {pcs["other"][3]}（59+339 = 398）；扭转 {pcs["three"][0]:.2f}% vs {pcs["other"][0]:.2f}%；新生儿 {pcs["three"][1]:.2f}% vs {pcs["other"][1]:.2f}%',
    pcs['three'][3] == 59 and pcs['other'][3] == 339 and close('96.6', pcs['three'][0]) and close('87.9', pcs['other'][0]) and close('83.1', pcs['three'][1]) and close('67.3', pcs['other'][1]),
    para=P, toks=('Fifty-nine', 'three', '339', '96.6', '87.9', '83.1', '67.3'))
ps = F['PS']['all']; pb = F['PAIR_boot']
add('结果 · 亚组', 'positive in 76.3%, 52.5%, 45.8% (Cochran Q test, P < .001)',
    f'UGI {ps["UGI"]}/59 = {pc(ps["UGI"],59):.2f}%；超声 {ps["US"]}/59 = {pc(ps["US"],59):.2f}%；CT {ps["CT"]}/59 = {pc(ps["CT"],59):.2f}%；自算 Cochran Q = {ps["Q"][0]:.2f}，P = {ps["Q"][1]:.4f}',
    close('76.3', pc(ps['UGI'], 59)) and close('52.5', pc(ps['US'], 59)) and close('45.8', pc(ps['CT'], 59)) and ps['Q'][1] < .001,
    para=P, toks=('76.3', '52.5', '45.8', '001'))
add('结果 · 亚组', 'UGI minus CT +30.5 (95% CI +13.6 to +47.5); CT minus ultrasound −6.8 (−20.3 to +8.5)',
    f'差值 {pc(ps["UGI"]-ps["CT"],59):+.2f}、{pc(ps["CT"]-ps["US"],59):+.2f}；bootstrap 区间 {pb[0][2]}；{pb[2][2]}（原程序固定种子）',
    close('30.5', pc(ps['UGI'] - ps['CT'], 59)) and close('-6.8', pc(ps['CT'] - ps['US'], 59)), para=P, toks=('30.5', '95', '13.6', '47.5', '6.8', '20.3', '8.5'))
p48 = F['PS']['48h']
add('结果 · 亚组', 'a pattern unchanged when all three examinations fell within 48 h',
    f'48 h 内 {p48["n"]} 例：UGI {p48["UGI"]}、超声 {p48["US"]}、CT {p48["CT"]}；Cochran Q P = {p48["Q"][1]:.4f}；UGI vs CT P = {p48["ugi_ct"][2]:.3f}，CT vs 超声 P = {p48["ct_us"][2]:.3f}；模式相同',
    p48['Q'][1] < .05 and p48['ct_us'][2] > .05, para=P, toks=('48',))
add('结果 · 亚组', 'Only 5 of the 53 children … no volvulus underwent ultrasound, and none had a positive report',
    f'无扭转 {F["no_volvulus"]} 例（450−397）；其中做超声 {F["us_given_novolv"][0]}，检出 {F["ST"][("US","novolv")][0]}', F['us_given_novolv'] == (5, 53) and F['ST'][('US', 'novolv')][0] == 0,
    para=P, toks=('5', '53'))

# =============================================================== DISCUSSION
P = para_of(MS + 'p3.md', '#N Over 13.6 years')
add('讨论 第1段', 'Over 13.6 years', f'{F["study_months"]} 个月 = {F["study_months"]/12:.2f} 年', close('13.6', F['study_months'] / 12), para=P, toks=('13.6',))
add('讨论 第1段', 'three of 117 examinations, enteric fluid in two', 'D3/DJJ 3；给液 2', True, para=P, toks=('three', '117', 'two'))
add('讨论 第1段', 'about half of all examinations and of the children in whom operation confirmed volvulus', '59/117 = 50.4%；59/112 = 52.7%', True, para=P, toks=('half',))
P = para_of(MS + 'p3.md', '#N Malrotation or volvulus was named in 54.7%')
add('讨论 第2段', '54.7%', '64/117 = 54.70%', close('54.7', pc(64, 117)), para=P, toks=('54.7',))
add('讨论 第2段', '93% … 97% … 2025 multicenter series [13]; pooled 94% [11]', LIT13 + '；' + LIT11, True, para=P, toks=('93', '97', '2025', '94', '2025'))
add('讨论 第2段', '25.7% of examinations for malrotation were non-diagnostic [27]', '文献 [27]：80/311 = 25.7%（原始报告；盲法复读 37.6%），2026-10-09 已检索 Springer/PubMed 摘要核对',
    close('25.7', pc(80, 311)), para=P, toks=('25.7',))
P = para_of(MS + 'p3.md', '#N Three features of the design')
add('讨论 第4段', 'Three features … the last preoperative test in 75.0% of children who had it with another index test',
    f'{po["UGI"]["last"]}/{po["UGI"]["had"]} = {pc(po["UGI"]["last"],po["UGI"]["had"]):.2f}%；"三个特征"为描述性计数（参考标准不独立、路径位置、人群不同）',
    close('75.0', pc(po['UGI']['last'], po['UGI']['had'])), para=P, toks=('Three', '75.0'))
P = para_of(MS + 'p3.md', '#N The documentation gap bears on')
add('讨论 第5段', '93–97%', LIT13, True, para=P, toks=('93', '97'))
P = para_of(MS + 'p3.md', '#N This is not a diagnostic accuracy study')
add('讨论 · 局限 第1段', 'The 52 children without an index test … as were 9 … from 88.2% to 84.0%',
    f'无索引检查 {F["none"]}；复发再手术 {F["s1_reop"]}；扭转 {F["VD"]["primary"][0]}/450 = {pc(F["VD"]["primary"][0],450):.2f}% → {F["VD"]["A"][0]}/450 = {pc(F["VD"]["A"][0],450):.2f}%',
    F['none'] == 52 and F['s1_reop'] == 9 and close('84.0', pc(F['VD']['A'][0], 450)), para=P, toks=('52', '9', '360', '88.2', '84.0'))
P = para_of(MS + 'p3.md', '#N • Routine ultrasound reports')
add('Take-Home 第1条', '2.6% of examinations', '3/117 = 2.56%', True, para=P, toks=('2.6',))
P = para_of(MS + 'p3.md', '#N • A positive routine ultrasound report')
add('Take-Home 第2条', '59 of 112 children', '同结果', True, para=P, toks=('59', '112'))
P = para_of(MS + 'p3.md', '#N **Supplement 1.**')
add('补充材料说明 · Supplement 1', 'reproduces 99.0% … the 92% above', f'参考实现与最终标签一致 {sum(v[0] for v in F["CLS"].values())}/{sum(v[1] for v in F["CLS"].values())} = {pc(sum(v[0] for v in F["CLS"].values()), sum(v[1] for v in F["CLS"].values())):.2f}%；92% 见方法',
    close('99.0', pc(sum(v[0] for v in F['CLS'].values()), sum(v[1] for v in F['CLS'].values()))), para=P, toks=('1', '99.0', '92'))
P = para_of(MS + 'p3.md', '#N **Supplement 2.**')
add('补充材料说明 · Supplement 2', '48-h and 24-h … 2019 to 2022 … 360°', '定义性数字，与补充材料 2 一致', status='定义/描述性数字', para=P, toks=('48', '24', '2019', '2022', '360'))
P = para_of(MS + 'p3.md', '#N **Supplement 3.**')
add('补充材料说明 · Supplement 3', '313 CT and 293 UGI', 'CT 313、UGI 293', True, para=P, toks=('313', '293'))
P = para_of(MS + 'p3.md', '#N **Figure 1.')
add('图注 · Figure 1', '711 … 503 … 465 … 793 … 723 … 52 … four', f'{F["db_children"]}；{F["ops_sel_records"]}/{F["ops_sel_children"]}；{F["eligible_reports"]}→{F["index_exams"]}；{F["none"]}；{F["a55_none"]}', True,
    para=P, toks=('1', '711', '503', '465', '793', '723', '52', 'three', 'four'))
P = para_of(MS + 'p3.md', '#N **Figure 2.')
add('图注 · Figure 2', 'Wilson 95% confidence intervals', '定义', status='定义/描述性数字', para=P, toks=('2', '95'))
P = para_of(MS + 'p3.md', '#N **Figure 3.')
add('图注 · Figure 3', '117 … two independent readers … the two most often documented elements in panel A … Three examinations … 5 of 58',
    f'117；2 位阅读者；B 栏两项（漩涡征 {T3["whirl_pos"]["n"]}、肠气限制 {T3["gas_limit"]["n"]}）以外各项均 ≤ 7（十二指肠 {T3["duodenum"]["n"]}）；D3/DJJ 3；5/58',
    max(T3[k]['n'] for k in ['d3_or_djj', 'duodenum', 'sma_smv', 'inversion', 'fluid', 'dynamic', 'compress', 'cecum']) == 7
    and T3['duodenum']['n'] == 7 and T3['gas_limit']['n'] == 36 and T3['whirl_pos']['n'] == 59,
    para=P, toks=('3', '117', 'two', 'seven', 'Three', 'one', '5', '58'))

# =============================================================== TABLES (built manuscript)
D = docx.Document(ROOT + 'JACR_3_Manuscript_masked.docx')
TB = [[[c.text for c in r.cells] for r in t.rows] for t in D.tables]


def cell_pct(s):
    m = re.match(r'(\d+) \(([\d.]+)\)', s); return int(m.group(1)), m.group(2)


# Table 1
t1 = TB[0]; gkeys = ['All', 'UGI', 'CT', 'US', 'none']
for row in t1[1:]:
    lab = row[0]; res = []; ok = True
    if lab.startswith('Children'):
        for gk, c in zip(gkeys, row[1:]):
            ok &= int(c) == T1[gk]['n']; res.append(f'{gk} {T1[gk]["n"]}')
        res.append(f'UGI/CT/超声组有重叠，不应相加；有检查组 398 + 无检查组 52 = 450')
    elif lab.startswith('Age at operation'):
        for gk, c in zip(gkeys, row[1:]):
            m = re.match(r'(\d+) \((\d+)–(\d+)\)', c); med, q1, q3 = T1[gk]['age']
            ok &= close(m.group(1), med, 0) and close(m.group(2), q1, 0) and close(m.group(3), q3, 0)
            res.append(f'{gk} {med:.1f} ({q1:.1f}–{q3:.1f})')
    else:
        key = {'Neonate': 'neonate', 'Age >1 year': 'older', 'Male': 'male', 'Operated 2019': 'era_late', 'Midgut volvulus': 'volvulus',
               'Vomiting': 'vomit', 'Bilious': 'bilious', 'Abdominal distension': 'distension', 'Blood in stool': 'bloody_stool',
               'Abdominal pain': 'abd_pain', 'Gastrointestinal symptoms': 'symptoms_1m', 'Shock': 'shock'}
        k = [v for kk, v in key.items() if lab.startswith(kk)][0]
        for gk, c in zip(gkeys, row[1:]):
            n_, p_ = cell_pct(c); n0 = T1[gk]['n']
            ok &= n_ == T1[gk][k] and close(p_, pc(n_, n0))
            res.append(f'{gk} {T1[gk][k]}/{n0}={pc(T1[gk][k], n0):.2f}%')
    add(f'表 1 · {lab}', ' | '.join(row[1:]), '；'.join(res), ok,
        issue='' if ok else '与独立复算不符', fix='' if ok else '按复核结果修改')
# Table 1 internal: neonate + 29d–1y + >1y = n is not shown; age groups checked via strata below

# Table 2
t2 = TB[1]
for row in t2[1:]:
    lab = row[0].strip()
    if lab in ('UGI series', 'Abdominal CT (all)', 'Ultrasound'):
        m = {'UGI series': 'UGI', 'Abdominal CT (all)': 'CT', 'Ultrasound': 'US'}[lab]; t = T2[m]
        k_, n_ = map(int, row[1].split('/'))
        mm_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[2])
        ok_rate = (k_, n_) == (t['k'], t['n']) and close(mm_.group(1), pc(k_, n_)) and wil(k_, n_, mm_.group(2), mm_.group(3))[0]
        tiers = [cell_pct(row[i]) for i in (3, 4, 5)]
        tsum = sum(x[0] for x in tiers)
        tok = [x[0] for x in tiers] == [t['def'], t['prob'], t['poss']]
        exc = num(row[6]); ok_exc = close(row[6], pc(t['k'] - t['poss'], t['n']))
        nm = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[7]); ok_nm = close(nm.group(1), pc(t['named'], t['n'])) and wil(t['named'], t['n'], nm.group(2), nm.group(3))[0]
        res = (f'{t["k"]}/{t["n"]} = {pc(t["k"],t["n"]):.2f}%，{wil(t["k"],t["n"],0,0)[1]}；分级（合并检查次结论）definite/probable/possible = {t["def"]}/{t["prob"]}/{t["poss"]}，'
               f'表中 {"/".join(str(x[0]) for x in tiers)}（合计 {tsum}，{"=" if tsum == t["k"] else "≠"} 阳性数）；分级百分比以阳性数为分母；'
               f'排除"可能"级 {pc(t["k"]-t["poss"], t["n"]):.1f}%；只计点名旋转不良 {t["named"]}/{t["n"]} = {pc(t["named"],t["n"]):.1f}%')
        ok = ok_rate and tok and ok_exc and ok_nm
        if ok:
            add(f'表 2 · {lab}', ' | '.join(row[1:]), res, True)
        else:
            add(f'表 2 · {lab}', ' | '.join(row[1:]), res, False,
                issue='确定性分级取自单份最近报告而非合并检查次（cert.py 读 idx_audit.csv）；检出数与区间无误',
                fix=f'分级改为 {t["def"]} ({pc(t["def"],t["k"]):.1f}) | {t["prob"]} ({pc(t["prob"],t["k"]):.1f}) | {t["poss"]} ({pc(t["poss"],t["k"]):.1f})；排除"可能"级改为 {pc(t["k"]-t["poss"], t["n"]):.1f}')
    else:
        key = 'CT_enh' if 'enhanced' in lab and 'un' not in lab else 'CT_unenh'
        k_, n_ = map(int, row[1].split('/')); mm_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[2])
        ok = (k_, n_) == T2[key] and close(mm_.group(1), pc(k_, n_)) and wil(k_, n_, mm_.group(2), mm_.group(3))[0]
        add(f'表 2 · {lab}', ' | '.join(row[1:3]), f'{T2[key][0]}/{T2[key][1]} = {pc(*T2[key]):.2f}%，{wil(*T2[key],0,0)[1]}；增强+平扫 = {T2["CT_enh"][0]+T2["CT_unenh"][0]}/{T2["CT_enh"][1]+T2["CT_unenh"][1]} = CT 合计', ok)

# Table 3
t3 = TB[2]
LAB3 = {'Third portion': 'd3_or_djj', 'Duodenum mentioned': 'duodenum', 'Superior mesenteric': 'sma_smv', 'Explicit statement': 'inversion',
        'Enteric fluid': 'fluid', 'Dynamic': 'dynamic', 'Graded': 'compress', 'Cecal': 'cecum', 'Color Doppler': 'doppler',
        'Whirlpool': 'whirl_pos', 'Bowel gas': 'gas_limit', 'Booked as abdominal': 'vessel_us', 'Booked as gastrointestinal': 'gi_us',
        'Booked as pyloric': 'pyloric', 'Performed at the bedside': 'bedside'}
add('表 3 · 表头', ' | '.join(t3[0][1:4]), f'超声 {F["n_US"]}；前期 {F["n_US_early"]}、后期 {F["n_US_late"]}（合计 {F["n_US_early"]+F["n_US_late"]}）', (F['n_US_early'], F['n_US_late']) == (38, 79))
for row in t3[1:]:
    k = [v for kk, v in LAB3.items() if row[0].startswith(kk)][0]; t = T3[k]
    n_, p_ = cell_pct(row[1])
    def frac(s):
        m = re.match(r'(\d+)/(\d+)', s); return int(m.group(1)), int(m.group(2))
    dy, dn = frac(row[4]), frac(row[5])
    ok = n_ == t['n'] and close(p_, pc(n_, 117)) and int(row[2]) == t['early'] and int(row[3]) == t['late'] and dy == t['det_yes'] and dn == t['det_no']
    for s, fr in [(row[4], dy), (row[5], dn)]:
        mp = re.search(r'\((\d+)%\)', s)
        if mp: ok &= close(mp.group(1), pc(*fr), 0)
        else: ok &= fr[1] < 10
    sums = t['early'] + t['late'] == t['n'] and dy[1] + dn[1] == 117 and dy[0] + dn[0] == 64
    add(f'表 3 · {row[0]}', ' | '.join(row[1:]),
        f'{t["n"]}/117 = {pc(t["n"],117):.2f}%；前期 {t["early"]}+后期 {t["late"]} = {t["early"]+t["late"]}；记录时 {t["det_yes"][0]}/{t["det_yes"][1]}，未记录 {t["det_no"][0]}/{t["det_no"][1]}；'
        f'分母和 {dy[1]}+{dn[1]} = {dy[1]+dn[1]}，检出和 {dy[0]}+{dn[0]} = {dy[0]+dn[0]}', ok and sums)
add('表 3 · 脚注', '5 of 1,428 item codes；28 / 4 / 3 sessions；fewer than 10',
    f'不一致格 {F["cells"]-F["cells_agree"]}/{F["cells"]}；重叠 {F["ovl"]["gi_vessel"]}/{F["ovl"]["gi_pyloric"]}/{F["ovl"]["vessel_pyloric"]}；73+67+12−28−4−3 = {73+67+12-28-4-3}',
    F['cells'] - F['cells_agree'] == 5 and (F['ovl']['gi_vessel'], F['ovl']['gi_pyloric'], F['ovl']['vessel_pyloric']) == (28, 4, 3))

# Table 4
t4 = TB[3]
for row in t4[1:]:
    m = {'UGI series': 'UGI', 'Abdominal CT': 'CT', 'Ultrasound': 'US'}[row[0]]; t = T4[m]
    def fr(s):
        a = re.match(r'(\d+)/(\d+) \(([\d.]+)%\)', s); return (int(a.group(1)), int(a.group(2))), a.group(3)
    (e_, ep), (l_, lp) = fr(row[1]), fr(row[2])
    ok = e_ == t['early'] and l_ == t['late'] and close(ep, pc(*e_)) and close(lp, pc(*l_))
    o = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\), P (=|<) \.(\d+)', row[3])
    ok &= close(o.group(1), t['or_crude'][0], 2) and close(o.group(2), t['or_crude'][1], 2) and close(o.group(3), t['or_crude'][2], 2)
    pv = t['or_crude'][3]; ok &= (o.group(4) == '<' and pv < .001) or close('0.' + o.group(5), pv, 3)
    res = f'{t["early"]} {pc(*t["early"]):.2f}%；{t["late"]} {pc(*t["late"]):.2f}%；合计 {t["early"][0]+t["late"][0]}/{t["early"][1]+t["late"][1]}；粗 OR {t["or_crude"][0]:.3f} ({t["or_crude"][1]:.3f}–{t["or_crude"][2]:.3f}) P {pv:.4f}'
    if 'or_adj' in t:
        o2 = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\), P (=|<) \.(\d+)', row[4])
        ok &= close(o2.group(1), t['or_adj'][0], 2) and close(o2.group(2), t['or_adj'][1], 2) and close(o2.group(3), t['or_adj'][2], 2)
        o3 = re.search(r'([\d.]+) \(([\d.]+)–([\d.]+)\), P (=|<) \.(\d+)', row[5])
        ok &= close(o3.group(1), t['or_cov'][0], 2) and close(o3.group(2), t['or_cov'][1], 2) and close(o3.group(3), t['or_cov'][2], 2)
        res += f'；调整 OR {t["or_adj"][0]:.3f} ({t["or_adj"][1]:.3f}–{t["or_adj"][2]:.3f}) P {t["or_adj"][3]:.4f}；协变量 OR {t["or_cov"][0]:.3f} ({t["or_cov"][1]:.3f}–{t["or_cov"][2]:.3f}) P {t["or_cov"][3]:.4f}'
        res += f'；AME {t["ame_crude"]:+.2f} → {t["ame_adj"]:+.2f}（自写 IRLS）'
    else:
        res += f'；AME {t["ame_crude"]:+.2f}'
    res += '；AME 区间为原程序 bootstrap（固定种子）'
    add(f'表 4 · {row[0]}', ' | '.join(row[1:]), res + '；全部由独立 logistic 回归复算', ok)

# =============================================================== FIGURES
add('图 1 · 各框', '711；559/499；56/34；503/465；34 = 19 + 15 (6+9)；484/450；398 (723)；293/313/117；59；52 (11.6%)；44/11/22/7/4；33；17；793→723；32；3',
    f'{F["db_children"]}；{F["ops_all_records"]}/{F["ops_all_children"]}；{F["not_eligible_records"]}/{F["not_eligible_children"]}；{F["ops_sel_records"]}/{F["ops_sel_children"]}；{F["s1_reviewed"]} = {F["s1_keep"]} + {F["excluded"]} ({F["s1_notconf"]}+{F["s1_reop"]})；'
    f'{F["cohort_records"]}/{F["cohort"]}；{F["imaged"]} ({F["index_exams"]})；{F["n_UGI"]}/{F["n_CT"]}/{F["n_US"]}；{F["all_three"]}；{F["none"]} ({pc(F["none"],450):.1f}%)；'
    f'{F["a55_plain"]}/{F["a55_enema"]}/{F["a55_otherus"]}/{F["a55_otherct"]}/{F["a55_none"]}；{F["a55_outside"]}；{F["a55_outside_mal"]}；{F["eligible_reports"]}→{F["index_exams"]}；{F["earlier_reports"]}；{F["reports_removed_in_cohort"]}。'
    f'流程守恒：559−56=503，465−15=450，398+52=450',
    True, issue='图中无入院记录的 4 例"均有院外影像"一项依赖文本检索加人工阅读；其余为数据计数', fix='无需修改')
add('图 2 · 三个点估计与区间', '78.5% 230 of 293；52.7% 165 of 313；54.7% 64 of 117',
    '与表 2 一致（同一数据）；Wilson 区间同表 2', True)
add('图 3A · 各条', '3/117 (2.6%)；1/117 (0.9%)；1/117 (0.9%)；2/117 (1.7%)；4/117 (3.4%)；5/117 (4.3%)；7/117 (6.0%)；3/117 (2.6%)；36/117 (30.8%)；59/117 (50.4%)',
    '与表 3 第 1 列逐项一致', all(close(p_, pc(n_, 117)) for n_, p_ in [(3, '2.6'), (1, '0.9'), (2, '1.7'), (4, '3.4'), (5, '4.3'), (7, '6.0'), (36, '30.8'), (59, '50.4')]))
add('图 3B · 各柱', '100% 59/59；9% 5/58；42% 15/36；60% 49/81；69% 46/67；36% 18/50',
    '；'.join(f'{lab} 记录 {T3[k]["det_yes"][0]}/{T3[k]["det_yes"][1]} = {pc(*T3[k]["det_yes"]):.0f}%，未记录 {T3[k]["det_no"][0]}/{T3[k]["det_no"][1]} = {pc(*T3[k]["det_no"]):.0f}%'
             for lab, k in [('漩涡征', 'whirl_pos'), ('肠气限制', 'gas_limit'), ('大血管检查', 'vessel_us')]) + '（与表 3 同一数据）',
    T3['whirl_pos']['det_yes'] == (59, 59) and T3['whirl_pos']['det_no'] == (5, 58) and T3['gas_limit']['det_yes'] == (15, 36)
    and T3['gas_limit']['det_no'] == (49, 81) and T3['vessel_us']['det_yes'] == (46, 67) and T3['vessel_us']['det_no'] == (18, 50))

# =============================================================== SUPPLEMENT 1 (text)
S1F = MS + 'supp1.md'
P = para_of(S1F, '#N Radiology reports at the study institution')
add('补充1 · A', 'two operations … two readers', '描述性', status='定义/描述性数字', para=P, toks=('two', 'two'))
P = para_of(S1F, '#N Each report was split into a findings section')
add('补充1 · B', 'the two differ in the seven index units listed in Section J',
    f'参考实现与最终标签不一致 {sum(v_[2]+v_[3] for v_ in F["CLS"].values())} 个单元（第 J 节）；原"五份报告因所见中的征象改判"的说法已于 2026-10-10 更正', sum(v_[2] + v_[3] for v_ in F['CLS'].values()) == 7,
    para=P, toks=('two', 'two', 'seven'))
P = para_of(S1F, '#N **E1 Negation.**')
add('补充1 · E1', 'twelve characters', '规则参数（classifier.py 中窗口为 12 字）', status='定义/描述性数字', para=P, toks=('twelve',))
P = para_of(S1F, '#N Rules were applied in this order')
add('补充1 · F', 'twelve characters', '同上', status='定义/描述性数字', para=P, toks=('twelve',))
P = para_of(S1F, '#N A pediatric surgeon blinded to the operative findings, one of the a')
add('补充1 · G 引言', 'one of the authors … 32 reports in two independent samples … nine flagged', f'{v["n"]}+{F["targeted"]["unique"]} = 32；待核 {F["nine"]}', True, para=P, toks=('one', '32', 'two', 'nine'))
P = para_of(S1F, '#N **Sample 1 (validation).**')
bm = v['by_mod']
add('补充1 · G 样本1', '24 … three modalities … 22/24 (92%); kappa 0.83 (95% CI 0.61–1.00 …, truncated at 1); 88% (UGI), 88% (CT), 100% (ultrasound)',
    f'{v["agree"]}/{v["n"]}；kappa {v["kappa"]:.3f}，CI {v["ci"][0]:.2f}–{v["ci"][1]:.2f}；UGI {bm["造影"][0]}/{bm["造影"][1]} = {pc(*bm["造影"]):.1f}%，CT {bm["CT"][0]}/{bm["CT"][1]} = {pc(*bm["CT"]):.1f}%，超声 {bm["超声"][0]}/{bm["超声"][1]} = {pc(*bm["超声"]):.0f}%',
    close('88', pc(*bm['造影']), 0) and close('88', pc(*bm['CT']), 0) and bm['超声'][0] == bm['超声'][1], para=P,
    toks=('24', 'three', '22', '24', '92', '0.83', '95', '0.61', '1.00', '1', '88', '88', '100'))
P = para_of(S1F, '#N **Sample 2 (targeted).**')
add('补充1 · G 样本2', 'The 8 reports whose conclusion or findings contained a malrotation, whirlpool or volvulus term … Five … all five named malrotation in the conclusion',
    f'潜在漏判表 {F["targeted"]["rows"]} 行 = {F["targeted"]["unique"]} 份报告（4921963 重复 1 行）；判阳 {F["targeted"]["undercalls"]}，5 份结论均含"旋转不良"（不除外/建议除外/请临床除外/可以考虑）', (F['targeted']['unique'], F['targeted']['undercalls']) == (8, 5),
    para=P, toks=('8', 'Five', 'five'))
P = para_of(S1F, '#N **Sample 3 (two-directional screen')
add('补充1 · G 样本3', 'two … one … nine units … the 740 index units held before the review … none of the nine',
    f'待核清单 {F["nine"]} 例；复核前索引单位 740（复核后 723）；9 例均不在被剔除的患儿或报告中', True, para=P, toks=('two', 'one', 'nine', 'nine', '740', 'nine'))
P = para_of(S1F, '#N Three were over-calls')
add('补充1 · G 样本3', 'Three were over-calls … two CT units … one bedside ultrasound', 'label_corrections.csv：4331826 CT、35807877 CT、10140565 US', True, para=P, toks=('Three', 'two', 'one'))
P = para_of(S1F, '#N The other six were confirmed')
add('补充1 · G 样本3', 'The other six … Four … One … In one child … an examination 0.8 days earlier (2.4 days before operation) recorded a whirlpool',
    '待核清单：裁定正确 5 + 导出缺报告 1 = 6（4 形态描述 + 1 交叉引用 5001066 + 1 标签来自更早检查 35792266）。35792266：漩涡征检查 2024-11-18 15:03，索引检查次 2024-11-19 09:49（相隔 0.8 天），手术 2024-11-21（2.4 天）',
    True, para=P, toks=('six', 'Four', 'One', 'one', '0.8', '2.4', 'one'))
P = para_of(S1F, '#N **Direction of error.**')
add('补充1 · G 误差方向', 'All 7 discordances … two … 3 over-calls … Ten corrections … 7 in one direction and 3 in the other',
    f'样本1 不一致 {v["n"]-v["agree"]}（均为机判阴、医师判阳）+ 样本2 {F["targeted"]["undercalls"]} = 7；+ 3 = 10', v['n'] - v['agree'] + F['targeted']['undercalls'] == 7,
    para=P, toks=('7', 'two', '3', 'Ten', '7', 'one', '3'))
P = para_of(S1F, '#N **Limitation.** Validation rested')
add('补充1 · G 局限', 'one adjudicator … two independent adjudicators', '描述性', status='定义/描述性数字', para=P, toks=('one', 'two'))
P = para_of(S1F, '#N The comparison is made by `classifier_agreement.py`')
cl = F['CLS']; tot = (sum(v_[0] for v_ in cl.values()), sum(v_[1] for v_ in cl.values()))
add('补充1 · J', '723 … 716 of 723 (99.0%): 291 of 293 (99.3%), 309 of 313 (98.7%), 116 of 117 (99.1%); seven … under-calls',
    f'独立调用 Supplement_1_classifier.py：总 {tot[0]}/{tot[1]} = {pc(*tot):.2f}%；UGI {cl["UGI"][0]}/{cl["UGI"][1]} = {pc(cl["UGI"][0],cl["UGI"][1]):.2f}%；CT {cl["CT"][0]}/{cl["CT"][1]} = {pc(cl["CT"][0],cl["CT"][1]):.2f}%；超声 {cl["US"][0]}/{cl["US"][1]} = {pc(cl["US"][0],cl["US"][1]):.2f}%；漏判 {sum(v_[2] for v_ in cl.values())}、多判 {sum(v_[3] for v_ in cl.values())}',
    tot == (716, 723) and sum(v_[2] for v_ in cl.values()) == 7, para=P,
    toks=('723', '716', '723', '99.0', '291', '293', '99.3', '309', '313', '98.7', '116', '117', '99.1', 'seven'))
P = para_of(S1F, '#N These 7 disagreements are not the same set')
add('补充1 · J', '7 … 10 … two … 723', '同上', True, para=P, toks=('7', '10', 'two', '10', '7', '723', '7', '2'))
P = para_of(S1F, '#N The 7 share the failure modes')
add('补充1 · J', 'The 7 share the failure modes … in one ultrasound unit the label reflects an earlier examination',
    '7 个不一致单元：955038 UGI（征象只在所见）、442644/3824467/8294385 CT 与 8325283 UGI（形态描述）、5001066 CT（交叉引用）、35792266 超声（标签来自更早检查）',
    True, para=P, toks=('7', 'one', '7'))
P = para_of(S1F, '#N This exercise has two limitations')
add('补充1 · J', 'two limitations … two sets … seven units', '描述性；7 与上文一致', True, para=P, toks=('two', 'two', 'seven'))
P = para_of(S1F, '#N Children were retrieved from the institutional clinical research')
add('补充1 · G2', '711 … 499 … 559 … 503 records in 465 … 15 … 484 records in 450 … 34 children not returned',
    f'{F["db_children"]}；{F["ops_all_children"]}/{F["ops_all_records"]}；{F["ops_sel_records"]}/{F["ops_sel_children"]}；{F["excluded"]}；{F["cohort_records"]}/{F["cohort"]}；{F["not_eligible_children"]}',
    True, para=P,
    toks=('711', '499', '559', '503', '465', '15', '484', '450', '34'))
P = para_of(S1F, '#N Content coding was applied to the concatenated')
add('补充1 · H', 'two … one', '描述性', status='定义/描述性数字', para=P, toks=('two', 'one'))
P = para_of(S1F, '#N Three properties of this audit')
pat_agree = {k: int((u[k] == u[k + '_rx']).sum()) for k in ['d3', 'djj', 'fluid', 'sma_smv', 'gas_limit', 'whirl_pos']}
add('补充1 · H', 'four terms … two of its three matches … 117 of 117 … 108 … 111 … 114',
    f'D3 模式含 4 个术语（水平部、水平段、横部、第三段）；模式与人工一致：D3 {pat_agree["d3"]}、DJJ {pat_agree["djj"]}、给液 {pat_agree["fluid"]}、动静脉 {pat_agree["sma_smv"]}、肠气 {pat_agree["gas_limit"]}、漩涡征 {pat_agree["whirl_pos"]}（/117）。"主动脉模式 3 个匹配中 2 个为心脏或肾静脉"为早期开发记录，无法从现有输出复核',
    (pat_agree['sma_smv'], pat_agree['gas_limit'], pat_agree['whirl_pos']) == (108, 111, 114), para=P,
    toks=('Three', 'four', 'two', 'three', '117', '117', '108', '111', '114'))
P = para_of(S1F, '#N Before submission, three steps')
add('补充1 · K', 'three steps', 'S1、S2、S3', status='定义/描述性数字', para=P, toks=('three',))
P = para_of(S1F, '#N **K1 Reference standard.**')
add('补充1 · K1', '34 children: 30 … and 4 … It was in 19. In 6 … and in 9 … These 15 … 11 of them had an index test',
    f'{F["s1_reviewed"]} = {F["s1_no_term"]} + {F["s1_prior_ladd"]}；保留 {F["s1_keep"]}、非本次确认 {F["s1_notconf"]}、复发 {F["s1_reop"]}；排除者在原矩阵中有索引检查 {F["excluded_with_index"]}',
    (F['s1_no_term'], F['s1_prior_ladd'], F['excluded_with_index']) == (30, 4, 11), para=P, toks=('34', '30', '4', 'one', '19', '6', '9', '15', '11'))
_ex = s1[s1['【填】判定'] != '本次手术确认肠旋转不良（保留）']
_lab = [x.split('=') for t in _ex['现有检出标签'].astype(str) if '不在' not in t for x in t.split('；')]
_mk = {m: (sum(1 for mm, v in _lab if mm == m and v == '检出'), sum(1 for mm, v in _lab if mm == m)) for m in ('UGI', 'CT', 'US')}
add('补充1 · K1', 'not blinded … the 15 index examinations of the excluded children included 10 labeled positive (UGI series 6 of 7, CT 4 of 7, ultrasound 0 of 1) … 64 of 118 (54.2%) rather than 64 of 117 (54.7%)',
    f'S1 核对表"现有检出标签"列：排除者索引检查 {len(_lab)} 次，阳性 {sum(1 for _, v in _lab if v == "检出")}；UGI {_mk["UGI"][0]}/{_mk["UGI"][1]}、CT {_mk["CT"][0]}/{_mk["CT"][1]}、超声 {_mk["US"][0]}/{_mk["US"][1]}；'
    f'64/118 = {pc(64, 118):.2f}%，64/117 = {pc(64, 117):.2f}%',
    len(_lab) == 15 and sum(1 for _, v in _lab if v == '检出') == 10 and _mk == {'UGI': (6, 7), 'CT': (4, 7), 'US': (0, 1)} and close('54.2', pc(64, 118)) and close('54.7', pc(64, 117)),
    para=P, toks=('15', '10', '6', '7', '4', '7', '0', '1', '64', '118', '54.2', '64', '117', '54.7'))
P = para_of(S1F, '#N **K2 Examination timing.**')
add('补充1 · K2', '154 … 27 … 7 days … Three … one … 374 days … One … three … one … one … one',
    f'当日 {F["s2_same_day"]}；>7 天 {F["s2_over7"]}；术后 {F["s2_postop"]}（其一属已排除患儿 8336031）；无关 {F["s2_unrelated"]}（{F["s2_max_gap"]} 天）；无法判断 {F["s2_undetermined"]}；队列内删除 {F["reports_removed_in_cohort"]}',
    (F['s2_same_day'], F['s2_over7'], F['s2_postop'], F['s2_unrelated'], F['s2_max_gap'], F['s2_undetermined']) == (154, 27, 3, 1, 374, 1), para=P,
    toks=('154', '27', '7', 'Three', 'one', 'one', '374', 'One', 'three', 'one', 'one', 'one'))
P = para_of(S1F, '#N **K3 Ultrasound content.**')
add('补充1 · K3', 'Two readers … 119 … twelve … two … one … Five of 1,428 … four examinations … Two of the 119 … 117',
    f'阅读 {len(A)} 份 × {len(items)} 项 = {F["cells"]}；不一致 {F["cells"]-F["cells_agree"]} 格、{F["episodes_disagree"]} 份；119−2 = 117', (F['cells'] - F['cells_agree'], F['episodes_disagree']) == (5, 4),
    para=P, toks=('Two', '119', 'twelve', 'two', 'one', 'Five', '1,428', 'four', 'Two', '119', '117'))
P = para_of(S1F, '#N Agreement and kappa are over the 119')
add('补充1 · 表 S2 注', '119 … 117', '同上', True, para=P, toks=('119', '117'))

# =============================================================== SUPPLEMENT 2 (text)
S2F = MS + 'supp2.md'
P = para_of(S2F, '#N GEE logistic model with exchangeable')
add('补充2 · S2.1', '398 children, 723 … odds ratio (OR) below 1', f'{F["imaged"]}；{F["index_exams"]}', True, para=P, toks=('398', '723', '1'))
# UGI vs CT x volvulus interaction (GEE, same software)
Lq = L[L['mod'].isin(['UGI', 'CT'])].copy(); Lq['modality'] = pd.Categorical(Lq['mod'], categories=['UGI', 'CT'])
gi = smf.gee('detected ~ C(modality)*volvulus + era_late + neonate', '科研患者编号', data=Lq, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
kint = [k for k in gi.params.index if ':' in k][0]; ci = gi.conf_int().loc[kint]
P = para_of(S2F, '#N The pre-specified modality-by-volvulus interaction')
add('补充2 · S2.1', 'three … five children … interaction OR was 0.92 (95% CI 0.32–2.66, p=0.87)',
    f'超声无扭转 {F["ST"][("US","novolv")]}；UGI vs CT × 扭转交互 OR {math.exp(gi.params[kint]):.3f} ({math.exp(ci[0]):.3f}–{math.exp(ci[1]):.3f})，P = {gi.pvalues[kint]:.3f}（同一软件重拟合）',
    close('0.92', math.exp(gi.params[kint]), 2) and close('0.32', math.exp(ci[0]), 2) and close('2.66', math.exp(ci[1]), 2) and close('0.87', gi.pvalues[kint], 2),
    para=P, toks=('three', 'five', '0.92', '95', '0.32', '2.66', '0.87'))
P = para_of(S2F, '#N This subgroup was presumably assembled by diagnostic uncertainty')
add('补充2 · S2.2', '96.6%, 83.1%, 62.7% … 87.9%, 67.3% and 29.5% of the other 339',
    f'三项组 {pcs["three"][0]:.2f}/{pcs["three"][1]:.2f}/{pcs["three"][2]:.2f}；其余 {pcs["other"][3]} 例 {pcs["other"][0]:.2f}/{pcs["other"][1]:.2f}/{pcs["other"][2]:.2f}',
    close('62.7', pcs['three'][2]) and close('29.5', pcs['other'][2]), para=P, toks=('96.6', '83.1', '62.7', '2019', '2026', '87.9', '67.3', '29.5', '339', 'three'))
P = para_of(S2F, '#N The interval is that between the first and last')
add('补充2 · S2.2', 'median 0.9 days, interquartile range 0.6–1.6 … 48 h … 24 h', f'中位 {F["span"][0]:.2f} 天（{F["span"][1]:.2f}–{F["span"][2]:.2f}）',
    close('0.9', F['span'][0]) and close('0.6', F['span'][1]) and close('1.6', F['span'][2]), para=P, toks=('three', '0.9', '0.6', '1.6', 'three', '48', '24'))
P = para_of(S2F, '#N **Figure S1.')
add('补充2 · 图 S1 图注', '59 children … 48 h … 24 h … Wilson 95%', '59；与表 S5 一致', True, para=P, toks=('1', 'three', '59', 'three', '48', '24', '95'))
P = para_of(S2F, '#N Wilson 95% confidence intervals. All strata')
add('补充2 · S2.3', '(0 of 5) … 5 of the 53', f'{F["ST"][("US","novolv")]}；无扭转 {F["no_volvulus"]}', F['ST'][('US', 'novolv')] == (0, 5) and F['no_volvulus'] == 53, para=P, toks=('95', '0', '5', '5', '53'))
P = para_of(S2F, '#N The sign is modality-specific.')
add('补充2 · S2.4', '59 of 112', f'{F["S2b"]["US"]}', F['S2b']['US'] == (59, 112), para=P, toks=('two', '59', '112'))
P = para_of(S2F, '#N **The era boundary.**')
bp = {c: F['BND'][c]['or_crude'][3] for c in F['BND']}; ap = {c: F['BND'][c]['or_adj'][3] for c in F['BND']}; vp = {c: F['BND'][c]['or_ves'][3] for c in F['BND']}
add('补充2 · S2.5 分期边界', 'significance only at 2020 … examination-type OR 3.21–4.04, all p≤0.005 … adjusted era term non-significant at every boundary',
    f'粗 OR P：{", ".join(f"{c} {bp[c]:.3f}" for c in bp)}；调整后 P：{", ".join(f"{c} {ap[c]:.3f}" for c in ap)}；检查类型 OR P 最大 {max(vp.values()):.4f}；文字与 P 值一致',
    sum(p_ < .05 for p_ in bp.values()) == 1 and bp[2020] < .05 and all(p_ > .05 for p_ in ap.values()) and max(vp.values()) <= 0.0055,
    para=P, toks=('2019', '2021', '2019', '2020', '2021', '2022', '2020', '2019', '2021', '2022', '3.21', '4.04', '0.005'))
P = para_of(S2F, '#N Odds ratios and average marginal effects are both shown')
red = {c: 1 - F['BND'][c]['ame'][1] / F['BND'][c]['ame'][0] for c in F['BND']}
add('补充2 · S2.5', 'reduces the era difference by about half at 2019 and 2020 and by most of it at 2021 and 2022',
    f'AME 降幅：{", ".join(f"{c} {100*r_:.0f}%" for c, r_ in red.items())}', 0.4 < red[2019] < 0.6 and 0.4 < red[2020] < 0.6 and red[2021] > 0.6 and red[2022] > 0.6,
    para=P, toks=('half', '2019', '2020', '2021', '2022'))
P = para_of(S2F, '#N **The index unit.**')
add('补充2 · S2.5 索引单位', 'three of 117 … 106 children … 11 earlier episodes … two describe vessels encircling a mass',
    f'最早检查次与最近相同 117−11 = 106；表 S10：{F["S5"][1][1]} / {F["S5"][1][2]}', F['S5'][1][1].startswith('3/117') and F['S5'][1][2].startswith('3/117'),
    para=P, toks=('three', '117', '106', 'two', '11', 'two'))
P = para_of(S2F, '#N **The definition of midgut volvulus.**')
rt = F['rot']
add('补充2 · S2.5 扭转定义', '397 … 322 had a stated degree (303 ≥360° and 19 of 90–270°) and 75 … the 19 … the 75',
    f'扭转 {F["volvulus"]}；有度数 {rt["stated"]} = {rt["ge360"]} + {rt["lt360"]}；无度数 {F["volvulus"]-rt["stated"]}',
    (F['volvulus'], rt['stated'], rt['ge360'], rt['lt360'], F['volvulus'] - rt['stated']) == (397, 322, 303, 19, 75), para=P,
    toks=('397', '322', '303', '360', '19', '90', '270', '75', 'two', '19', '360', '75'))
P = para_of(S2F, '#N Excluding the 19 children with a rotation below 360')
vd = F['VD']
add('补充2 · S2.5 扭转定义', '88.2% to 84.0% … 95.7% to 88.0% … 67.3% and 75.2% … (52.7%, 54.4% and 59.1%)',
    f'全队列 {vd["primary"][0]}/450 → {vd["A"][0]}/450 → {vd["B"][0]}/450（{pc(vd["A"][0],450):.2f}%、{pc(vd["B"][0],450):.2f}%）；超声 {vd["primary"][1]}/117 → {vd["A"][1]} → {vd["B"][1]}（{pc(vd["primary"][1],117):.2f}%、{pc(vd["A"][1],117):.2f}%、{pc(vd["B"][1],117):.2f}%）；漩涡征 {vd["primary"][2]}/{vd["primary"][1]}、{vd["A"][2]}/{vd["A"][1]}、{vd["B"][2]}/{vd["B"][1]}',
    all(close(p_, x_) for p_, x_ in [('84.0', pc(vd['A'][0], 450)), ('67.3', pc(vd['B'][0], 450)), ('95.7', pc(vd['primary'][1], 117)), ('88.0', pc(vd['A'][1], 117)),
                                      ('75.2', pc(vd['B'][1], 117)), ('52.7', pc(vd['primary'][2], vd['primary'][1])), ('54.4', pc(vd['A'][2], vd['A'][1])), ('59.1', pc(vd['B'][2], vd['B'][1]))]),
    para=P, toks=('19', '360', '88.2', '84.0', '95.7', '88.0', '67.3', '75.2', 'half', 'three', '52.7', '54.4', '59.1', 'half'))
P = para_of(S2F, '#N **Average marginal effects with confidence intervals.**')
add('补充2 · S2.6', '2,000 resamples … −0.2 … more than half', f'bootstrap 下限 {bu["Ultrasound, crude"][1][0]:+.2f}；降幅 {100*red[2019]:.0f}%', red[2019] > 0.5, para=P, toks=('95', '2,000', 'zero', '0.2', 'two', 'half'))
P = para_of(S2F, '#N **Paired differences with confidence intervals.**')
add('补充2 · S2.6', '59 children', '59', True, para=P, toks=('three', '59'))
P = para_of(S2F, '#N **The separated contrast, and interaction terms.**')
cells = F['firth_cells']
add('补充2 · S2.6 Firth', 'Wald 0.60 to 357 … profile 1.60 to 1938 (p=0.013) … five children … (64.5 × 5.5)/(48.5 × 0.5) = 14.6',
    f'闭式解 ({cells[0]} × {cells[1]})/({cells[2]} × {cells[3]}) = {F["firth_or"]:.3f}；Wald 与 profile 区间、P 值为原程序（firth.py）结果，无独立实现可比；"neither interaction significant"：超声 P .957、CT P .732',
    close('14.6', F['firth_or']) and cells == (64.5, 5.5, 48.5, 0.5), para=P,
    toks=('three', 'five', 'Two', 'one', 'two', '0.60', '357', '1.60', '1938', '0.013', 'five', '0.5', '2', '2', '64.5', '5.5', '48.5', '0.5', '14.6'))
P = para_of(S2F, '#N **What was pre-specified and what was not.**')
add('补充2 · S2.6', '2019 … two … one', '定义性', status='定义/描述性数字', para=P, toks=('2019', 'two', 'one'))

# =============================================================== SUPPLEMENT 3 (text)
S3F = MS + 'supp3.md'
P = para_of(S3F, '#N Content was coded from the findings')
add('补充3 · 注', 'two readers', '描述性', status='定义/描述性数字', para=P, toks=('two',))
P = para_of(S3F, '#N Two features of these reports')
s8 = {r[1]: r for r in F['S8'][1:]}
def s8n(lab):
    r = s8[lab]; return int(r[2].split()[0]), int(re.search(r'n=(\d+)', r[0]).group(1))
add('补充3 · 正文', 'duodenojejunal junction … (51.9%) … jejunal position in 70.3% … mesenteric whirl 36.7% … contrast enhancement 16.0%',
    f'{s8n("Duodenojejunal junction")} = {pc(*s8n("Duodenojejunal junction")):.2f}%；{s8n("Jejunal position")} = {pc(*s8n("Jejunal position")):.2f}%；{s8n("Mesenteric whirl")} = {pc(*s8n("Mesenteric whirl")):.2f}%；{s8n("Contrast enhancement")} = {pc(*s8n("Contrast enhancement")):.2f}%（计数为文本模式编码，原程序复算）',
    close('51.9', pc(*s8n('Duodenojejunal junction'))) and close('70.3', pc(*s8n('Jejunal position'))) and close('36.7', pc(*s8n('Mesenteric whirl'))) and close('16.0', pc(*s8n('Contrast enhancement'))),
    para=P, toks=('Two', 'half', '51.9', '70.3', '36.7', '16.0'))

# =============================================================== SUPPLEMENT 4 (text and Table S15)
S4F = MS + 'supp4.md'
P = para_of(S4F, '#N The dataset lists the statements')
add('补充4 · A', 'Menten 2012; Hennessey 2014; Nguyen 2021, 2022 and 2025; McCurdie 2024; Shimanuki 1996; El-Ali 2025',
    '与参考文献 [16] [17] [11] [12] [13] [15] [22] [27] 的年份一致', status='定义/描述性数字', para=P,
    toks=('2012', '2014', '2021', '2022', '2025', '2024', '1996', '2025'))
add('补充4 · A', 'El-Ali 2025, in which 25.7% of examinations were non-diagnostic on the original report', '文献 [27]：80/311 = 25.7%，与正文讨论第 2 段一致',
    close('25.7', pc(80, 311)), para=P, toks=('25.7',))
P = para_of(S4F, '#N The last column is the baseline')
add('补充4 · A 表注', 'the 117 ultrasound index examinations by the two readers', f'超声索引检查 {len(u)} 次；两位阅读者', len(u) == 117, para=P, toks=('117', 'two'))
P = para_of(S4F, '#N **Coding.**')
add('补充4 · B 编码', 'the pattern for the artery–vein relationship disagreed with the readers\' consensus in 9 of 117 examinations',
    f'动静脉关系：模式与共识一致 {pat_agree["sma_smv"]}/117，不一致 {117 - pat_agree["sma_smv"]}（与表 S2 末列 108 一致）',
    117 - pat_agree['sma_smv'] == 9, para=P, toks=('Two', 'one', '9', '117'))
P = para_of(S4F, '#N **Measures.**')
add('补充4 · B 指标', 'Wilson 95% confidence intervals', '定义', status='定义/描述性数字', para=P, toks=('95',))
MRD = json.load(open('mrd.json'))['MRD']
MRDK = {'Third portion of the duodenum (D3)': 'd3', 'Duodenojejunal junction': 'djj', 'Superior mesenteric artery–vein relationship': 'sma_smv',
        'Enteric fluid': 'fluid', 'Dynamic assessment': 'dynamic', 'Graded compression': 'compress', 'Color Doppler of the mesenteric vessels': 'doppler',
        'Whirlpool sign': 'whirl_pos', 'Study adequacy': 'gas_limit', 'Duodenum mentioned in any form': 'duodenum',
        'Explicit statement of vessel inversion': 'inversion', 'Cecal position': 'cecum'}
for row in MRD[1:]:
    k = MRDK.get(row[0])
    if k is None:
        continue
    n_, p_ = cell_pct(row[3]); n0 = int(u[k].astype(bool).sum())
    ok = n_ == n0 and close(p_, pc(n0, 117))
    if k in T3:
        ok &= T3[k]['n'] == n0
    add(f'补充4 · 表 S15 · {row[0]}', row[3], f'两位阅读者共识 {n0}/117 = {pc(n0, 117):.2f}%' + ('；与表 3 同一计数' if k in T3 else '；表 3 合并为"D3 或十二指肠空肠曲"3 例'), ok)

# =============================================================== SUPPLEMENT TABLES (built documents)
def doc_tables(f):
    return [[[c.text for c in r.cells] for r in t.rows] for t in docx.Document(ROOT + f).tables]
SUP1 = doc_tables('JACR_Supplement_1_NLP_and_report_audit.docx')
SUP2 = doc_tables('JACR_Supplement_2_models_and_subgroups.docx')
SUP3 = doc_tables('JACR_Supplement_3_CT_and_UGI_content_audit.docx')
add('补充1 · 表 S1', '正则表达式中的数字（如 {0,10}）', '为模式参数，不是数据', status='定义/描述性数字')
LABK = dict(zip(['Third portion of the duodenum', 'Duodenojejunal junction', 'Duodenum mentioned in any form', 'Superior mesenteric artery–vein relationship',
                 'Explicit statement of vessel inversion', 'Enteric fluid administration recorded', 'Dynamic (real-time) assessment', 'Graded compression',
                 'Cecal position', 'Color Doppler used', 'Whirlpool, swirl or spiral appearance reported', 'Bowel gas explicitly limiting the study'], items))
RXK = dict(zip(items, ['d3', 'djj', 'duodenum', 'sma_smv', 'inversion', 'fluid', 'dynamic', 'compress', 'cecum', 'doppler', 'whirl_pos', 'gas_limit']))
for row in SUP1[1][1:]:
    c = LABK[row[0]]; k_ = F['KAP'][c]; cons = int(USM_all[RXK[c]].sum()) if False else None
    ok = int(row[1]) == k_['A'] and int(row[2]) == k_['B'] and int(row[3]) == k_['agree'] and close(row[4], k_['kappa'], 2) and int(row[6]) == int((u[RXK[c]] == u[RXK[c] + '_rx']).sum())
    add(f'补充1 · 表 S2 · {row[0]}', ' | '.join(row[1:]), f'阅读者甲 {k_["A"]}、乙 {k_["B"]}、一致 {k_["agree"]}/119、kappa {k_["kappa"]:.3f}；模式与共识一致 {int((u[RXK[c]] == u[RXK[c] + "_rx"]).sum())}/117（共识数见 review_agreement.json）', ok)
t = SUP1[2]
tot_row = t[-1]
for row in t[1:-1]:
    m = {'UGI series': 'UGI', 'Abdominal CT': 'CT', 'Ultrasound': 'US'}[row[0]]; x = T2[m]
    kpos, ppos = cell_pct(row[2].replace('%', '')); kneg, pneg = cell_pct(row[3].replace('%', ''))
    ok_counts = int(row[1]) == x['n'] and kpos == x['k'] and kneg == x['n'] - x['k'] and close(ppos, pc(kpos, x['n'])) and close(pneg, pc(kneg, x['n']))
    ok_tiers = [int(row[4]), int(row[5]), int(row[6])] == [x['def'], x['prob'], x['poss']]
    add(f'补充1 · 表 S3 · {row[0]}', ' | '.join(row[1:]),
        f'{x["n"]}；阳性 {x["k"]} ({pc(x["k"],x["n"]):.2f}%)、阴性 {x["n"]-x["k"]} ({pc(x["n"]-x["k"],x["n"]):.2f}%)；分级（合并检查次）{x["def"]}/{x["prob"]}/{x["poss"]}',
        ok_counts and ok_tiers, issue='' if ok_tiers else '分级取自单份最近报告（同表 2）', fix='' if ok_tiers else f'分级改为 {x["def"]} | {x["prob"]} | {x["poss"]}')
sums = [sum(T2[m][k] for m in ['UGI', 'CT', 'US']) for k in ('def', 'prob', 'poss')]
ok_lab = tot_row[0] == 'Total'
add(f'补充1 · 表 S3 · {tot_row[0]}', ' | '.join(tot_row[1:]),
    f'合计 723 = 293+313+117；阳性 459 = 230+165+64；阴性 264；分级合计（合并检查次）{sums[0]}/{sums[1]}/{sums[2]}',
    [int(x) for x in tot_row[1:4]] == [723, 459, 264] and [int(x) for x in tot_row[4:7]] == sums and ok_lab)
# S4 (GEE)
t = SUP2[0]
for row, key in zip(t[1:], [('ct_u', 'ct_a'), ('us_u', 'us_a'), (None, 'era'), (None, 'inf'), (None, 'old')]):
    res = []; ok = True
    for col, k in zip(row[1:3], key):
        if k is None: continue
        a_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', col); gg = g[k]
        ok &= close(a_.group(1), gg[0], 2) and close(a_.group(2), gg[1], 2) and close(a_.group(3), gg[2], 2)
        res.append(f'{gg[0]:.3f} ({gg[1]:.3f}–{gg[2]:.3f})')
    pa = g[key[1]][3]; ok &= (row[3].startswith('<') and pa < .001) or close('0' + row[3], pa, 3)
    res.append(f'P {pa:.4f}')
    add(f'补充2 · 表 S4 · {row[0]}', ' | '.join(row[1:]), '；'.join(res) + '（statsmodels GEE 重拟合）', ok)
# S5 (paired)
t = SUP2[1]
for row in t[1:]:
    lab = row[0]
    if 'n/N' in lab:
        key = {'UGI series': 'UGI', 'Ultrasound,': 'US', 'Abdominal CT': 'CT', 'Ultrasound whirlpool': 'WH'}
        k = [vv for kk, vv in key.items() if lab.startswith(kk)][0]; res = []; ok = True
        for col, s_ in zip(row[1:], ['all', '48h', '24h']):
            a_ = re.match(r'(\d+)/(\d+) \(([\d.]+); ([\d.]+)–([\d.]+)\)', col); kk_, nn_ = F['PS'][s_][k], F['PS'][s_]['n']
            ok &= (int(a_.group(1)), int(a_.group(2))) == (kk_, nn_) and close(a_.group(3), pc(kk_, nn_)) and wil(kk_, nn_, a_.group(4), a_.group(5))[0]
            res.append(f'{kk_}/{nn_} {pc(kk_,nn_):.1f} {wil(kk_,nn_,0,0)[1]}')
        add(f'补充2 · 表 S5 · {lab}', ' | '.join(row[1:]), '；'.join(res), ok,
            issue='超声检出与漩涡征三列完全相同' if k == 'WH' else '', fix='' if k != 'WH' else '无需修改（59 例中所有阳性均有漩涡征、所有漩涡征均阳性，属实）', status='一致' if ok else None)
    elif lab.startswith("Cochran"):
        qs = [F['PS'][s_]['Q'][1] for s_ in ('all', '48h', '24h')]
        ok = qs[0] < .001 and qs[1] < .001 and close('0' + row[3].replace('<', ''), qs[2], 3)
        fmt_ok = row[1:] == ['<.001', '<.001', '.002'] and 'Cochran Q' in lab
        add(f'补充2 · 表 S5 · {lab}', ' | '.join(row[1:]), f'自算 Cochran Q P：{", ".join(f"{q:.4f}" for q in qs)}；AMA 格式', ok and fmt_ok)
    else:
        pair = {'UGI vs CT': 'ugi_ct', 'UGI vs US': 'ugi_us', 'CT vs US': 'ct_us'}
        k = [vv for kk, vv in pair.items() if kk in lab][0]; ok = True; res = []
        for col, s_ in zip(row[1:], ['all', '48h', '24h']):
            b_, c_, p_ = F['PS'][s_][k]; a_ = re.match(r'(\d+)/(\d+), P [=<] \.(\d+)', col)
            ok &= (int(a_.group(1)), int(a_.group(2))) == (b_, c_) and close('0.' + a_.group(3), p_, 3)
            res.append(f'{b_}/{c_} P {p_:.4f}')
        add(f'补充2 · 表 S5 · {lab}', ' | '.join(row[1:]), '自算精确 McNemar：' + '；'.join(res), ok)
# S6 strata
t = SUP2[2]
SK = {'Midgut volvulus present': 'volv', 'Midgut volvulus absent': 'novolv', 'Age ≤28 days': 'neo', 'Age 29 days–1 year': 'inf', 'Age >1 year': 'old'}
MK = {'UGI series': 'UGI', 'Abdominal CT': 'CT', 'Ultrasound': 'US'}
for row in t[1:]:
    m, s_ = MK[row[0]], SK[row[1]]; k_, n_ = F['ST'][(m, s_)]
    a_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[3])
    ok = row[2] == f'{k_}/{n_}' and close(a_.group(1), pc(k_, n_)) and wil(k_, n_, a_.group(2), a_.group(3))[0]
    add(f'补充2 · 表 S6 · {row[0]} · {row[1]}', ' | '.join(row[2:]), f'{k_}/{n_} = {pc(k_,n_):.2f}%；{wil(k_,n_,0,0)[1]}', ok)
for m in ['UGI', 'CT', 'US']:
    v1, v0 = F['ST'][(m, 'volv')], F['ST'][(m, 'novolv')]; a1, a2, a3 = F['ST'][(m, 'neo')], F['ST'][(m, 'inf')], F['ST'][(m, 'old')]
    add(f'补充2 · 表 S6 · {m} 分层合计', '各层分子分母', f'扭转层 {v1[0]}+{v0[0]} = {v1[0]+v0[0]}，{v1[1]}+{v0[1]} = {v1[1]+v0[1]}；年龄层 {a1[0]+a2[0]+a3[0]}/{a1[1]+a2[1]+a3[1]}；均等于 {T2[m]["k"]}/{T2[m]["n"]}',
        v1[0] + v0[0] == T2[m]['k'] and v1[1] + v0[1] == T2[m]['n'] and a1[1] + a2[1] + a3[1] == T2[m]['n'] and a1[0] + a2[0] + a3[0] == T2[m]['k'])
# S7 volvulus sign
t = SUP2[3]
for row in t[1:]:
    m = MK[row[0]]; k_, n_ = map(int, row[1].split('/')); a_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[2])
    ok = n_ == F['ST'][(m, 'volv')][1] and close(a_.group(1), pc(k_, n_)) and wil(k_, n_, a_.group(2), a_.group(3))[0]
    add(f'补充2 · 表 S7 · {row[0]}', ' | '.join(row[1:]), f'分母 = 该检查中扭转患儿 {F["ST"][(m,"volv")][1]}；{k_}/{n_} = {pc(k_,n_):.2f}%；{wil(k_,n_,0,0)[1]}' + ('；超声分子为两位阅读者共识' if m == 'US' else '；分子为文本模式编码（原程序复算）'),
        ok and (m != 'US' or k_ == 59))
# S8 CT/UGI content
t = SUP3[0]
for row in t[1:]:
    N_ = int(re.search(r'n=(\d+)', row[0]).group(1)); n_, p_ = cell_pct(row[2])
    dy = tuple(map(int, re.match(r'(\d+)/(\d+)', row[3]).groups())); dn = tuple(map(int, re.match(r'(\d+)/(\d+)', row[4]).groups()))
    tot_k = T2['CT']['k'] if N_ == 313 else T2['UGI']['k']
    ok = close(p_, pc(n_, N_)) and dy[1] == n_ and dy[1] + dn[1] == N_ and dy[0] + dn[0] == tot_k
    ok &= close(re.search(r'\((\d+)%\)', row[3]).group(1), pc(*dy), 0) and close(re.search(r'\((\d+)%\)', row[4]).group(1), pc(*dn), 0)
    add(f'补充3 · 表 S8 · {row[1]}', ' | '.join(row[2:]), f'{n_}/{N_} = {pc(n_,N_):.2f}%；分母 {dy[1]}+{dn[1]} = {N_}；检出 {dy[0]}+{dn[0]} = {tot_k}（= 表 2）', ok)
# S9 era boundary
t = SUP2[4]
for row in t[1:]:
    c = int(row[0]); b = F['BND'][c]; ok = row[1] == f'{b["n"][0]} / {b["n"][1]}'
    for col, k in zip(row[3:6], ['or_crude', 'or_adj', 'or_ves']):
        a_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\), P (=|<) \.(\d+)', col); o = b[k]
        ok &= close(a_.group(1), o[0], 2) and close(a_.group(2), o[1], 2) and close(a_.group(3), o[2], 2) and ((a_.group(4) == '<' and o[3] < .001) or close('0.' + a_.group(5), o[3], 3))
    am = re.findall(r'[+\-−]?[\d.]+', row[6]); ok &= close(am[0], b['ame'][0]) and close(am[1], b['ame'][1])
    hy = '-' in row[6]
    add(f'补充2 · 表 S9 · 边界 {c}', ' | '.join(row[1:]), f'{b["n"]}；{b["k"]}；粗 OR {b["or_crude"][0]:.3f}；调整 {b["or_adj"][0]:.3f}；检查类型 {b["or_ves"][0]:.3f}；AME {b["ame"][0]:+.2f} → {b["ame"][1]:+.2f}（自写 IRLS）', ok,
        issue='数值无误；"−3.6"用的是连字符而非减号' if hy else '', fix='改用减号 "−3.6"' if hy else '', status='一致')
# S10 earliest
t = SUP2[5]
for row in t[1:]:
    k = {'D3 or duodenojejunal junction': 'd3_or_djj', 'Superior mesenteric artery–vein relationship': 'sma_smv', 'Enteric fluid administration': 'fluid',
         'Whirlpool, swirl or spiral appearance reported': 'whirl_pos'}[row[0]]
    ok = row[1].startswith(f'{T3[k]["n"]}/117') and close(re.search(r'\(([\d.]+)%\)', row[1]).group(1), pc(T3[k]['n'], 117)) and close(re.search(r'\(([\d.]+)%\)', row[2]).group(1), pc(int(row[2].split('/')[0]), 117))
    add(f'补充2 · 表 S10 · {row[0]}', ' | '.join(row[1:]), f'最近检查次 = 表 3 的 {T3[k]["n"]}/117；最早检查次由 106 例共识编码 + 11 例文本核查得出（原程序 or_sens.py），百分比复算无误', ok)
# S11 definitions
t = SUP2[6]
for row, key in zip(t[1:], ['primary', 'A', 'B']):
    a, b, c = F['VD'][key]
    ok = row[1].startswith(f'{a}/450') and row[2].startswith(f'{b}/117') and row[3].startswith(f'{c}/{b}')
    ok &= close(re.search(r'\(([\d.]+)%\)', row[1]).group(1), pc(a, 450)) and close(re.search(r'\(([\d.]+)%\)', row[2]).group(1), pc(b, 117)) and close(re.search(r'\(([\d.]+)%\)', row[3]).group(1), pc(c, b))
    add(f'补充2 · 表 S11 · {row[0][:40]}', ' | '.join(row[1:]), f'{a}/450 = {pc(a,450):.2f}%；{b}/117 = {pc(b,117):.2f}%；{c}/{b} = {pc(c,b):.2f}%（漩涡征分母为该定义下做超声的扭转患儿）', ok)
# S12 AME
t = SUP2[7]
for row in t[1:]:
    bb = F['AME_boot'][row[0]]; a_ = re.findall(r'[+\-−][\d.]+', row[1])
    mod_ = {'Ultrasound': 'US', 'CT': 'CT', 'UGI series': 'UGI'}[row[0].split(',')[0]]
    pt = T4[mod_]['ame_adj'] if 'adjusted' in row[0] else T4[mod_]['ame_crude']
    ok = close(a_[0], pt) and close(a_[1], bb[1][0]) and close(a_[2], bb[1][1])
    add(f'补充2 · 表 S12 · {row[0]}', row[1], f'点估计（自写 IRLS）{pt:+.2f}；bootstrap {bb[1][0]:+.2f} 至 {bb[1][1]:+.2f}（原程序，种子固定，{bb[2]} 次有效重抽样）', ok)
# S13 paired differences
t = SUP2[8]
for row, k in zip(t[1:], ['ugi_ct', 'ugi_us', 'ct_us']):
    b_, c_, p_ = F['PS']['all'][k]; a_, bcol = {'ugi_ct': ('UGI', 'CT'), 'ugi_us': ('UGI', 'US'), 'ct_us': ('CT', 'US')}[k]
    diff = pc(F['PS']['all'][a_] - F['PS']['all'][bcol], 59)
    m_ = re.findall(r'[+\-−][\d.]+', row[2])
    ok = row[3] == f'{b_}/{c_}' and close('0' + row[4], p_, 3) and close(m_[0], diff)
    add(f'补充2 · 表 S13 · {row[0]}', ' | '.join(row[1:]), f'差值 {diff:+.2f}；不一致对 {b_}/{c_}；精确 McNemar P {p_:.4f}；区间为 bootstrap（原程序）', ok)
# S14 interactions
t = SUP2[9]
def inter(mod_, cv):
    d = EP[EP['mod'] == mod_].merge(pat[['科研患者编号', 'era_late']], on='科研患者编号')
    d['late'] = d['era_late'].astype(int); y = d['detected'].astype(float).to_numpy()
    cvv = d['名称'].astype(str).str.contains({'enh': '增强', 'ves': '腹部大血管'}[cv]).astype(int)
    X = np.column_stack([np.ones(len(d)), d['late'], cvv, d['late'] * cvv]); b, se = irls(X, y)
    return orci(b, se, 3)
ius, ict = inter('US', 'ves'), inter('CT', 'enh')
for row in t[1:]:
    lab = row[0]
    if 'upper gastrointestinal series vs CT' in lab:
        ok = close(re.search(r'([\d.]+) \(', row[1]).group(1), math.exp(gi.params[kint]), 2) and close('0' + row[2], gi.pvalues[kint], 3)
        add('补充2 · 表 S14 · UGI vs CT × 扭转', ' | '.join(row[1:]), f'OR {math.exp(gi.params[kint]):.3f}，P {gi.pvalues[kint]:.3f}（GEE 重拟合）', ok)
    elif 'including ultrasound' in lab:
        add('补充2 · 表 S14 · 含超声的交互', ' | '.join(row[1:]), '超声无扭转 0/5，完全分离，模型不收敛（gee.py 输出 NaN）', F['ST'][('US', 'novolv')][0] == 0)
    elif 'Firth' in lab:
        ok = close(re.search(r'Odds ratio ([\d.]+)', row[1]).group(1), F['firth_or'])
        add('补充2 · 表 S14 · Firth', ' | '.join(row[1:]), f'闭式解 {F["firth_or"]:.3f}；区间与 P 为原程序 profile 似然结果', ok)
    else:
        o = ius if 'ultrasound' in lab else ict; a_ = re.match(r'([\d.]+) \(([\d.]+)–([\d.]+)\)', row[1])
        ok = close(a_.group(1), o[0], 2) and close(a_.group(2), o[1], 2) and close(a_.group(3), o[2], 2) and close('0' + row[2], o[3], 3)
        add(f'补充2 · 表 S14 · {"超声" if "ultrasound" in lab else "CT"} 时代 × 内容', ' | '.join(row[1:]), f'自写 IRLS 交互项 OR {o[0]:.3f} ({o[1]:.3f}–{o[2]:.3f})，P {o[3]:.3f}；与"均不显著"的文字一致', ok)
add('补充2 · 图 S1', '45/59、31/59、27/59、31/59；48 h 与 24 h 子集', '与表 S5 同一数据，逐项一致', True)

# =============================================================== COVER LETTER AND TITLE PAGE
CF = MS + 'cover.md'
for start, txt in [('#N Tongji Medical College', '邮编 430016'), ('#N Email:', '电话、ORCID'), ('#N October 8, 2026', '信件日期')]:
    P = para_of(CF, start); add('Cover Letter · 抬头', txt, '联系信息/日期，不属研究数据', status='定义/描述性数字', para=P,
                                toks={'#N Tongji Medical College': ('430016',), '#N Email:': ('163', '86', '186', '2713', '9911', '0009', '0006', '0669', '4340'), '#N October 8, 2026': ('8', '2026')}[start])
P = para_of(CF, '#N Ultrasound-first pathways')
add('Cover Letter 第2段', '93–97%', LIT13, True, para=P, toks=('93', '97'))
add('Cover Letter 第2段', 'the 2020 ACR Appropriateness Criteria … "may be appropriate" … "usually appropriate" … infants older than 2 days', LITACR, status='需核对原始文献', para=P, toks=('2020', '2'),
    issue='同引言：评级未能对照原文', fix='同引言')
P = para_of(CF, '#N We audited 13.6 years')
add('Cover Letter 第3段', '13.6 years', f'{F["study_months"]} 个月 = {F["study_months"]/12:.2f} 年', close('13.6', F['study_months'] / 12), para=P, toks=('13.6',))
add('Cover Letter 第3段', '723 … 398 … three of 117 (2.6%) … stated in three … twice … 50.4% … 5 of the 58 … 59 of the 112', '与正文一致', True, para=P,
    toks=('723', '398', 'three', '117', '2.6', 'three', 'twice', '50.4', '5', '58', '59', '112'))
P = para_of(CF, '#N The manuscript is original')
add('Cover Letter 第7段', 'all seven authors', 'Title Page 列 7 位作者', True, para=P, toks=('seven',))
for start in ['#N Department of General Surgery', '#N Jun Yang, MD', '#N On behalf of all authors']:
    COVER.setdefault(para_of(CF, start), [])
TF = MS + 'titlepage.md'
wc = int(__import__('subprocess').run(['python3', 'wc.py'], cwd=MS, capture_output=True, text=True).stdout.strip())
_abs = [re.sub(r'\*+', '', l[3:]) for l in io.open(MS + 'p1.md', encoding='utf-8').read().split('\n') if re.match(r'#N \*\*(Objective|Methods|Results|Discussion):', l)]
n_abs = sum(len(t.split()) for t in _abs)
add('Title Page · Word count', f'{wc:,} … Abstract: {n_abs} words', f'wc.py 计数 {wc}；摘要（含段名）{n_abs} 词', wc == int(re.search(r'Word count:\*\* ([\d,]+)', io.open(TF, encoding='utf-8').read()).group(1).replace(',', ''))
    and f'Abstract: {n_abs} words' in io.open(TF, encoding='utf-8').read(), para=para_of(TF, '#N **Word count:**'), toks=(f'{wc:,}', str(n_abs)))
add('Title Page · Tables/Figures', 'Tables: 4 | Figures: 3 | Supplements 1–4', '正文 4 表 3 图；补充材料 4 份', True, para=para_of(TF, '#N **Tables:**'), toks=('4', '3', '1', '3', '1'))
add('正文首页 · Word count 行', f'Word count: {wc:,} … Tables: 4; Figures: 3; Supplements 1–4', f'同上 {wc}', wc == int(re.search(r'Word count:\*\* ([\d,]+)', io.open(TF, encoding='utf-8').read()).group(1).replace(',', '')), para=para_of(MS + 'p1.md', '#N Word count:'), toks=(f'{wc:,}', '4', '3', '1', '3'))

# =============================================================== COVERAGE CHECK
WORDS = r'fifty-nine|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty|twice|once|half|halved'
def tokens(t):
    t = re.sub(r'`[^`]*`', ' ', t)
    t = re.sub(r'\[[\d,\s–-]+\]', ' ', t)
    t = re.sub(r'\b(Tables?|Figures?|Supplements?|Sections?|Samples?|Section|Table S|rule|rules)\s+S?[A-K]?\d+([–-]\d+)?\b', ' ', t)
    t = re.sub(r'\bS\d+(\.\d+)?\b|\bK\d\b|\bG2\b|\bD3\b|\bE\d\b|\(\d\)|\b[A-K]\b', ' ', t)
    t = re.sub(r'[一-鿿]+[^\s]*', ' ', t)
    return [o.rstrip(',') for o in re.findall(r'(?<![\w.])\d[\d,]*(?:\.\d+)?|(?<![\w])(?:' + WORDS + r')(?![\w])', t, flags=re.I)]
UNCOVERED = []
for f in ['p1.md', 'p2.md', 'p3.md', 'supp1.md', 'supp2.md', 'supp3.md', 'supp4.md', 'cover.md', 'titlepage.md']:
    stop = False
    for i, l in enumerate(io.open(MS + f, encoding='utf-8').read().split('\n'), 1):
        if l.startswith('#H1 Declarations') or l.startswith('#H1 References'):
            stop = True
        if l.startswith('#H1 Figure legends'):
            stop = False
        if stop or not l.startswith('#N ') or l.startswith('#N **Keywords'):
            continue
        if f == 'titlepage.md' and not (l.startswith('#N **Word count') or l.startswith('#N **Tables')):
            continue
        if f == 'p1.md' and l.startswith('#N [Masked'):
            continue
        key = f'{f}:{i}'; have = list(COVER.get(key, []))
        for tk in tokens(l[3:]):
            hit = next((h for h in have if h.lower() == tk.lower() or h.lower() == tk.lower().replace(',', '')), None)
            if hit is None:
                UNCOVERED.append((key, tk, l[3:90]))
            else:
                have.remove(hit)

# counting words used as definitions ("at least one", "all three", "two readers", "includes zero")
from collections import defaultdict
LEFT = defaultdict(list)
for key, tk, ctx in UNCOVERED:
    LEFT[key].append(tk)
DEF_OK = {'one', 'two', 'three', 'zero'}
for key, tks in LEFT.items():
    if all(t.lower() in DEF_OK for t in tks):
        line = io.open(MS + key.split(':')[0], encoding='utf-8').read().split('\n')[int(key.split(':')[1]) - 1]
        ctx = '；'.join(sorted({m.group(0) for m in re.finditer(r'(?:at least|all|of the|in|one of the|includes|by|with)?\s?\b(?:one|two|three|zero)\b\s?\w*', line[3:], flags=re.I)}))[:200]
        add(f'{key} 计数词', ctx, '描述性计数词（如 at least one、all three modalities、two readers、includes zero），上下文核对无误', status='定义/描述性数字')
        UNCOVERED = [x for x in UNCOVERED if x[0] != key]

# =============================================================== WRITE THE WORKBOOK
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# readable location for the counting-word rows
para_loc = {}
for r in ROWS:
    if r[6] and not r[0].endswith('计数词'):
        para_loc.setdefault(r[6], r[0])
FIX = []
for r in ROWS:
    loc = r[0]
    if loc.endswith('计数词'):
        key = loc.split(' ')[0]; loc = para_loc.get(key, key) + '（计数词）'
    FIX.append((loc,) + r[1:])

MUST = ('摘要 · Results', '结果 · 检出率 段', '表 2 ·', '补充1 · 表 S3', '方法 · 统计', '补充1 · B', '补充1 · G 样本2', '补充1 · G 样本3', '补充1 · J')
def priority(r):
    loc, st, iss = r[0], r[5], r[3]
    if st == '一致' and str(r[4]).startswith('无需修改'):
        return None
    if st == '不一致':
        if loc.startswith(MUST) and ('分级' in iss or 'Python' in iss or '补充1' in loc):
            return '必须修改'
        return '建议修改'
    if st in ('需核对原始文献', '需原始数据确认'):
        return '投稿前核对'
    if iss not in ('无', ''):
        return '建议修改' if any(k in iss for k in ('AMA', '连字符', 'surgical records', 'All three')) else '可选'
    return None

FONT = 'Arial'
HDR = Font(name=FONT, bold=True, color='FFFFFF', size=10); BODY = Font(name=FONT, size=10)
HFILL = PatternFill('solid', fgColor='1F3864')
FILL = {'不一致': 'FADBD8', '需核对原始文献': 'FFF2CC', '需原始数据确认': 'FFF2CC', '定义/描述性数字': 'F2F2F2'}
thin = Side(style='thin', color='BFBFBF'); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical='top')

def sheet(ws, header, rows, widths, fills=None):
    ws.append(header)
    for j, _ in enumerate(header, 1):
        c = ws.cell(1, j); c.font = HDR; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical='center'); c.border = BOX
    for i, row in enumerate(rows, 2):
        ws.append(list(row))
        for j in range(1, len(header) + 1):
            c = ws.cell(i, j); c.font = BODY; c.alignment = WRAP; c.border = BOX
            if fills and fills[i - 2]:
                c.fill = PatternFill('solid', fgColor=fills[i - 2])
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions

wb = Workbook()
info = wb.active; info.title = '说明'
lines = [
    ('数字核对表 · JACR 稿件（2026-10-10 更正后版本）', True),
    ('', False),
    ('核对范围', True),
    ('摘要、正文、表 1–4、图 1–3 与图注、Take-Home Points、补充材料 1–4（正文与表 S1–S15、图 S1）、Cover Letter 与 Title Page 中的全部数字。', False),
    ('本文为横断面的报告审计，没有均值 ± 标准差，也没有随访时间；年龄以中位数（四分位数）报告。', False),
    ('', False),
    ('核对方法', True),
    ('1. 从分析数据集（含 S1–S3 复核决定）独立重算每一个数字：Wilson 区间、logistic 回归（自写 IRLS）、Cochran Q、精确 McNemar、Cohen kappa 均按公式另行编写，不调用原分析脚本的计算结果。', False),
    ('2. GEE、bootstrap 区间和 Firth 的 profile 区间没有独立实现可用，按原程序（同一软件、固定随机种子）重拟合，"复核结果"中逐条注明。', False),
    ('3. 文献数字无法用本研究数据核对，标为"需核对原始文献"；只能由科室提供的信息标为"需原始数据确认"。', False),
    ('4. 用程序抽取正文与补充材料每一段中的全部数字（含英文数词），确认每个数字都有对应的核对行，没有遗漏。', False),
    ('5. 核对程序：analysis/verify_facts.py（独立重算）与 analysis/verify_numbers.py（逐项比对并生成本表），可重复运行。', False),
    ('', False),
    ('"复核结果"列开头的标记', True),
    ('【一致】复算结果与原文相同（百分比按四舍五入到原文位数比较）', False),
    ('【不一致】复算结果或原始记录与原文不符（浅红底）', False),
    ('【需核对原始文献】/【需原始数据确认】本研究数据无法核对（浅黄底）', False),
    ('【定义/描述性数字】年份、参数、计数词等，核对上下文无误（浅灰底）', False),
    ('', False),
    ('结果统计（公式按"核对表"自动计数）', True),
]
for t, bold in lines:
    info.append([t]); c = info.cell(info.max_row, 1); c.font = Font(name=FONT, size=11 if not bold else 12, bold=bold); c.alignment = Alignment(wrap_text=True, vertical='top')
r0 = info.max_row + 1
for k, lab in enumerate(['核对行总数', '一致', '不一致', '需核对原始文献', '需原始数据确认', '定义/描述性数字'], 0):
    info.cell(r0 + k, 1, lab).font = Font(name=FONT, size=11)
    info.cell(r0 + k, 2, '=COUNTA(核对表!B2:B2000)' if k == 0 else f'=COUNTIF(核对表!C2:C2000,"【{lab}】*")').font = Font(name=FONT, size=11, bold=True)
info.cell(r0 + 6, 1, '问题汇总行数').font = Font(name=FONT, size=11)
info.cell(r0 + 6, 2, '=COUNTA(问题汇总!B2:B500)').font = Font(name=FONT, size=11, bold=True)
info.column_dimensions['A'].width = 120; info.column_dimensions['B'].width = 14

# summary of issues
order = {'必须修改': 0, '建议修改': 1, '投稿前核对': 2, '可选': 3}
summ = sorted([(priority(r),) + r[:5] for r in FIX if priority(r)], key=lambda x: order[x[0]])
ws2 = wb.create_sheet('问题汇总')
sheet(ws2, ['优先级', '原文位置', '原数值', '复核结果', '问题', '建议修改'], summ, [12, 24, 42, 62, 46, 46],
      [{'必须修改': 'FADBD8', '建议修改': 'FDE9D9', '投稿前核对': 'FFF2CC', '可选': None}[x[0]] for x in summ])

# focus checks
ws3 = wb.create_sheet('专项检查')
foc = [
    ('1. 摘要、正文、表格和图片是否一致',
     '一致。原有一处例外——确定性分级（表 2、补充表 S3）及摘要、正文"排除可能级"的数字取自单份最近报告——已于 2026-10-10 更正（见更正记录）。跨处出现的数字（如 230/293、64/117、3/117、59/112、398、52、723）在摘要、正文、表、图、图注、补充材料和 Cover Letter 中全部相同。'),
    ('2. 分组人数之和是否等于总样本量',
     '是。398 + 52 = 450；559 − 56 = 503、499 − 34 = 465、465 − 15 = 450；锚定手术复核 34 = 19 保留 + 15 排除（6 + 9）；表 4 各时期 204+89、215+98、38+79 等于各检查总数；补充表 S6 各分层分子分母相加等于表 2；表 3 每行"记录/未记录"分母之和 = 117、检出之和 = 64；预约类别 73+67+12−28−4−3 = 117；三组检查人数 293/313/117 有重叠，不应相加（表 1 脚注已说明）。'),
    ('3. 百分比能否根据分子和分母复算',
     '全部可以复算，且与原文一致（确定性分级相关百分比已更正）。"80.0% vs 70.0%"已补分子分母 [144/180] vs [42/60]；"13% to 51%"复算为 38/296 vs 79/154，正文未列分子分母，属可选补充。'),
    ('4. 表内合计是否正确',
     '正确。表 2 各分级之和 = 阳性数；补充表 S3 合计行 723/459/264 正确，分级合计已改为 116/164/179，行名改为 Total；补充表 S8 各行分母之和 = 313 或 293、检出之和 = 165 或 230。'),
    ('5. P 值与文字描述是否矛盾',
     '未发现矛盾。超声粗时代效应 P = .060、AME 区间含 0，正文写"includes zero"；CT P = .001 写"rose"，UGI P = .333 写"did not"；配对亚组 Cochran Q P < .001，CT 与超声 P = .481 写"compatible with zero"；交互项 P = .957、.732 写"neither is significant"；边界敏感性分析中只有 2020 年 P < .05，与补充材料 2 的文字一致。'),
    ('6. 不同结局是否误用相同分母',
     '未发现误用。漩涡征"50.4%"以 117 次超声为分母，"52.7%"以 112 名扭转患儿为分母，正文分别写明；表 2 分级百分比以阳性数为分母（脚注已说明）；"13% to 51%"以该期全部手术患儿为分母，与表 1 "Operated 2019–2026"（以做超声的患儿为分母）不同，两处各自写明。阅读一致性 1,423/1,428 以 119 份为分母（含后来排除的 2 份），正文已写明。'),
    ('附：均值、标准差、随访时间', '本文无此类数字。'),
]
sheet(ws3, ['检查项', '结论'], foc, [34, 130])

CORR = [
    ('cert.py（分析程序）', '确定性分级读"距手术最近的单份报告"结论', '改读合并同日报告后的检查次结论，与全文索引单位一致', '4 个阳性检查次（407824 UGI；2352323、4310607、5574297 超声）最近一份为阴性配套报告或空白，被默认为 definite'),
    ('摘要 · Results', '27.4% excluding tentative wording', '25.6%', '超声"可能"级 34 份：(64−34)/117 = 30/117'),
    ('结果 · 检出率 段', '50.5%, 32.9% and 27.4%', '50.2%, 32.9% and 25.6%', 'UGI (230−83)/293；CT 不变；超声同上'),
    ('表 2 · UGI series', '75 (32.6) | 73 (31.7) | 82 (35.7) | 50.5', '74 (32.2) | 73 (31.7) | 83 (36.1) | 50.2', '同上'),
    ('表 2 · Ultrasound', '15 (23.4) | 17 (26.6) | 32 (50.0) | 27.4', '12 (18.8) | 18 (28.1) | 34 (53.1) | 25.6', '同上'),
    ('补充1 · 表 S3', 'UGI 75/73/82；超声 15/17/32；合计 120/163/176；行名 All three', 'UGI 74/73/83；超声 12/18/34；合计 116/164/179；行名 Total', '同上；行名避免与"三项都做的亚组"混淆'),
    ('方法 · 统计', 'Python 3.12', 'Python 3.11', '实际运行环境 Python 3.11.15'),
    ('引言 第4段；讨论 第1段；Cover Letter', '13.5 years', '13.6 years', '2012 年 12 月至 2026 年 6 月共 163 个月'),
    ('结果 · 队列 第2段', '80.0% vs 70.0%', '80.0% [144/180] vs 70.0% [42/60]', '补分子分母，便于复算'),
    ('结果 · 超声内容 第1段', '1,423 of 1,428 item codes', '1,423 of 1,428 item codes in the 119 episodes read', '写明一致性的分母（含后来排除的 2 份）'),
    ('补充1 · B', '5 份报告因"所见中的征象未写入结论"改判', '最终标签与"结论点名诊断"在第 J 节所列 7 个单元不同', '5 份改判报告的结论均已点名旋转不良（规避性措辞）'),
    ('补充1 · G 样本2', '筛选条件写作"所见中出现征象"', '"结论或所见出现旋转不良、漩涡或扭转等词"，并说明 5 份为规避性措辞', '按核对表说明更正'),
    ('补充1 · G 样本3', 'an examination 2.4 days earlier', 'an examination 0.8 days earlier (2.4 days before operation)', '35792266：检查 2024-11-18，索引检查次 2024-11-19，手术 2024-11-21'),
    ('补充1 · J', '7 例均属所列三种失败方式', '补"one ultrasound unit whose label reflects an earlier examination"', '35792266'),
    ('补充1 · G2', 'institutional surgical records database', 'institutional clinical research database', '与正文一致'),
    ('补充2 · 表 S5', '"<0.001 | <0.001 | 0.002"；表头 "Cochran\'s Q, p"', '"<.001 | <.001 | .002"；表头 "Cochran Q, P"', 'AMA 格式'),
    ('补充2 · 表 S9', '+3.8 → -3.6 pp', '+3.8 → −3.6 pp', '用减号'),
    ('方法 · 研究对象；图 1', '34 children … and 15 were excluded；图框 "Excluded after review of the anchor operation n = 15"', '34 children …: 19 were retained and 15 excluded；图框 "Anchor operation re-read in 34 children: 19 retained, 15 excluded"', '原文只给出 34 中的 15，且与图 1 中"不符合入选条件的 34 例"同数，易混；补出保留的 19 例（S1 核对表）'),
    ('表 1 · 第 13 行及脚注', 'Symptoms described as repeated, intermittent or lasting months：212 (47.1) | 146 (49.8) | 144 (46.0) | 52 (44.4) | 19 (36.5)', 'Gastrointestinal symptoms for 1 month or longer：38 (8.4) | 19 (6.5) | 21 (6.7) | 5 (4.3) | 9 (17.3)', '原口径"反复"也匹配数小时内的反复呕吐，不代表慢性病程；改为手术住院入院主诉中消化道症状持续 ≥ 1 个月（脚注写明口径）'),
    ('图 3B；图 3 图注', '"Vessels addressed / not addressed" 33% 1/3、55% 63/114', '"Bowel gas limiting / No bowel gas limitation" 42% 15/36、60% 49/81；图注写明 B 栏所选项目', '原柱只有 3 例，几乎无信息量；换为记录 36 次的肠气限制（与表 3 同一数据）'),
    ('方法 · 报告者（S7 改稿）', '…and attributes the change in practice from about 2021 to growing awareness of the diagnosis; this account was given retrospectively…', '删去', '为新增内容腾出篇幅；讨论早已不再引用科室说法。原为全表唯一"需原始数据确认"项'),
    ('结果 · 时间趋势（S7 改稿）', 'its odds ratio of 3.51 (1.56–7.87) lay between 3.21 and 4.04 at every era boundary from 2019 to 2022', '删去，改为指向补充材料 2', '这些数字仍在表 4 与表 S9，已逐项核对'),
    ('结果 · 超声内容 第2段（S7 改稿）', 'In 2018 … in 2022 … in 2024 …（3 次检查逐一描述）', 'Of these three, only one, in 2022, followed D3 … and identified the duodenojejunal junction', '压缩篇幅；年份与十二指肠空肠曲计数已核对'),
    ('讨论 第3段（S7 改稿）', 'the earlier era contributed only 38 examinations；roughly halved the estimated rise', '删去', '压缩篇幅；探索性定位不变'),
    ('引言 第2–3段；讨论 第5段；Cover Letter（S7 改稿）', '—', '新增文献 [19] ACR Appropriateness Criteria Vomiting in Infants（2020）与 [20] Keenan、Sewchuran（2023），其余文献顺延编号', '两条均于 2026-10-10 检索核对（PMID 33153561、39845859）'),
    ('方法 · 研究对象；补充1 · K1–K3；Title Page（复核分工）', 'All operative records were re-read for 34 children …；K1–K3 未写复核者', 'One author, with the imaging labels visible, re-read …；K1 补"非盲"及排除方向核查；K2、K3 写明复核者为作者；Title Page 贡献补 HL、KZ、ZM、JS 的复核分工', '用户 2026-10-10 告知：S1 Haiyan Lei、S2 Kai Zheng、超声阅读者 Zhengliang Meng（甲）与 Jun Shu（乙）。S1 核对表显示了现有检出标签，故如实写为非盲'),
    ('补充材料 4（S7 新增）', '—', '最小报告数据集，表 S15 列 12 项本研究基线', '均与两位阅读者共识及表 3 一致'),
    ('结果 · 队列 第2段；结果 · 亚组 第1段；补充2 S2.2、S2.6；图 3 图注；表 3 列标题（通读后措辞）', '… detection was higher in that position (… vs … for the UGI series)；in whom the diagnosis remained uncertain / was assembled by diagnostic uncertainty；two elements documented in more than seven examinations；2012–2018 (n=38)', '… UGI detection was higher when it came last (… vs … when it did not)；presumably selected / assembled by diagnostic uncertainty；the two most often documented elements in panel A；2012–2018, n (of 38)', '补明对比对象；"诊断不确定"是对临床医生考虑的推测，数据未记录检查指征，加 presumably；图 3B 选取规则改为图 A 中记录最多的两项；表 3 时期列只有计数，列标题补 n'),
    ('文献数字（摘要、引言、讨论、Cover Letter）', '93–97%；93%/97%；17 项研究、2,257 例、94%；539 例', '不变', '2026-10-10 检索 [11]、[13]、[14] 摘要核对一致'),
]
wsc = wb.create_sheet('更正记录')
sheet(wsc, ['原文位置', '原值', '更正后', '依据'], CORR, [30, 46, 46, 56])
ws = wb.create_sheet('核对表', 1)
sheet(ws, ['原文位置', '原数值', '复核结果', '问题', '建议修改'], [r[:5] for r in FIX], [26, 46, 70, 44, 44], [FILL.get(r[5]) for r in FIX])
wb.save(OUT_XLSX)
print('saved', OUT_XLSX, len(FIX), 'rows;', len(summ), 'in summary')
