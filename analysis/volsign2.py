# -*- coding: utf-8 -*-
"""Volvulus-specific sign among children with operatively confirmed midgut volvulus,
on pooled index episodes, using the same negation-aware rules as the main audit."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import json, re
from statsmodels.stats.proportion import proportion_confint as pci
NEG=r'未见|未探及|未显示|未发现|无明显|不明显|未闻'
def reported(text,rx):
    for c in re.split(r'[。；;\n]+',str(text)):
        for m in re.finditer(rx,c):
            if not re.search(NEG,c[max(0,m.start()-12):m.start()]): return True
    return False
SIGN={'US':r'漩涡|旋涡|涡流|螺旋','CT':r'漩涡|旋涡|涡流|螺旋','UGI':r'弹簧|螺旋|绞索|盘曲'}
LAB={'UGI':'Upper gastrointestinal series','US':'Gastrointestinal ultrasound','CT':'Abdominal CT'}
rows=[['Index test','Volvulus-specific sign / children with confirmed midgut volvulus','Rate % (95% CI)']]
for mod in ['UGI','US','CT']:
    d=IX[IX['mod']==mod].merge(pat[['科研患者编号','volvulus']],on='科研患者编号',how='left')
    d=d[d['volvulus'].astype(bool)]
    s=d['txt'].map(lambda t: reported(t,SIGN[mod]))
    k=int(s.sum()); n=len(d); lo,hi=pci(k,n,method='wilson')
    rows.append([LAB[mod],f'{k}/{n}',f'{100*k/n:.1f} ({100*lo:.1f}–{100*hi:.1f})'])
    print(f'  {LAB[mod]:32s} {k}/{n} = {100*k/n:.1f}% ({100*lo:.1f}-{100*hi:.1f})')
json.dump({'S2b':rows},open('volsign2.json','w'),ensure_ascii=False,indent=1)
