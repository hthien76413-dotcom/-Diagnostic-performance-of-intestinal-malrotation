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

# Elsevier numeric layout: [n] A.B. Author, A.B. Author, Title, J. Abbrev. Volume (Year) Pages. https://doi.org/DOI
TAIL = re.compile(r'^(.*), ([^,]+?) (\d+) \((\d{4})\) (\S+(?: – \S+)?)\. https://doi\.org/(\S+)$')
AUTHOR = re.compile(r"^(?:[A-Z]\.)+ [A-ZÀ-Ý][\w'’\- ]+$")
rows = []
for line in io.open(SRC, encoding='utf-8'):
    line = line.rstrip()
    m = re.match(r'^#R \[(\d+)\] (.+)$', line)
    if not m:
        continue
    n, rest = m.groups()
    head, jo, vol, yr, pg, doi = TAIL.match(rest).groups()
    parts = head.split(', ')
    au = []
    while parts and (AUTHOR.match(parts[0]) or parts[0] == 'et al.' or (not au and parts[0].startswith('Expert Panel'))):
        au.append(parts.pop(0))
    ti = ', '.join(parts)
    rows.append((n, ', '.join(au), yr, ti, jo, vol, pg.replace(' – ', '–'), doi))
N = len(rows)
assert [int(r[0]) for r in rows] == list(range(1, N + 1)), 'references not numbered 1..N'
assert N == sum(1 for l in io.open(SRC, encoding='utf-8') if l.startswith('#R ')), 'a reference did not parse'

def ris_authors(s):
    for a in [x.strip() for x in s.split(', ') if x.strip() and x.strip() != 'et al.']:
        m = re.match(r'^((?:[A-Z]\.)+) (.+)$', a)
        yield f'{m.group(2)}, {m.group(1)}' if m else a   # group authors stay as written

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

# clean the file properties of every package document (author, times, thumbnail, embedded-image text chunks)
from scrub_metadata import scrub_all
scrub_all()
