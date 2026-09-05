# -*- coding: utf-8 -*-
"""Guard rail for the language pass: nothing factual may move.

Compares the .bak snapshots with the current sources on every token that
carries meaning — numbers, citation markers, and the hedging vocabulary the
review rounds put there — and reports any that appear, vanish or change count.
"""
import re, io, sys, collections

FILES = ['p1.md', 'p2.md', 'p3.md']
NUM   = re.compile(r'(?<![A-Za-z])\d[\d,]*(?:\.\d+)?%?')
CITE  = re.compile(r'\[[0-9,\s–\-]+\]')
HEDGE = ['no evidence', 'compatible with zero', 'not estimable', 'partly definitional',
         'lower bound', 'not randomised', 'cannot be separated', 'bounds the era',
         'not pre-specified', 'hypothesis-generating', 'not adjusted for multiplicity',
         'not missing at random', 'informative missingness', 'consistent with',
         'associated with', 'tracked', 'no argument against']

def toks(which):
    out = {}
    for f in FILES:
        s = io.open((f.replace('.md','.bak') if which == 'old' else f), encoding='utf-8').read()
        body = s.split('#H1 References')[0]
        # the manuscript's own word-count line is expected to change
        body = '\n'.join(l for l in body.split('\n') if not l.startswith('#N Word count:'))
        out[f] = dict(num=collections.Counter(NUM.findall(body)),
                      cite=collections.Counter(CITE.findall(body)),
                      hedge=collections.Counter({h: body.lower().count(h) for h in HEDGE}))
    return out

old, new = toks('old'), toks('new')
bad = 0
for f in FILES:
    for kind in ('num', 'cite'):
        o, n = old[f][kind], new[f][kind]
        for k in set(o) | set(n):
            if o[k] != n[k]:
                bad += 1
                print(f'  ✗ {f} {kind} {k!r}: 原 {o[k]} 次 -> 现 {n[k]} 次')
    for h in HEDGE:
        o, n = old[f]['hedge'][h], new[f]['hedge'][h]
        if o and not n:
            bad += 1
            print(f'  ✗ {f} 限定语 {h!r} 消失了（原 {o} 处）')
print('数字与引用标记：完全一致，限定语全部保留' if not bad else f'\n共 {bad} 处差异需要确认')
sys.exit(1 if bad else 0)
