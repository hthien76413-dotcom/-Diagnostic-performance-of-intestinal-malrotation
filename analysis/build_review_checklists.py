# -*- coding: utf-8 -*-
"""Build the adjudication workbooks for review items S1-S3.

S1  anchor operations that may not have confirmed malrotation at that operation
S2  index examinations whose timing relative to the operation is uncertain
    (operation times are recorded as dates only) or very early (>7 days)
S3  the 119 ultrasound index episodes, for independent manual reading by two
    readers, blinded to the detection label, the era and the program's coding

Writes 审稿核对表_S1-S3.xlsx (instructions, S1, S2, S3 for reader A) and
S3超声报告阅读_阅读者乙.xlsx (the same S3 sheet for reader B) to the repository
root. Run from analysis/:  python3 build_review_checklists.py
"""
import math
import re

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

exec(open('core.py').read())

ROOT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
MAIN = ROOT + '审稿核对表_S1-S3.xlsx'
READER_B = ROOT + 'S3超声报告阅读_阅读者乙.xlsx'

FONT = 'Arial'
HEAD_FILL = PatternFill('solid', fgColor='1F3864')
INPUT_FILL = PatternFill('solid', fgColor='FFF2CC')
FLAG_FILL = PatternFill('solid', fgColor='FCE4D6')
THIN = Side(style='thin', color='BFBFBF')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def clean(s):
    s = '' if s is None or (isinstance(s, float) and math.isnan(s)) else str(s)
    return re.sub(r'\n{2,}', '\n', s.replace('\r', '')).strip()


def labels(pid):
    m = mat[mat['科研患者编号'] == pid]
    if m.empty:
        return '不在分析矩阵中'
    r = m[['US_detected', 'CT_detected', 'UGI_detected']].iloc[0]
    out = [f'{k.split("_")[0]}={"检出" if v == 1 else "未检出"}' for k, v in r.items() if v == v]
    return '；'.join(out) if out else '无索引检查'


def write_sheet(ws, header, rows, widths, input_cols, validations=(), body_size=9):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(name=FONT, size=10, bold=True, color='FFFFFF')
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
        c.border = BOX
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        longest = 1
        for c in row:
            c.font = Font(name=FONT, size=body_size)
            c.alignment = Alignment(wrap_text=True, vertical='top')
            c.border = BOX
            w = widths[c.column - 1]
            text = '' if c.value is None else str(c.value)
            lines = sum(max(1, math.ceil(len(seg) * 1.9 / max(w, 1))) for seg in text.split('\n'))
            longest = max(longest, lines)
        ws.row_dimensions[row[0].row].height = min(400, 13 * longest + 4)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[1].height = 34
    ws.freeze_panes = 'C2'
    last = ws.max_row
    for col in input_cols:
        L = get_column_letter(col)
        for r in range(2, last + 1):
            ws[f'{L}{r}'].fill = INPUT_FILL
    for formula, col, first, lastrow in validations:
        dv = DataValidation(type='list', formula1=formula, allow_blank=True,
                            errorTitle='请从下拉列表选择', error='请从下拉列表中选择一项。')
        L = get_column_letter(col)
        dv.add(f'{L}{first}:{L}{lastrow}')
        ws.add_data_validation(dv)
    return last


# ---------- S1: anchor operations ----------
first = ops.sort_values('op_dt').groupby('科研患者编号').first().reset_index()
first = first[first['科研患者编号'].isin(coh['科研患者编号'])].set_index('科研患者编号')
proc = first['手术名称'].fillna('').astype(str)
dx1 = first['术中诊断'].fillna('').astype(str)
is_ladd = proc.str.contains(r'(?i)lad+|拉德|复位|扭转|旋转不良')
status_post = dx1.str.contains(r'旋转不良[^，,；;。]{0,6}术后|旋转不良（术后）|旋转不良\(术后\)')
queried = dx1.str.contains(r'旋转不良\s*[？?]|[？?]\s*旋转不良|旋转不良可能|疑似[^，,；;]{0,4}旋转不良')
endoscopy_only = proc.str.contains(r'镜检查|镜下[^，,+]*活组织|活组织检查|活检') & ~proc.str.contains(r'(?i)lad+|拉德|开腹|剖腹|腹腔镜(?!检查)')
# status-post with a Ladd/derotation anchor: recurrence or redo. 5001066 is excluded
# because its 术后 refers to atresia, not to malrotation.
redo = status_post & is_ladd & ~dx1.str.contains(r'旋转不良\s+肠闭锁术后')

raw_ops = x.parse('住院病历手术记录')
raw_ops['手术日期及时间'] = pd.to_datetime(raw_ops['手术日期及时间'], errors='coerce')

s1_ids = list(proc[~is_ladd].index) + [p for p in proc[redo].index if p not in set(proc[~is_ladd].index)]
s1_rows = []
for n, pid in enumerate(s1_ids, start=1):
    reasons = []
    if status_post[pid] and not is_ladd[pid]:
        reasons.append('诊断写"肠旋转不良术后"（既往已手术），本次手术不是旋转不良手术')
    if redo[pid]:
        reasons.append('有既往旋转不良手术史，本次为 Ladd/复位（复发或再次手术）')
    if queried[pid]:
        reasons.append('诊断中的旋转不良带问号或"可能"')
    if endoscopy_only[pid]:
        reasons.append('本次操作为内镜或活检，未开腹/腹腔镜探查')
    if not reasons:
        reasons.append('手术名称中无 Ladd/复位/旋转不良字样')
    others = raw_ops[(raw_ops['科研患者编号'] == pid)].sort_values('手术日期及时间')
    other_txt = '\n'.join(
        f'{"【锚定】" if d.date() == first.loc[pid, "op_dt"].date() else ""}{d.date()}｜{clean(dg)[:60]}｜{clean(pr)[:50]}'
        for d, dg, pr in zip(others['手术日期及时间'], others['术中诊断'], others['手术名称']))
    s1_rows.append([
        n, int(pid), '；'.join(reasons), first.loc[pid, 'op_dt'].date().isoformat(),
        int(coh.loc[coh['科研患者编号'] == pid, '该患者手术记录条数'].iloc[0]),
        clean(dx1[pid]), clean(proc[pid]), clean(first.loc[pid, '手术经过']), other_txt, labels(pid), None, None])

# ---------- S2: timing of index examinations ----------
ix = idx[['科研患者编号', 'mod', '检查时间']].rename(columns={'检查时间': 'idx_t'})
pooled = rep.merge(ix, on=['科研患者编号', 'mod'])
pooled = pooled[pooled['检查时间'].dt.normalize() == pooled['idx_t'].dt.normalize()]
sameday = pooled[pooled['检查时间'].dt.normalize() == pooled['op_dt'].dt.normalize()].copy()
early = idx[idx['gap'] > 7].copy()
MODCN = {'US': '超声', 'CT': 'CT', 'UGI': '上消化道造影'}
POSTOP = re.compile(r'术后|手术后|吻合口')
s2_rows = []
for _, r in sameday.sort_values(['科研患者编号', '检查时间']).iterrows():
    hint = '报告含"术后/吻合口"字样，可能是术后检查' if POSTOP.search(r['txt']) else ''
    s2_rows.append(['手术当日', int(r['科研患者编号']), r['op_dt'].date().isoformat(), MODCN[r['mod']],
                    r['检查时间'].to_pydatetime(), clean(r['报告名称']), clean(r['检查所见']), clean(r['检查结论']), hint])
n_same = len(s2_rows)
for _, r in early.sort_values(['gap'], ascending=False).iterrows():
    s2_rows.append([f'距手术 {r["gap"]:.0f} 天', int(r['科研患者编号']), r['op_dt'].date().isoformat(), MODCN[r['mod']],
                    r['检查时间'].to_pydatetime(), clean(r['报告名称']), clean(r['检查所见']), clean(r['检查结论']),
                    '索引检查距手术超过 7 天，可能与本次手术的病程无关'])
s2_rows = [[i] + row for i, row in enumerate(s2_rows, start=1)]

# ---------- S3: ultrasound index episodes ----------
us = pooled[pooled['mod'] == 'US'].sort_values(['科研患者编号', '检查时间'])
s3_rows = []
for n, (pid, g) in enumerate(us.groupby('科研患者编号', sort=False), start=1):
    names = '；'.join(clean(v) for v in g['报告名称'])
    if len(g) > 1:
        find = '\n'.join(f'【{clean(a)}】{clean(b)}' for a, b in zip(g['报告名称'], g['检查所见']))
        concl = '\n'.join(f'【{clean(a)}】{clean(b)}' for a, b in zip(g['报告名称'], g['检查结论']))
    else:
        find, concl = clean(g['检查所见'].iloc[0]), clean(g['检查结论'].iloc[0])
    s3_rows.append([n, int(pid), names, find, concl] + [None] * 13)
assert len(s3_rows) == 119, len(s3_rows)

ITEMS = ['十二指肠第三段（水平部/横部）', '十二指肠空肠交界（屈氏韧带）', '提及十二指肠（任何形式）',
         '肠系膜上动、静脉位置关系', '明确写出动静脉换位/倒置', '写明检查前给液（口服或胃管注入）',
         '动态观察', '加压或逐级加压', '回盲部位置', '使用彩色多普勒', '漩涡征（阳性描述，未被否定）',
         '肠气干扰显示（明确写出）']


def add_s3(wb, title):
    ws = wb.create_sheet(title)
    header = ['序号', '患者编号', '报告名称', '检查所见（同日多份报告已合并）', '检查结论'] + ITEMS + ['备注']
    widths = [5, 10, 18, 70, 36] + [9] * len(ITEMS) + [18]
    last = write_sheet(ws, header, s3_rows, widths, input_cols=range(6, 6 + len(ITEMS) + 1),
                       validations=[('"是,否"', c, 2, 120) for c in range(6, 6 + len(ITEMS))])
    ws.freeze_panes = 'F2'
    return ws, last


# ---------- workbook ----------
wb = openpyxl.Workbook()
info = wb.active
info.title = '说明'

s1 = wb.create_sheet('S1_锚定手术判定')
S1_OPTS = '"本次手术确认肠旋转不良（保留）,非本次手术确认（排除）,复发再次手术（单独讨论）,无法判定"'
s1_last = write_sheet(
    s1, ['序号', '患者编号', '筛出原因', '锚定手术日期', '该患儿纳入手术记录条数', '术中诊断（锚定手术）',
         '手术名称（锚定手术）', '手术经过（锚定手术，全文）', '该患儿全部手术记录（日期｜诊断｜手术名称）',
         '现有检出标签', '【填】判定', '【填】依据/备注'],
    s1_rows, [5, 10, 30, 11, 9, 34, 30, 70, 46, 16, 22, 26], input_cols=[11, 12],
    validations=[(S1_OPTS, 11, 2, 1 + len(s1_rows))])

s2 = wb.create_sheet('S2_术前时间核对')
s2_last = write_sheet(
    s2, ['序号', '类型', '患者编号', '手术日期', '模态', '检查时间', '检查名称', '检查所见', '检查结论', '程序提示',
         '【填】手术开始时间（时:分）', '按时间自动判断', '【填】判定', '【填】备注'],
    [row + [None, None, None, None] for row in s2_rows],
    [5, 11, 10, 11, 10, 16, 18, 52, 34, 22, 13, 11, 18, 20], input_cols=[11, 13, 14],
    validations=[('"术前（保留）,术后（剔除）,无法判断"', 13, 2, 1 + n_same),
                 ('"保留,排除（与本次手术病程无关）"', 13, 2 + n_same, 1 + len(s2_rows))])
for r in range(2, s2_last + 1):
    s2[f'F{r}'].number_format = 'yyyy-mm-dd hh:mm'
    s2[f'K{r}'].number_format = 'hh:mm'
    if r <= 1 + n_same:
        # exam time-of-day against the operation start time entered in column K
        s2[f'L{r}'] = f'=IF(K{r}="","",IF(MOD(F{r},1)<K{r},"术前","术后"))'
    else:
        s2[f'L{r}'] = '不适用'
    if s2[f'J{r}'].value:
        s2[f'J{r}'].fill = FLAG_FILL

s3, s3_last = add_s3(wb, 'S3_超声报告阅读_甲')

# ---------- instructions ----------
info.column_dimensions['A'].width = 3
info.column_dimensions['B'].width = 24
info.column_dimensions['C'].width = 100
lines = [
    ('title', '审稿意见 S1–S3 核对表'),
    ('', ''),
    ('h', '这份表是做什么的'),
    ('p', '审稿意见中的三项严重问题都需要人工核实，核实完成后才能重算全文数字。三个工作表分别对应一项，每例都附有原始记录全文。'),
    ('p', '只需要填写浅黄色的列，其余各列请不要改动。判定栏点开后从下拉列表里选。'),
    ('', ''),
    ('h', 'S1_锚定手术判定'),
    ('k', '谁来填', '一名外科医生，最好熟悉这些病例。'),
    ('k', '判断什么', '每例只判断一件事：这一次手术中是否确认了肠旋转不良。依据 H 列的手术经过全文和 I 列的全部手术记录。'),
    ('k', '共几例', f'{len(s1_rows)} 例：手术名称里没有 Ladd/复位/旋转不良字样的锚定手术 {int((~is_ladd).sum())} 例，加上有既往旋转不良手术史、这次为 Ladd/复位的 {int(redo.sum())} 例。'),
    ('k', '选项含义', '"本次手术确认（保留）"：术中直接看到旋转不良，或做了针对旋转不良的处理。'
                     '"非本次手术确认（排除）"：旋转不良只是既往诊断或附带诊断。'
                     '"复发再次手术（单独讨论）"：既往做过 Ladd，这次因复发再次手术。'),
    ('', ''),
    ('h', 'S2_术前时间核对'),
    ('k', '为什么要核', '数据中的手术时间只有日期，没有具体时刻，所以手术当天做的检查无法判断是在术前还是术后。已发现 1 例（3826010）的唯一一次超声其实是术后检查。'),
    ('k', '首选做法', f'从手术麻醉系统查出这些患儿的手术开始时间，填入 K 列（格式：14:30）。L 列会自动给出"术前/术后"，M 列可以不填。手术当日的检查共 {n_same} 份报告，涉及 {sameday["科研患者编号"].nunique()} 名患儿；同一患儿有几行就每行都填一次。'),
    ('k', '查不到时间时', '根据报告内容人工判断，在 M 列选"术前（保留）/术后（剔除）/无法判断"。J 列标了橙色的是报告里出现"术后/吻合口"字样的。'),
    ('k', '距手术超过 7 天', f'表格末尾 {len(early)} 行是距手术超过 7 天的索引检查（最长一份在术前约一年）。请在 M 列判断它是否属于导致本次手术的这段病程。'),
    ('', ''),
    ('h', 'S3_超声报告阅读'),
    ('k', '谁来填', '两名阅读者独立完成，至少一名是超声科医师。阅读者甲填本文件的 S3 工作表，阅读者乙填单独发给他的文件《S3超声报告阅读_阅读者乙.xlsx》。两人完成前不要互相看结果。'),
    ('k', '判断什么', '对 119 份超声报告的每一项内容，判断报告里"有没有写"，只看报告写了什么，不推测医生做了什么。'),
    ('k', '计"是"的规则', '技术要素（十二指肠、血管关系、回盲部、彩色多普勒等）只要报告写到就计"是"，不论结果正常还是异常。'
                       '漩涡征只有在阳性描述时才计"是"，写"未见漩涡征"计"否"。'
                       '给液只有写明"口服/注入"时才计"是"，只看到肠腔内有液体不算。'
                       '肠气干扰只有明确写出影响显示时才计"是"。'),
    ('k', '刻意不提供的信息', '表中没有检查日期、检出标签和程序的自动编码，以免影响判断。'),
    ('', ''),
    ('h', '填写示例（非真实病例）'),
    ('k', 'S1 示例', '判定："非本次手术确认（排除）"；依据："本次为粘连松解术，手术经过未描述肠管旋转情况，旋转不良为 2015 年外院手术史"。'),
    ('k', 'S2 示例', 'K 列填 09:40；L 列自动显示"术前"（检查时间 08:15 早于开刀时间）。'),
    ('k', 'S3 示例', '报告写"十二指肠水平部位于肠系膜上动脉后方"：十二指肠第三段=是，提及十二指肠=是，肠系膜上动、静脉位置关系=否（除非同时写了动静脉关系）。'),
    ('', ''),
    ('h', '填写进度（自动统计）'),
]
r = 1
for kind, *vals in lines:
    if kind == 'title':
        info.cell(r, 2, vals[0]).font = Font(name=FONT, size=14, bold=True)
    elif kind == 'h':
        info.cell(r, 2, vals[0]).font = Font(name=FONT, size=11, bold=True)
    elif kind == 'p':
        c = info.cell(r, 2, vals[0]); c.font = Font(name=FONT, size=10)
        info.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        c.alignment = Alignment(wrap_text=True, vertical='top')
        info.row_dimensions[r].height = 30
    elif kind == 'k':
        a = info.cell(r, 2, vals[0]); a.font = Font(name=FONT, size=10, bold=True); a.alignment = Alignment(vertical='top')
        b = info.cell(r, 3, vals[1]); b.font = Font(name=FONT, size=10); b.alignment = Alignment(wrap_text=True, vertical='top')
        info.row_dimensions[r].height = max(16, 15 * math.ceil(len(vals[1]) * 1.9 / 100))
    r += 1
progress = [
    ('S1 已判定', f"=COUNTA('S1_锚定手术判定'!K2:K{s1_last})", f'/ {len(s1_rows)} 例'),
    ('S2 已填手术时间或已判定',
     f"=SUMPRODUCT(--((('S2_术前时间核对'!K2:K{s2_last}<>\"\")+('S2_术前时间核对'!M2:M{s2_last}<>\"\"))>0))",
     f'/ {len(s2_rows)} 行'),
    ('S3 阅读者甲已读完', f"=COUNTIF('S3_超声报告阅读_甲'!Q2:Q{s3_last},\"?*\")", '/ 119 份（以"漩涡征"列已填计）'),
]
for label, formula, unit in progress:
    info.cell(r, 2, label).font = Font(name=FONT, size=10, bold=True)
    c = info.cell(r, 3, formula); c.font = Font(name=FONT, size=10); c.alignment = Alignment(horizontal='left')
    info.cell(r, 4, unit).font = Font(name=FONT, size=10)
    r += 1
info.column_dimensions['D'].width = 32
info.cell(r + 1, 2, '填完后把文件发回即可，我会据此剔除或保留病例并重算全部结果。').font = Font(name=FONT, size=10, italic=True)

def print_setup(book):
    # printable: landscape, every column on one page width, header row repeated
    for ws in book.worksheets:
        ws.sheet_view.zoomScale = 100
        ws.page_setup.orientation = 'portrait' if ws.title == '说明' else 'landscape'
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
        if ws.title != '说明':
            ws.print_title_rows = '1:1'


print_setup(wb)
wb.properties.creator = ''
wb.save(MAIN)

# ---------- reader B file ----------
wb2 = openpyxl.Workbook()
note = wb2.active
note.title = '说明'
note.column_dimensions['B'].width = 110
for i, t in enumerate([
        'S3 超声报告阅读（阅读者乙）',
        '请独立完成，完成前不要查看阅读者甲的结果。只填浅黄色的列，从下拉列表选"是/否"。',
        '只判断报告里"有没有写"，不推测医生做了什么。技术要素只要写到就计"是"，不论正常还是异常；'
        '漩涡征只有阳性描述计"是"；给液只有写明"口服/注入"才计"是"；肠气干扰只有明确写出影响显示才计"是"。',
        '示例：报告写"十二指肠水平部位于肠系膜上动脉后方"——十二指肠第三段=是，提及十二指肠=是。'], start=1):
    c = note.cell(i * 2 - 1, 2, t)
    c.font = Font(name=FONT, size=14 if i == 1 else 10, bold=(i == 1))
    c.alignment = Alignment(wrap_text=True, vertical='top')
    note.row_dimensions[i * 2 - 1].height = 18 if i == 1 else 32
add_s3(wb2, 'S3_超声报告阅读_乙')
print_setup(wb2)
wb2.properties.creator = ''
wb2.save(READER_B)
print(f'S1 {len(s1_rows)} cases | S2 {n_same} same-day reports + {len(early)} early index exams | S3 {len(s3_rows)} episodes')
print('saved', MAIN.split('/')[-1], 'and', READER_B.split('/')[-1])
