# -*- coding: utf-8 -*-
"""Agreement between the published reference implementation
(Online_Resource_1_classifier.py) and the final labels used in the analysis.

The comparison is at the level of the 740 index examination episodes: all
reports of a modality issued on the index day are pooled, exactly as the
analysis pools them, and the classifier is applied to the pooled conclusion.
"""
exec(open('core.py').read())
import importlib.util, pandas as pd

spec = importlib.util.spec_from_file_location(
    'ref_classifier', BASE + 'Online_Resource_1_classifier.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)

rep['day'] = rep['检查时间'].dt.normalize()
first = rep.sort_values('gap').groupby(['科研患者编号', 'mod']).first().reset_index()[
    ['科研患者编号', 'mod', 'day']]
IX = (rep.merge(first, on=['科研患者编号', 'mod', 'day'], how='inner')
         .groupby(['科研患者编号', 'mod'])
         .agg(concl=('concl', '\n'.join)).reset_index())

lab = {'US': 'US_detected', 'CT': 'CT_detected', 'UGI': 'UGI_detected'}
IX['final'] = [mat.set_index('科研患者编号')[lab[m]].get(p)
               for p, m in zip(IX['科研患者编号'], IX['mod'])]
IX = IX[IX['final'].notna()].copy()
IX['final'] = IX['final'].astype(int)
IX['ref'] = [ref.classify(c, m)[0] for c, m in zip(IX['concl'], IX['mod'])]

ok = IX['ref'] == IX['final']
print(f'index episodes compared: {len(IX)}')
print(f'agreement: {int(ok.sum())}/{len(IX)} ({100*ok.mean():.1f}%)')
for m in ['UGI', 'CT', 'US']:
    d = IX[IX['mod'] == m]; o = d['ref'] == d['final']
    print(f'  {m:4s} {int(o.sum())}/{len(d)} ({100*o.mean():.1f}%)')
dis = IX[~ok]
print(f'disagreements: {len(dis)} — '
      f'reference under-calls {int(((dis["final"]==1)&(dis["ref"]==0)).sum())}, '
      f'over-calls {int(((dis["final"]==0)&(dis["ref"]==1)).sum())}')
print(dis.groupby(['mod', 'final', 'ref']).size().to_string())
