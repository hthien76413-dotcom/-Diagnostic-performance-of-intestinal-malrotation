# -*- coding: utf-8 -*-
"""Four sensitivity analyses added after a statistical review of the Methods and
Results (Supplement 2, S2.7 to S2.10; Tables S16 to S19).

  A. Effect sizes for the between-modality comparison: adjusted odds ratios and
     standardized detection with risk differences (cluster bootstrap by child).
  B. The same comparison under three other outcome definitions: conclusions that
     name malrotation, possible-tier conclusions counted negative, and the label
     of the published conclusion-only classifier (Supplement_1_classifier.py).
  C. Index-unit and timing sensitivity: closest, earliest and any preoperative
     episode; calendar-day interval between examination and operation; detection
     restricted to examinations within 2 days of operation.
  D. Ultrasound content documentation by booking category and in three
     alternative denominators.

Nothing here changes the primary analysis. Writes hp_sens.json.
"""
exec(open('core.py').read())
import json, re, sys, time, importlib.util
import numpy as np, pandas as pd
import statsmodels.api as sm, statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportion_confint as pci

B = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
SEED = 20261010
OUT = {}

spec = importlib.util.spec_from_file_location('ref_classifier', BASE + 'Supplement_1_classifier.py')
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)


def wil(k, n):
    lo, hi = pci(k, n, method='wilson')
    return 100 * lo, 100 * hi


def rate(k, n):
    lo, hi = wil(k, n)
    return f'{k}/{n} ({100 * k / n:.1f}; {lo:.1f}–{hi:.1f})'


# ---------------------------------------------------------------- episodes
rep['day'] = rep['检查时间'].dt.normalize()
POSS = r'可疑|可能|\?|？|不除外|不排除|待排|待除外|建议.{0,10}(除外|排除|进一步)|似'
PROB = r'多考虑|首先考虑|考虑|倾向|符合.{0,6}表现'


def tier(s):
    if re.search(POSS, s): return 'possible'
    if re.search(PROB, s): return 'probable'
    return 'definite'


def names_mal(t):
    for c in re.split(r'[。；;\n]+', str(t)):
        for m in re.finditer(r'旋转不良', c):
            if not re.search(r'未见|未探及|未显示|未发现|无明显|不明显|不考虑', c[max(0, m.start() - 12):m.start()]):
                return True
    return False


def pooled(how):
    asc = how == 'closest'
    first = rep.sort_values('gap', ascending=asc).groupby(['科研患者编号', 'mod']).first().reset_index()[
        ['科研患者编号', 'mod', 'day']]
    p = rep.merge(first, on=['科研患者编号', 'mod', 'day'], how='inner')
    return p.groupby(['科研患者编号', 'mod']).agg(concl=('concl', '\n'.join), day=('day', 'first')).reset_index()


CL = pooled('closest'); EA = pooled('earliest')
ALL = (rep.groupby(['科研患者编号', 'mod', 'day']).agg(concl=('concl', '\n'.join)).reset_index())
ALL['ref'] = [ref.classify(c, m)[0] for c, m in zip(ALL['concl'], ALL['mod'])]

fin = long[['科研患者编号', 'mod', 'detected', 'neonate', 'era_late', 'volvulus', 'age_days', 'op_year']]
D = CL.merge(fin, on=['科研患者编号', 'mod'], how='inner')
assert len(D) == len(long) == 723
D['named'] = ((D['detected'] == 1) & D['concl'].map(names_mal)).astype(int)
D['strict'] = ((D['detected'] == 1) & (D['concl'].map(tier) != 'possible')).astype(int)
D['ref'] = [ref.classify(c, m)[0] for c, m in zip(D['concl'], D['mod'])]
D['agegrp'] = pd.cut(D['age_days'], [-1, 28, 365, 1e5], labels=['neonate', '1-12mo', '>1y'])
D['era'] = D['era_late'].astype(int)
D['modality'] = pd.Categorical(D['mod'], categories=['UGI', 'CT', 'US'])
D = D.sort_values('科研患者编号').reset_index(drop=True)
# sanity: the definitions reproduce the manuscript's Table 2
for m, (kn, ks) in {'UGI': (228, 147), 'CT': (152, 103), 'US': (63, 30)}.items():
    d = D[D['mod'] == m]
    print(f'{m}: primary {int(d.detected.sum())}/{len(d)}, named {int(d.named.sum())}, strict {int(d.strict.sum())}, ref {int(d.ref.sum())}')
    assert int(d.named.sum()) == kn and int(d.strict.sum()) == ks, m

# ---------------------------------------------------------------- GEE helpers
FORM = '{y} ~ C(modality, Treatment("{r}")) + era + C(agegrp, Treatment("neonate"))'


def gee(d, y, r='UGI'):
    d = d.copy(); d['modality'] = pd.Categorical(d['mod'], categories=[r] + [m for m in ['UGI', 'CT', 'US'] if m != r])
    return smf.gee(FORM.format(y=y, r=r), '科研患者编号', data=d, family=sm.families.Binomial(),
                   cov_struct=sm.cov_struct.Exchangeable()).fit()


def or_ci(m, key):
    ci = m.conf_int().loc[key]
    return float(np.exp(m.params[key])), float(np.exp(ci[0])), float(np.exp(ci[1])), float(m.pvalues[key])


def standardized(m, d):
    """Detection each modality would have if every child had it: the fitted model
    is applied to the covariates of all children with at least one index test."""
    kids = d.drop_duplicates('科研患者编号')[['科研患者编号', 'era', 'agegrp']]
    res = {}
    for mod in ['UGI', 'CT', 'US']:
        x = kids.copy(); x['modality'] = pd.Categorical([mod] * len(x), categories=['UGI', 'CT', 'US'])
        res[mod] = 100 * float(m.predict(x).mean())
    return res


def fit_std(d, y):
    m = gee(d, y)
    return m, standardized(m, d)


def boot_std(d, y, B, rng):
    kids = d['科研患者编号'].unique(); grp = {k: g for k, g in d.groupby('科研患者编号')}
    out = []
    for _ in range(B):
        pick = rng.choice(kids, len(kids), replace=True)
        parts = []
        for j, k in enumerate(pick):
            g = grp[k].copy(); g['科研患者编号'] = j; parts.append(g)
        s = pd.concat(parts, ignore_index=True)
        try:
            s = s.copy(); s['agegrp'] = pd.Categorical(s['agegrp'], categories=['neonate', '1-12mo', '>1y'])
            if s[y].nunique() < 2 or s['mod'].nunique() < 3 or s['agegrp'].nunique() < 3 or s['era'].nunique() < 2:
                continue
            mm = gee(s, y); st = standardized(mm, s)
            out.append((st['UGI'], st['CT'], st['US']))
        except Exception:
            pass
    a = np.array(out)
    return a


def pct(a, f):
    v = f(a); return np.percentile(v, [2.5, 97.5])


# ---------------------------------------------------------------- A and B
DEFS = [('primary', 'detected', 'Primary: final label'),
        ('named', 'named', 'Conclusion names malrotation'),
        ('strict', 'strict', 'Possible-tier conclusions counted negative'),
        ('ref', 'ref', 'Conclusion-only classifier (Supplement_1_classifier.py)')]
def run_def(item):
    """One outcome definition: adjusted odds ratios, standardized detection and
    cluster-bootstrap intervals. Own random stream per definition, so the result
    does not depend on how the work is distributed over processes."""
    n, (key, y, lab) = item
    rng = np.random.default_rng(SEED + n)
    m_ugi = gee(D, y, 'UGI'); m_ct = gee(D, y, 'CT')
    ors = {'CT vs UGI': or_ci(m_ugi, 'C(modality, Treatment("UGI"))[T.CT]'),
           'US vs UGI': or_ci(m_ugi, 'C(modality, Treatment("UGI"))[T.US]'),
           'US vs CT': or_ci(m_ct, 'C(modality, Treatment("CT"))[T.US]')}
    st = standardized(m_ugi, D)
    rates = {m: (int(D[(D['mod'] == m)][y].sum()), int((D['mod'] == m).sum())) for m in ['UGI', 'CT', 'US']}
    bt = boot_std(D, y, B, rng)
    ci = {'UGI': pct(bt, lambda a: a[:, 0]), 'CT': pct(bt, lambda a: a[:, 1]), 'US': pct(bt, lambda a: a[:, 2]),
          'CT−UGI': pct(bt, lambda a: a[:, 1] - a[:, 0]), 'US−UGI': pct(bt, lambda a: a[:, 2] - a[:, 0]),
          'US−CT': pct(bt, lambda a: a[:, 2] - a[:, 1])}
    return key, dict(label=lab, rates=rates, ors=ors, std=st, ci={k: [float(x) for x in v] for k, v in ci.items()}, nboot=int(len(bt)))


from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
AB = {}
t0 = time.time()
with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context('fork')) as ex:
    for key, r in ex.map(run_def, list(enumerate(DEFS))):
        AB[key] = r
for key, y, lab in DEFS:
    r = AB[key]; st = r['std']
    print(f'[{key}] {lab}: ORs ' + '; '.join(f'{k} {v[0]:.2f} ({v[1]:.2f}–{v[2]:.2f})' for k, v in r['ors'].items()) +
          f' | std {st["UGI"]:.1f}/{st["CT"]:.1f}/{st["US"]:.1f} | boot {r["nboot"]}')
    for k in ['CT−UGI', 'US−UGI', 'US−CT']:
        a, b = r['ci'][k]
        pt = {'CT−UGI': st['CT'] - st['UGI'], 'US−UGI': st['US'] - st['UGI'], 'US−CT': st['US'] - st['CT']}[k]
        print(f'     {k}: {pt:+.1f} pp ({a:+.1f} to {b:+.1f})')
print(f'bootstrap done in {time.time() - t0:.0f}s', flush=True)
OUT['AB'] = AB

# ---------------------------------------------------------------- C
cl = CL.copy()
op = pat.set_index('科研患者编号')['op_dt'].dt.normalize()
cl['op_day'] = cl['科研患者编号'].map(op)
cl['interval'] = (cl['op_day'] - cl['day']).dt.days
assert (cl['interval'] >= 0).all()
CR = {'interval': {}, 'units': {}, 'restricted': {}}
for m in ['UGI', 'CT', 'US']:
    v = cl.loc[cl['mod'] == m, 'interval']
    CR['interval'][m] = dict(n=int(len(v)), median=float(v.median()), q1=float(v.quantile(.25)), q3=float(v.quantile(.75)),
                            d0=int((v == 0).sum()), d1=int((v == 1).sum()), d2_7=int(((v >= 2) & (v <= 7)).sum()), d8=int((v > 7).sum()),
                            max=int(v.max()))
    print(m, CR['interval'][m])
# closest vs earliest vs any, all under the conclusion-only classifier
for m in ['UGI', 'CT', 'US']:
    a = CL[CL['mod'] == m][['科研患者编号', 'day']].merge(ALL[ALL['mod'] == m][['科研患者编号', 'day', 'ref']], on=['科研患者编号', 'day'])
    e = EA[EA['mod'] == m][['科研患者编号', 'day']].merge(ALL[ALL['mod'] == m][['科研患者编号', 'day', 'ref']], on=['科研患者编号', 'day'])
    anyp = ALL[ALL['mod'] == m].groupby('科研患者编号')['ref'].max()
    kids = a['科研患者编号']
    nsame = int((CL[CL['mod'] == m].set_index('科研患者编号')['day'] == EA[EA['mod'] == m].set_index('科研患者编号')['day']).sum())
    nepi = ALL[ALL['mod'] == m].groupby('科研患者编号').size()
    CR['units'][m] = dict(n=len(a), final=int(D[D['mod'] == m]['detected'].sum()), closest=int(a['ref'].sum()), earliest=int(e['ref'].sum()),
                         anypos=int(anyp.loc[kids].sum()), n_multi=int((nepi > 1).sum()), n_diff=len(a) - nsame)
    print(m, CR['units'][m])
# detection restricted to examinations within 2 calendar days of operation
R = D.merge(cl[['科研患者编号', 'mod', 'interval']], on=['科研患者编号', 'mod'])
for lim in (0, 1, 2):
    s = R[R['interval'] <= lim]
    row = {}
    for m in ['UGI', 'CT', 'US']:
        d = s[s['mod'] == m]; row[m] = (int(d['detected'].sum()), int(len(d)))
    mm = {}
    if lim == 2:
        g = gee(s, 'detected', 'UGI')
        mm = {'CT vs UGI': or_ci(g, 'C(modality, Treatment("UGI"))[T.CT]'), 'US vs UGI': or_ci(g, 'C(modality, Treatment("UGI"))[T.US]')}
        g2 = gee(s, 'detected', 'CT'); mm['US vs CT'] = or_ci(g2, 'C(modality, Treatment("CT"))[T.US]')
    CR['restricted'][f'le{lim}'] = dict(rates=row, ors=mm, children=int(s['科研患者编号'].nunique()))
    print('interval <=', lim, row, mm)
OUT['C'] = CR

# ---------------------------------------------------------------- D
u = pd.read_csv('us_audit4.csv')
u = u.merge(pat[['科研患者编号', 'neonate']], on='科研患者编号', how='left')
for c in ['vessel_us', 'gi_us', 'pyloric', 'bedside', 'neonate']:
    u[c] = u[c].astype(bool)
for c in ['d3_or_djj', 'sma_smv', 'fluid', 'whirl_pos']:
    u[c] = u[c].astype(bool)
assert len(u) == 117
groups = [('All ultrasound examinations (primary denominator)', pd.Series(True, index=u.index)),
          ('Booked as gastrointestinal', u['gi_us']),
          ('Booked as abdominal great-vessel', u['vessel_us']),
          ('Booked as gastrointestinal or great-vessel', u['gi_us'] | u['vessel_us']),
          ('Booked as pyloric only', u['pyloric'] & ~u['gi_us'] & ~u['vessel_us']),
          ('Performed at the bedside', u['bedside']),
          ('Child aged 28 days or younger', u['neonate'])]
DT = []
for lab, mask in groups:
    d = u[mask]; n = len(d)
    DT.append(dict(label=lab, n=n, d3=int(d['d3_or_djj'].sum()), sma=int(d['sma_smv'].sum()), fluid=int(d['fluid'].sum()),
                   whirl=int(d['whirl_pos'].sum()), det=int(d['det'].sum())))
    print(DT[-1])
OUT['D'] = DT
# the headline element in the two denominators that exclude pyloric-only sessions
json.dump(OUT, open('hp_sens.json', 'w'), ensure_ascii=False, indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else float(o))
print('done', f'{time.time() - t0:.0f}s')
