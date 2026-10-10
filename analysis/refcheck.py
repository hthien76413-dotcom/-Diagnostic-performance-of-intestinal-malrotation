# -*- coding: utf-8 -*-
"""Compare the manuscript reference list against Zotero's Crossref-fetched output."""
import re, io

RTF='/root/.claude/uploads/4998e6b2-e14c-57b0-80b5-41a1fb987d43/2fae5034-________.rtf'
MS='/home/user/-Diagnostic-performance-of-intestinal-malrotation/analysis/manuscript_source_iii/p3.md'

raw=io.open(RTF,encoding='utf-8',errors='replace').read()
raw=re.sub(r'\\uc0\\u(\d+)\{\}', lambda m: chr(int(m.group(1))), raw)
raw=re.sub(r'\\u(\d+)\{?\}?', lambda m: chr(int(m.group(1))), raw)
raw=raw.replace('{\\i{}','').replace('}','').replace('\\i','')

zot={}
for line in raw.split('\\\n'):
    line=' '.join(line.split())
    m=re.search(r'https?://doi\.org/(\S+?)\.?$', line)
    if not m: continue
    doi=m.group(1).rstrip('.')
    au=line.split('《')[0].strip().rstrip(',').rstrip('.')
    tail=line.split('》')[-1]
    yr=re.search(r'\((\d{4})',tail)
    vol=re.search(r'(\d+),?\s*期?\s*\d*\s*\(',tail)
    pg=re.search(r'\):\s*([0-9e][0-9a-zA-Z]*(?:～[0-9]+)?)',tail)
    zot[doi]=dict(au=au, year=yr.group(1) if yr else '?',
                  vol=vol.group(1) if vol else '?',
                  pg=pg.group(1).replace('～','-') if pg else '?')

ms={}
for line in io.open(MS,encoding='utf-8'):
    m=re.match(r'^#R (\d+)\.\s+(.*?)\s+\((\d{4})\)\s+(.*?)\.\s+(.+?)\s+(\d+):(\S+)\s+https://doi\.org/(\S+)\s*$', line.strip())
    if m:
        n,au,yr,ti,jo,vol,pg,doi=m.groups()
        ms[doi]=dict(n=int(n),au=au,year=yr,jo=jo,vol=vol,pg=pg,ti=ti)

def endpage(sp,ep):
    """Chicago abbreviates end pages: 1485-500 means 1485-1500."""
    if not ep: return None
    return sp[:len(sp)-len(ep)]+ep if len(ep)<len(sp) else ep

print(f'{"#":>3} {"DOI":42} {"年":4} {"卷":5} {"页":16} 结果')
print('-'*118)
issues=[]
for doi,m in sorted(ms.items(), key=lambda x:x[1]['n']):
    z=zot.get(doi)
    if not z:
        issues.append((m['n'],'Zotero 中找不到该 DOI')); print(f'{m["n"]:>3} {doi:42} {"":4} {"":5} {"":16} ✗ 未抓到'); continue
    ok=[]; bad=[]
    (ok if m['year']==z['year'] else bad).append(f'年 稿:{m["year"]} vs Zotero:{z["year"]}')
    (ok if m['vol']==z['vol'] else bad).append(f'卷 稿:{m["vol"]} vs Zotero:{z["vol"]}')
    msp=re.split(r'[–-]',m['pg']); zsp=re.split(r'[-]',z['pg'])
    zfull=zsp[0] if len(zsp)==1 else f"{zsp[0]}-{endpage(zsp[0],zsp[1])}"
    msfull='-'.join(msp)
    if msfull==zfull: ok.append('页')
    elif len(zsp)==1 and msp[0]==zsp[0]: ok.append('页(仅起始页)'); issues.append((m['n'],f'Crossref 只有起始页 {zsp[0]}，稿件写 {msfull} —— 无法确认'))
    else: bad.append(f'页 稿:{msfull} vs Zotero:{zfull}')
    zau=z['au'].split(',')[0].strip()
    msau=m['au'].split(',')[0].split()[0]
    if msau.lower() not in z['au'].lower(): bad.append(f'首作者 稿:{msau} vs Zotero:{zau}')
    mark='✓' if not bad else '✗'
    print(f'{m["n"]:>3} {doi:42} {m["year"]:4} {m["vol"]:5} {msfull:16} {mark} ' + ('；'.join(bad) if bad else '全部一致'))
    for b in bad: issues.append((m['n'],b))
print()
print('需要处理的条目：')
for n,t in issues: print(f'  [{n}] {t}')
if not issues: print('  无')
