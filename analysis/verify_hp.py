# -*- coding: utf-8 -*-
"""Independent recomputation of the four sensitivity analyses of hp_sens.py.

exec'd at the end of verify_facts.py, which supplies ROOT, rep, pat, long, EP,
tier, names_mal, wilson, np, pd, math and the statsmodels imports. Written apart
from hp_sens.py:
  * episodes are grouped by calendar day directly, the interval to operation is
    a calendar-day difference, and the closest and earliest episodes are the
    minimum and maximum interval;
  * the GEE is fitted from a hand-built design matrix (statsmodels.GEE with
    arrays, no formula), and standardized detection is computed from the
    fitted coefficients by hand;
  * the cluster bootstrap is re-run with a different seed and fewer resamples
    (300, spread over four processes) and compared with hp_sens.json within the
    Monte-Carlo error of that smaller run.
"""
import importlib.util
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

_spec = importlib.util.spec_from_file_location('ref_classifier2', ROOT + 'Supplement_1_classifier.py')
_ref = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_ref)
HP = {}

# ---- episodes by calendar day, own implementation
_rp = rep.copy(); _rp['day'] = _rp['检查时间'].dt.normalize()
_ep = _rp.groupby(['科研患者编号', 'mod', 'day']).agg(concl=('concl', '\n'.join)).reset_index()
_ep['ref'] = [_ref.classify(c, m)[0] for c, m in zip(_ep['concl'], _ep['mod'])]
_op = pat.set_index('科研患者编号')['op_dt'].dt.normalize()
_ep['interval'] = (_ep['科研患者编号'].map(_op) - _ep['day']).dt.days
assert (_ep['interval'] >= 0).all()
_g = _ep.groupby(['科研患者编号', 'mod'])
_clo = _ep.loc[_g['interval'].idxmin()].set_index(['科研患者编号', 'mod'])
_ear = _ep.loc[_g['interval'].idxmax()].set_index(['科研患者编号', 'mod'])
_any = _g['ref'].max()
_keys = long.set_index(['科研患者编号', 'mod']).index
HP['interval'] = {}; HP['units'] = {}
for m in ['UGI', 'CT', 'US']:
    k = [i for i in _keys if i[1] == m]
    iv = _clo.loc[k, 'interval']
    HP['interval'][m] = dict(n=len(k), median=float(iv.median()), q1=float(iv.quantile(.25)), q3=float(iv.quantile(.75)),
                             d0=int((iv == 0).sum()), d1=int((iv == 1).sum()), d2_7=int(((iv >= 2) & (iv <= 7)).sum()), d8=int((iv > 7).sum()))
    HP['units'][m] = dict(n=len(k), final=int(long[long['mod'] == m]['detected'].sum()), closest=int(_clo.loc[k, 'ref'].sum()),
                          earliest=int(_ear.loc[k, 'ref'].sum()), anypos=int(_any.loc[k].sum()),
                          n_multi=int((_ear.loc[k, 'interval'] != _clo.loc[k, 'interval']).sum()))

# ---- outcome definitions on the pooled index episode (EP from verify_facts)
_E = EP.copy()
_E['d_primary'] = _E['detected'].astype(int)
_E['d_named'] = ((_E['detected'] == 1) & _E['named']).astype(int)
_E['d_strict'] = ((_E['detected'] == 1) & (_E['tier'] != 'possible')).astype(int)
_E['d_ref'] = [_ref.classify(c, m)[0] for c, m in zip(_E['concl'], _E['mod'])]
_E = _E.merge(long[['科研患者编号', 'mod', 'era_late', 'age_days']], on=['科研患者编号', 'mod'])
_E['era'] = _E['era_late'].astype(float)
_E['a2'] = ((_E['age_days'] > 28) & (_E['age_days'] <= 365)).astype(float)
_E['a3'] = (_E['age_days'] > 365).astype(float)
_E = _E.sort_values(['科研患者编号', 'mod']).reset_index(drop=True)
_kid = _E.drop_duplicates('科研患者编号')[['科研患者编号', 'era', 'a2', 'a3']].reset_index(drop=True)


def _design(d, refm):
    others = [m for m in ['UGI', 'CT', 'US'] if m != refm]
    X = np.column_stack([np.ones(len(d))] + [(d['mod'] == m).to_numpy(float) for m in others] +
                        [d['era'].to_numpy(float), d['a2'].to_numpy(float), d['a3'].to_numpy(float)])
    return X, others


def _fit(d, y, refm='UGI'):
    X, others = _design(d, refm)
    return sm.GEE(d[y].to_numpy(float), X, groups=d['科研患者编号'].to_numpy(), family=sm.families.Binomial(),
                  cov_struct=sm.cov_struct.Exchangeable()).fit(), others


def _std(res, others, refm, kid):
    out = {}
    b = np.asarray(res.params)
    for m in ['UGI', 'CT', 'US']:
        eta = b[0] + (b[1 + others.index(m)] if m in others else 0.0) + b[3] * kid['era'].to_numpy() + b[4] * kid['a2'].to_numpy() + b[5] * kid['a3'].to_numpy()
        out[m] = 100 * float((1 / (1 + np.exp(-eta))).mean())
    return out


HP['rates'] = {}; HP['ors'] = {}; HP['std'] = {}
for key in ['primary', 'named', 'strict', 'ref']:
    y = 'd_' + key
    HP['rates'][key] = {m: (int(_E[_E['mod'] == m][y].sum()), int((_E['mod'] == m).sum())) for m in ['UGI', 'CT', 'US']}
    r, oth = _fit(_E, y, 'UGI'); ci = np.asarray(r.conf_int()); pr = np.asarray(r.params)
    r2, oth2 = _fit(_E, y, 'CT'); ci2 = np.asarray(r2.conf_int()); pr2 = np.asarray(r2.params)
    HP['ors'][key] = {'CT vs UGI': (math.exp(pr[1]), math.exp(ci[1, 0]), math.exp(ci[1, 1])),
                      'US vs UGI': (math.exp(pr[2]), math.exp(ci[2, 0]), math.exp(ci[2, 1])),
                      'US vs CT': (math.exp(pr2[oth2.index('US') + 1]), math.exp(ci2[oth2.index('US') + 1, 0]), math.exp(ci2[oth2.index('US') + 1, 1]))}
    HP['std'][key] = _std(r, oth, 'UGI', _kid)

# ---- detection within 0, 1 and 2 calendar days of operation (final label)
_E['interval'] = [int(_clo.loc[(p, m), 'interval']) for p, m in zip(_E['科研患者编号'], _E['mod'])]
HP['restricted'] = {}
for lim in (0, 1, 2):
    s = _E[_E['interval'] <= lim]
    HP['restricted'][lim] = {m: (int(s[s['mod'] == m]['d_primary'].sum()), int((s['mod'] == m).sum())) for m in ['UGI', 'CT', 'US']}
_s2 = _E[_E['interval'] <= 2]
_r, _o = _fit(_s2, 'd_primary', 'UGI'); _c = np.asarray(_r.conf_int()); _p = np.asarray(_r.params)
_r2, _o2 = _fit(_s2, 'd_primary', 'CT'); _c2 = np.asarray(_r2.conf_int()); _p2 = np.asarray(_r2.params)
HP['restricted_or'] = {'CT vs UGI': (math.exp(_p[1]), math.exp(_c[1, 0]), math.exp(_c[1, 1])),
                       'US vs UGI': (math.exp(_p[2]), math.exp(_c[2, 0]), math.exp(_c[2, 1])),
                       'US vs CT': (math.exp(_p2[_o2.index('US') + 1]), math.exp(_c2[_o2.index('US') + 1, 0]), math.exp(_c2[_o2.index('US') + 1, 1]))}

# ---- ultrasound content by booking category (Table S19)
_u = U.copy() if 'U' in globals() else None
_u = _u.merge(pat[['科研患者编号', 'neonate']], on='科研患者编号', how='left')
_grp = {'All ultrasound examinations (primary denominator)': pd.Series(True, index=_u.index),
        'Booked as gastrointestinal': _u['gi_us'].astype(bool),
        'Booked as abdominal great-vessel': _u['vessel_us'].astype(bool),
        'Booked as gastrointestinal or great-vessel': _u['gi_us'].astype(bool) | _u['vessel_us'].astype(bool),
        'Booked as pyloric only': _u['pyloric'].astype(bool) & ~_u['gi_us'].astype(bool) & ~_u['vessel_us'].astype(bool),
        'Performed at the bedside': _u['bedside'].astype(bool),
        'Child aged 28 days or younger': _u['neonate'].astype(bool)}
HP['content'] = {}
for lab, mask in _grp.items():
    d = _u[mask]
    HP['content'][lab] = dict(n=len(d), d3=int(d['d3_or_djj'].astype(bool).sum()), sma=int(d['sma_smv'].astype(bool).sum()),
                              fluid=int(d['fluid'].astype(bool).sum()), whirl=int(d['whirl_pos'].astype(bool).sum()), det=int(d['det'].sum()))


# ---- independent re-run of the cluster bootstrap (primary definition; other seed, 300 resamples)
def _boot_chunk(args):
    seed, nres = args
    rng = np.random.default_rng(seed)
    grp = {k: g for k, g in _E.groupby('科研患者编号')}
    ids_ = np.array(list(grp))
    res = []
    for _ in range(nres):
        pick = rng.choice(ids_, len(ids_), replace=True)
        parts = []
        for j, k in enumerate(pick):
            g = grp[k].copy(); g['科研患者编号'] = j; parts.append(g)
        s = pd.concat(parts, ignore_index=True)
        try:
            r, oth = _fit(s, 'd_primary', 'UGI')
            kid = s.drop_duplicates('科研患者编号')[['科研患者编号', 'era', 'a2', 'a3']]
            st = _std(r, oth, 'UGI', kid)
            res.append((st['UGI'], st['CT'], st['US']))
        except Exception:
            pass
    return res


with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context('fork')) as _ex:
    _parts = list(_ex.map(_boot_chunk, [(777 + i, 75) for i in range(4)]))
_a = np.array([r for p in _parts for r in p])
HP['boot_check'] = {'n': int(len(_a)),
                    'UGI': tuple(np.percentile(_a[:, 0], [2.5, 97.5])), 'CT': tuple(np.percentile(_a[:, 1], [2.5, 97.5])),
                    'US': tuple(np.percentile(_a[:, 2], [2.5, 97.5])),
                    'CT−UGI': tuple(np.percentile(_a[:, 1] - _a[:, 0], [2.5, 97.5])),
                    'US−UGI': tuple(np.percentile(_a[:, 2] - _a[:, 0], [2.5, 97.5])),
                    'US−CT': tuple(np.percentile(_a[:, 2] - _a[:, 1], [2.5, 97.5]))}
HP['ref_agree'] = (int((_E['d_primary'] == _E['d_ref']).sum()), int(len(_E)))
F['HP'] = HP
