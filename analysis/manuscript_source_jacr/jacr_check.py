# -*- coding: utf-8 -*-
"""Pre-submission checks of the built JACR files against the journal's limits.

Run after the builders. Every check prints PASS or FAIL; the script exits
non-zero if any check fails.
"""
import docx, glob, os, re, sys
from docx.oxml.ns import qn
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usspell import british_left

ROOT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
fails = 0


def check(ok, msg):
    global fails
    print(('PASS ' if ok else 'FAIL ') + msg)
    fails += (not ok)


def paras(path):
    d = docx.Document(path)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag in (qn('w:p'), qn('w:tbl')):
            t = ''.join(x.text or '' for x in el.iter(qn('w:t')))
            if t.strip():
                out.append(t)
    return d, out


ms_doc, ms = paras(ROOT + 'JACR_3_Manuscript_masked.docx')
title = ms[0]
check(len(title) <= 129 and not title.rstrip().endswith('?'), f'title {len(title)} characters, not a question')

i = ms.index('Abstract')
abstract = ms[i + 1:i + 5]
words = sum(len(p.split()) for p in abstract)
check([p.split(':')[0] for p in abstract] == ['Objective', 'Methods', 'Results', 'Discussion'], 'abstract headings Objective/Methods/Results/Discussion (JACR guide)')
check(words <= 250, f'abstract {words} words incl. headings (limit 250)')
check(not any(re.search(r'\[\d', p) for p in abstract), 'no citations in the abstract')
kw = [p for p in ms if p.startswith('Keywords:')][0]
check(3 <= len(kw.split(':', 1)[1].split(';')) <= 5, 'keywords 3-5')

a, b = ms.index('Introduction'), ms.index('Supplemental Material')
body = [p for p in ms[a:b] if not p.startswith('Table ')]
# tables, table titles and footnotes are excluded, as in wc.py
import subprocess
wc = int(subprocess.check_output([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wc.py')]).strip())
stated = re.search(r'Word count: ([\d,]+)', ' '.join(ms)).group(1).replace(',', '')
check(wc < 3000 and int(stated) == wc, f'main text {wc} words (stated {stated}; limit <3,000)')
tp_doc, tp = paras(ROOT + 'JACR_2_TitlePage.docx')
tps = re.search(r'Word count: ([\d,]+)', ' '.join(tp)).group(1).replace(',', '')
check(int(tps) == wc, 'title-page word count matches')

ntab = len(ms_doc.tables)
nfig = len([p for p in ms if re.match(r'Figure \d\. ', p)])
check(ntab + nfig <= 7, f'{ntab} tables + {nfig} figures = {ntab + nfig} (limit 7)')
check(any(p == 'Limitations' for p in ms), 'formal Limitations section')
th = ms[ms.index('Take-Home Points') + 1:ms.index('Supplemental Material')]
check(3 <= len(th) <= 6, f'{len(th)} take-home points (3-6)')
summary = th[0].lstrip('• ').strip()
check(len(summary.split()) <= 35 and summary in ' '.join(ms), f'summary sentence {len(summary.split())} words, verbatim in manuscript')

# Items the JACR Guide for Authors (ScienceDirect, printed 2026-10-08) names explicitly
DATA_STMT = ('The authors declare that they had full access to all of the data in this study and the authors take '
             'complete responsibility for the integrity of the data and the accuracy of the data analysis.')
check(any(DATA_STMT in p for p in tp), 'title page carries the JACR data statement verbatim')
check(any(p.startswith('Leadership roles:') for p in tp), 'title page lists leadership roles')
check(any(p.startswith('Author contributions (by ICMJE activity):') for p in tp), 'contributions listed by ICMJE activity')
check(not any(p.startswith(('Declaration of competing interest', 'Competing interests')) for p in tp),
      'no conflict-of-interest statement on the title page (uploaded separately)')
AI_HEAD = 'Declaration of generative AI and AI-assisted technologies in the writing process:'
check(any(p.startswith(AI_HEAD) for p in tp), 'title page AI declaration uses the JACR heading')
ai_at = [i for i, p in enumerate(ms) if p.startswith(AI_HEAD)]
check(len(ai_at) == 1 and ai_at[0] < ms.index('References'), 'manuscript AI declaration uses the JACR heading, before the references')
check(ms.index('Figure Legends') > ms.index('References'), 'figure legends follow the references')
check(len(ms_doc.inline_shapes) == 3, f'{len(ms_doc.inline_shapes)} figures embedded in the manuscript (initial submission)')
auth = [p for p in tp if p.startswith('Authors:')][0]
n_auth = len(auth.split(':', 1)[1].split(','))
check(n_auth <= 7, f'{n_auth} authors on the title page (limit 7)')
for name in ('Guanghua Zhang', 'Hongxi Guo', 'Haibin Wang'):
    where = [p.split(':')[0] for p in tp if name in p]
    check(where == ['Acknowledgments'], f'{name} appears only in Acknowledgments')

masked = ['JACR_3_Manuscript_masked.docx', 'JACR_Supplement_1_NLP_and_report_audit.docx',
          'JACR_Supplement_2_models_and_subgroups.docx', 'JACR_Supplement_3_CT_and_UGI_content_audit.docx',
          'JACR_STROBE_checklist.docx']
ident = re.compile(r'Wuhan|Tongji|Huazhong|2026R018|Jun Yang|Jun Shu|Bian|Zhengliang|Haiyan|Kai Zheng|Fei Peng|yjun')
for f in masked:
    d, ps = paras(ROOT + f)
    hits = sorted({m.group(0) for p in ps for m in ident.finditer(p)})
    check(not hits, f'{f}: no identifying text {hits if hits else ""}')
    cp = d.core_properties
    check(not (cp.author or cp.last_modified_by), f'{f}: document properties blank')

stale = re.compile(r'Online Resource|Key Point|Critical relevance|Insights into Imaging|Graphical abstract|\bFig\. |171/320|65/119|54\.6%|0\.31 \(0\.22–0\.44|0\.33 \(0\.21–0\.50'
                   # values retired by the S1-S3 review (cohort 465 -> 450)
                   r'|237/301|169/320|64/119|58 of 113|58/113|\b410 children')
# Supplement 1 Section K legitimately describes the 740 units and the 119
# ultrasound episodes held before the review, so these apply everywhere else
stale_post = re.compile(r'\b740 index|\b119 ultrasound|of the 119\b')
for f in sorted(glob.glob(ROOT + 'JACR_*.docx')):
    if f.endswith('投稿操作单.docx'):
        continue
    _, ps = paras(f)
    refs = False
    text = []
    for p in ps:
        if p == 'References':
            refs = True
        if p.startswith('Figure 1.') or re.match(r'Table \d\. ', p):
            refs = False
        if not refs:
            text.append(p)
    t = '\n'.join(text)
    check(not british_left(t), f'{os.path.basename(f)}: American spelling {british_left(t) or ""}')
    hits = sorted({m.group(0) for m in stale.finditer(t)})
    if 'Supplement_1' not in f:
        hits = sorted(set(hits) | {m.group(0) for m in stale_post.finditer(t)})
    check(not hits, f'{os.path.basename(f)}: no stale IiI terms or retired values {hits if hits else ""}')

refs = [p for p in ms if re.match(r'\d+\. ', p)]
cited = {int(n) for p in ms[:ms.index('References')] for grp in re.findall(r'\[([\d,\s–-]+)\]', p)
         for part in grp.split(',') for n in (range(int(part.split('–')[0]), int(part.split('–')[-1]) + 1) if '–' in part else [part.strip()])}
check(cited == set(range(1, len(refs) + 1)), f'{len(refs)} references, every one cited')
check(all(re.search(r'\. \d{4};\d+:[\w-]+\. doi:10\.', r) for r in refs), 'references in AMA layout')
print('\n%d check(s) failed' % fails if fails else '\nall checks passed')
sys.exit(1 if fails else 0)
