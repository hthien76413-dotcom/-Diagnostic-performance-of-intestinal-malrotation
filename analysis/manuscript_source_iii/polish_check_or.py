# -*- coding: utf-8 -*-
"""Guard rail for the language pass over the three Online Resources.

Same contract as polish_check.py, with two additions the supplements need:
the Chinese source terms and the regular expressions in them are data, not
prose, so every CJK run and every backticked code span must survive the pass
byte for byte.
"""
import re, io, sys, collections, os

ROOT  = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/analysis/'
FILES = [ROOT + 'manuscript_source/or1.md',
         ROOT + 'manuscript_source_iii/or2_iii.md',
         ROOT + 'manuscript_source_iii/or3_iii.md']

NUM   = re.compile(r'(?<![A-Za-z])\d[\d,]*(?:\.\d+)?%?')
CJK   = re.compile(r'[　-鿿＀-￯]+')
CODE  = re.compile(r'`[^`]+`')
HEDGE = ['no evidence', 'compatible with zero', 'not estimable', 'uninterpretable',
         'lower bound', 'not randomised', 'cannot be separated', 'does not converge',
         'not pre-specified', 'hypothesis-generating', 'exploratory', 'conservative',
         'not adjusted', 'consistent with', 'associated with', 'no directional conclusion',
         'not sensitivities', 'not a population-level', 'no claim', 'could not be estimated',
         'cannot be estimated', 'not confirmatory', 'no minimum']

def toks(which):
    out = {}
    for f in FILES:
        p = f.replace('.md', '.bak') if which == 'old' else f
        s = io.open(p, encoding='utf-8').read()
        out[os.path.basename(f)] = dict(
            num=collections.Counter(NUM.findall(s)),
            cjk=collections.Counter(CJK.findall(s)),
            code=collections.Counter(CODE.findall(s)),
            hedge=collections.Counter({h: s.lower().count(h) for h in HEDGE}))
    return out

old, new = toks('old'), toks('new')
bad = 0
for f in [os.path.basename(x) for x in FILES]:
    for kind, label in (('num', '数字'), ('cjk', '中文原文'), ('code', '代码片段')):
        o, n = old[f][kind], new[f][kind]
        for k in set(o) | set(n):
            if o[k] != n[k]:
                bad += 1
                print(f'  ✗ {f} {label} {k!r}: 原 {o[k]} 次 -> 现 {n[k]} 次')
    for h in HEDGE:
        o, n = old[f]['hedge'][h], new[f]['hedge'][h]
        if o and not n:
            bad += 1
            print(f'  ✗ {f} 限定语 {h!r} 消失了（原 {o} 处）')
print('数字、中文原文、代码片段与限定语：完全一致' if not bad else f'\n共 {bad} 处差异需要确认')
sys.exit(1 if bad else 0)
