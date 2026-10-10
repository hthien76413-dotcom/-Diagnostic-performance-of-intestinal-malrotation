# -*- coding: utf-8 -*-
"""Supplement 4, Table S15: the minimum reporting dataset, with this audit's
documentation rates as the baseline for a second audit cycle.

Reads the consensus coding of the 117 ultrasound index episodes (us_audit4.csv,
written by usaudit4.py) and writes mrd.json. The wording of each row is the
dataset; only the last column is data.
"""
import json
import pandas as pd

u = pd.read_csv('us_audit4.csv')
N = len(u)
assert N == 117


def base(k):
    n = int(u[k].astype(bool).sum())
    return f'{n} ({n / N * 100:.1f})'


# element | what the report states | documented in this audit when the report... | baseline
ROWS = [
    ('Third portion of the duodenum (D3)',
     'Whether D3 was seen crossing between the superior mesenteric artery and the aorta, or that it was not visualized',
     'names the third (horizontal) portion, whether normal, abnormal or not visualized', base('d3')),
    ('Duodenojejunal junction',
     'Its position, or that it was not visualized',
     'names the duodenojejunal junction or its position', base('djj')),
    ('Superior mesenteric artery–vein relationship',
     'The position of the vein relative to the artery, or that it was not assessed',
     'states the position of the two vessels relative to each other', base('sma_smv')),
    ('Enteric fluid',
     'Whether fluid was given, by which route, and whether its passage was followed',
     'states that fluid was given by mouth or tube (fluid seen in the lumen does not count)', base('fluid')),
    ('Dynamic assessment',
     'Whether passage of fluid through the pylorus and duodenum was observed in real time',
     'states real-time observation, or describes fluid passing the pylorus or duodenum', base('dynamic')),
    ('Graded compression',
     'Whether graded compression was used to displace bowel gas',
     'states that compression was used', base('compress')),
    ('Color Doppler of the mesenteric vessels',
     'That the mesenteric vessels were examined with color Doppler',
     'states color Doppler examination', base('doppler')),
    ('Whirlpool sign',
     'Present or absent, stated explicitly in either case',
     'describes a whirlpool or swirl, or a vein, mesentery or bowel rotating around the artery (present only; a stated absence was not coded)', base('whirl_pos')),
    ('Study adequacy',
     'Whether the examination was diagnostic, and if not, what limited it (bowel gas, patient state, incomplete views)',
     'states explicitly that bowel gas limited the study (other statements of adequacy were not coded)', base('gas_limit')),
    ('Conclusion',
     'Malrotation and volvulus addressed separately, each as present, absent or indeterminate, with the recommended next test when indeterminate',
     'not coded as such; the certainty tiers of positive conclusions are given in Table 2 of the manuscript', 'Not coded'),
]
# audited items that are indicators rather than statements the dataset asks for
INDICATORS = [
    ('Duodenum mentioned in any form', 'mentions the duodenum in any form (a lower bound on duodenal assessment)', base('duodenum')),
    ('Explicit statement of vessel inversion', 'states that the vessels are inverted (one of the two ultrasound positivity criteria)', base('inversion')),
    ('Cecal position', 'states where the cecum lies', base('cecum')),
]

T = [['Element', 'What the report states', 'Counted as documented in this audit when the report…',
      f'Documented in this audit, n (%) of {N}']]
T += [list(r) for r in ROWS]
T += [['Also audited, not part of the dataset', '', '', '']]
T += [[a, '', b, c] for a, b, c in INDICATORS]
json.dump({'MRD': T}, open('mrd.json', 'w'), ensure_ascii=False, indent=1)
for r in T:
    print(' | '.join(r))
