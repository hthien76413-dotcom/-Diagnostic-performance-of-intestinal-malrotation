# -*- coding: utf-8 -*-
"""Emit the reference list as (a) a bare DOI list and (b) an RIS file.

The DOI list is the one that matters: pasted into Zotero's "Add Item by
Identifier" (or looked up in EndNote), it makes the software fetch metadata
from Crossref/PubMed rather than trusting what is typed here. The RIS carries
the manuscript's own, UNVERIFIED metadata and exists only as a container to
run "Find Reference Updates" against, and as the thing to diff.
"""
import io, re, os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p3.md')
OUT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'

# AMA layout: Authors. Title. *Journal*. Year;Volume:Pages. doi:DOI
REF = re.compile(r'^#R (\d+)\.\s+(.+?)\.\s+(.+?)\.\s+\*(.+?)\*\.\s+(\d{4});(\d+(?:\([^)]*\))?):([^.\s]+)\.\s+doi:(\S+)\s*$')
rows = []
for line in io.open(SRC, encoding='utf-8'):
    m = REF.match(line.rstrip())
    if m:
        n, au, ti, jo, yr, vol, pg, doi = m.groups()
        rows.append((n, au, yr, ti, jo, vol, pg, doi))
N = len(rows)
assert [int(r[0]) for r in rows] == list(range(1, N + 1)), 'references not numbered 1..N'
assert N == sum(1 for l in io.open(SRC, encoding='utf-8') if l.startswith('#R ')), 'a reference did not parse'

def ris_authors(s):
    if ';' in s and ',' not in s.split(';')[0]:   # leading group author, e.g. 'Expert Panel on Pediatric Imaging; Alazraki AL, ...'
        g, s = s.split(';', 1)
        yield g.strip()
    s = s.split(';')[0]  # drop a trailing group author such as '; STROBE Initiative'
    s = s.replace(', et al', '').replace(' et al', '')
    for a in [x.strip() for x in s.split(',') if x.strip()]:
        parts = a.split()
        yield f'{" ".join(parts[:-1])}, {parts[-1]}' if len(parts) > 1 else a

with io.open(OUT + f'参考文献_{N}条_DOI清单.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(r[7] for r in rows) + '\n')

with io.open(OUT + f'参考文献_{N}条_编号对照.txt', 'w', encoding='utf-8') as f:
    for n, au, yr, ti, jo, vol, pg, doi in rows:
        f.write(f'[{n:>2}]  {doi}\n      {au} ({yr}) {ti}. {jo} {vol}:{pg}\n\n')

with io.open(OUT + f'参考文献_{N}条.ris', 'w', encoding='utf-8') as f:
    for n, au, yr, ti, jo, vol, pg, doi in rows:
        f.write('TY  - JOUR\n')
        for a in ris_authors(au): f.write(f'AU  - {a}\n')
        f.write(f'PY  - {yr}\nTI  - {ti}\nJO  - {jo}\nVL  - {vol}\n')
        parts = re.split(r'[–-]', pg)
        f.write(f'SP  - {parts[0]}\n')
        if len(parts) > 1: f.write(f'EP  - {parts[1]}\n')
        f.write(f'DO  - {doi}\nUR  - https://doi.org/{doi}\n')
        f.write(f'N1  - Manuscript reference [{n}]. Metadata UNVERIFIED - confirm against Crossref.\nER  - \n\n')

print(f'{len(rows)} references written: DOI list, numbered key, RIS')
