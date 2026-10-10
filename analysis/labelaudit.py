# -*- coding: utf-8 -*-
"""Two-directional check of the final labels against the index report text.

Asks, for every patient-modality index episode, whether the adjudicated label
can be reconstructed from the exported report text: are there episodes labelled
positive with no diagnostic term or modality-specific sign anywhere in their
findings and conclusion, and are there episodes labelled negative whose text
names the diagnosis? Writes 待核标签清单_9例.txt with the full text of every
flagged case so the labels can be checked against the source records.

The lexical patterns cannot see a sign that is described morphologically
without being named, which is failure mode (ii) in Online Resource 1 Section G,
so a flagged episode is a case to read, not a proven error.
"""
import re, io
exec(open('core.py').read())

NAMED = r'肠旋转不良|中肠旋转不良|旋转不良|中肠扭转|肠扭转|肠系膜扭转|小肠扭转'
SIGN = {'US':  r'漩涡|旋涡|涡流|螺旋|换位|反位|倒置|关系异常|异常关系',
        'CT':  r'漩涡|旋涡|涡流|螺旋|十二指肠.{0,8}(位置异常|异常位置)',
        'UGI': r'弹簧|螺旋|绞索|盘曲|十二指肠空肠曲.{0,10}(异常|偏|低|中线|右)'}

rep['day'] = rep['检查时间'].dt.normalize()
first = (rep.sort_values('gap').groupby(['科研患者编号', 'mod']).first()
            .reset_index()[['科研患者编号', 'mod', 'day']])
pool = rep.merge(first, on=['科研患者编号', 'mod', 'day'], how='inner')
IX = (pool.groupby(['科研患者编号', 'mod'])
          .agg(txt=('txt', '\n'.join), concl=('concl', '\n'.join)).reset_index()
          .merge(long.rename(columns={'detected': 'det'})[['科研患者编号', 'mod', 'det']],
                 on=['科研患者编号', 'mod'], how='inner'))
IX['has'] = [bool(re.search(NAMED, str(t)) or re.search(SIGN[m], str(t)))
             for t, m in zip(IX['txt'], IX['mod'])]

flagged, out = [], []
for mod in ['UGI', 'CT', 'US']:
    d = IX[IX['mod'] == mod]
    pos_no_text = d[(d['det'] == 1) & (~d['has'])]
    neg_named = d[(d['det'] == 0) & (d['txt'].astype(str).str.contains(NAMED, regex=True))]
    print(f'{mod} (n={len(d)}): positive without text support {len(pos_no_text)}; '
          f'negative naming the diagnosis {len(neg_named)}')
    flagged += [(r['科研患者编号'], mod) for _, r in pos_no_text.iterrows()]

out.append('待核标签清单：最终标签为阳性、但导出报告文本中找不到依据的 %d 例' % len(flagged))
out.append('（反方向核查：判阴性而文本含诊断名者见上方计数）')
out.append('')
for i, (pid, mod) in enumerate(flagged, 1):
    d = rep[(rep['科研患者编号'] == pid) & (rep['mod'] == mod)].sort_values('gap')
    earlier = any(re.search(NAMED, str(q['txt'])) or re.search(SIGN[mod], str(q['txt']))
                  for _, q in d.iloc[1:].iterrows())
    out.append(f'{i}. 患者 {pid} ｜ 模态 {mod} ｜ 术前该模态报告 {len(d)} 份'
               + ('（更早一次报告含阳性内容，属索引单位与结局不同步）' if earlier else ''))
    for _, q in d.iterrows():
        out.append(f'   ── 距手术 {q["gap"]:.2f} 天 ｜ {q["报告名称"]}')
        out.append(f'      所见：{str(q["检查所见"])[:300].strip()}')
        out.append(f'      结论：{str(q["检查结论"])[:300].strip()}')
    out.append('   请核：(a) 导出数据是否漏报告 (b) 当时判阳性的依据 (c) 是否确为错标')
    out.append('')
io.open(BASE + '待核标签清单_9例.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(f'\nwrote 待核标签清单_9例.txt with {len(flagged)} cases')
