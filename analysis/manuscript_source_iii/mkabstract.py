# -*- coding: utf-8 -*-
"""Regenerate abstract.txt from p1.md, so the paste-in text cannot drift
from the manuscript. Run after editing p1.md:  python3 mkabstract.py
"""
import os, re
D = os.path.dirname(os.path.abspath(__file__))
ls = open(os.path.join(D, 'p1.md'), encoding='utf-8').read().split('\n')
a = ls.index('#H1 Abstract')
b = ls.index('#H1 Introduction')
out = []
for l in ls[a:b]:
    l = l.strip()
    if not l:
        continue
    if l.startswith('#H1 '):
        out += ['', l[4:], '']
    else:
        t = re.sub(r'^#N\s*', '', l).replace('**', '')
        out.append(t if t.startswith(('•', 'Keywords')) else t)
        out.append('')
txt = '\n'.join(out).strip()
txt = re.sub(r'\n{3,}', '\n\n', txt)
txt = re.sub(r'(?m)^(• .*)\n\n(?=• )', r'\1\n', txt)
open(os.path.join(D, 'abstract.txt'), 'w', encoding='utf-8').write(txt + '\n')
print('abstract.txt rebuilt from p1.md')
