# -*- coding: utf-8 -*-
"""Independent recomputation of every number the manuscript reports.

Reads the analysis dataset (core.py, with the S1-S3 review decisions applied,
and the pooled index episodes of usaudit4.py) and recomputes the reported
quantities with code written separately from the analysis scripts: Wilson
intervals, logistic regression (own IRLS), Cochran Q, exact McNemar and Cohen
kappa are implemented here from their formulas. Where only the original method
can reproduce a number (GEE, bootstrap intervals, Firth profile intervals) the
number is refitted with the same software and fixed seed, and the check table
says so.

exec'd by verify_numbers.py; defines the dict F of facts.
"""
import math, re, json
import numpy as np, pandas as pd
from scipy.stats import norm, binom, chi2

exec(open('usaudit4.py').read().split('ROWS=')[0])

ROOT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
F = {}


def wilson(k, n, z=1.959963984540054):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return 100 * (c - h), 100 * (c + h)


def irls(X, y):
    b = np.zeros(X.shape[1])
    for _ in range(200):
        mu = 1 / (1 + np.exp(-(X @ b)))
        W = mu * (1 - mu)
        H = X.T @ (X * W[:, None])
        step = np.linalg.solve(H, X.T @ (y - mu))
        b = b + step
        if np.max(np.abs(step)) < 1e-12:
            break
    mu = 1 / (1 + np.exp(-(X @ b)))
    H = X.T @ (X * (mu * (1 - mu))[:, None])
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return b, se


def orci(b, se, j):
    return (math.exp(b[j]), math.exp(b[j] - 1.959963984540054 * se[j]),
            math.exp(b[j] + 1.959963984540054 * se[j]), 2 * norm.sf(abs(b[j] / se[j])))


def ame(b, X):
    X0 = X.copy(); X0[:, 1] = 0
    X1 = X.copy(); X1[:, 1] = 1
    f = lambda M: (1 / (1 + np.exp(-(M @ b)))).mean()
    return 100 * (f(X1) - f(X0))


def kappa(a, b):
    a = np.asarray(a, int); b = np.asarray(b, int)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return (po - pe) / (1 - pe), po, pe


def cochran_q(M):
    M = np.asarray(M, int); k = M.shape[1]
    C = M.sum(0); R = M.sum(1); N = M.sum()
    Q = (k - 1) * (k * (C ** 2).sum() - N ** 2) / (k * N - (R ** 2).sum())
    return Q, chi2.sf(Q, k - 1)


def mcnemar_exact(b, c):
    return min(1.0, 2 * binom.cdf(min(b, c), b + c, 0.5))


# ---------------------------------------------------------------- cohort flow
x0 = pd.ExcelFile(ROOT + '全部肠旋转不良数据.xlsx')
F['db_children'] = x0.parse('病案首页基本信息')['科研患者编号'].nunique()
opsall = x0.parse('住院病历手术记录')
F['ops_all_records'] = len(opsall); F['ops_all_children'] = opsall['科研患者编号'].nunique()
ops0 = pd.read_excel(ROOT + '诊断效能_手术确诊队列_465例.xlsx', sheet_name='手术记录明细_503条')
F['ops_sel_records'] = len(ops0); F['ops_sel_children'] = ops0['科研患者编号'].nunique()
F['not_eligible_records'] = F['ops_all_records'] - F['ops_sel_records']
F['not_eligible_children'] = F['ops_all_children'] - F['ops_sel_children']
s1 = pd.read_excel('review_returns/审稿核对表_S1-S3_已填.xlsx', sheet_name='S1_锚定手术判定')
F['s1_reviewed'] = len(s1)
F['s1_prior_ladd'] = int(s1['筛出原因'].str.startswith('有既往旋转不良手术史').sum())
F['s1_no_term'] = F['s1_reviewed'] - F['s1_prior_ladd']
vc = s1['【填】判定'].value_counts()
F['s1_keep'] = int(vc['本次手术确认肠旋转不良（保留）']); F['s1_notconf'] = int(vc['非本次手术确认（排除）'])
F['s1_reop'] = int(vc['复发再次手术（单独讨论）']); F['excluded'] = F['s1_notconf'] + F['s1_reop']
excl_ids = set(REV.loc[REV['kind'] == 'child', '科研患者编号'])
F['excluded_with_index'] = len(excl_ids & set(pd.read_excel(ROOT + '诊断效能_逐患者矩阵_当前版v3.xlsx')['科研患者编号']))
s2 = pd.read_excel('review_returns/审稿核对表_S1-S3_已填.xlsx', sheet_name='S2_术前时间核对')
F['s2_same_day'] = int((s2['类型'] == '手术当日').sum())
F['s2_over7'] = int((s2['类型'] != '手术当日').sum())
F['s2_max_gap'] = int(s2['类型'].str.extract(r'(\d+)')[0].dropna().astype(int).max())
F['s2_postop'] = int((s2['【填】判定'] == '术后（剔除）').sum())
F['s2_unrelated'] = int(s2['【填】判定'].str.startswith('排除').sum())
F['s2_undetermined'] = int((s2['【填】判定'] == '无法判断').sum())
rr = REV[REV['kind'] == 'report']
F['reports_removed_in_cohort'] = int((~rr['科研患者编号'].isin(excl_ids)).sum())
F['cohort'] = len(coh); F['cohort_records'] = len(ops)
F['imaged'] = mat['科研患者编号'].nunique(); F['none'] = F['cohort'] - F['imaged']
for m, c in [('UGI', 'UGI_detected'), ('CT', 'CT_detected'), ('US', 'US_detected')]:
    F['n_' + m] = int(mat[c].notna().sum()); F['k_' + m] = int(mat[c].sum())
F['all_three'] = int(mat[['UGI_detected', 'CT_detected', 'US_detected']].notna().all(axis=1).sum())
F['index_exams'] = len(IX)
rep_ = rep.copy(); rep_['day'] = rep_['检查时间'].dt.normalize()
first_ = rep_.sort_values('gap').groupby(['科研患者编号', 'mod']).first().reset_index()[['科研患者编号', 'mod', 'day']]
mm = rep_.merge(first_, on=['科研患者编号', 'mod'], suffixes=('', '_ix'))
F['eligible_reports'] = len(rep_); F['reports_in_index'] = int((mm['day'] == mm['day_ix']).sum())
F['earlier_reports'] = F['eligible_reports'] - F['reports_in_index']
F['neonates'] = int(pat['neonate'].sum()); F['volvulus'] = int(pat['volvulus'].sum())
F['no_volvulus'] = F['cohort'] - F['volvulus']
F['study_months'] = (2026 - 2012) * 12 + (6 - 12) + 1   # December 2012 to June 2026 inclusive
A55 = json.load(open('a55b.json'))
F.update({'a55_' + k: v for k, v in A55.items()})

# ---------------------------------------------------------------- Table 1
adm = pd.concat([x0.parse('儿科入院记录'), x0.parse('新生儿科入院记录')], ignore_index=True)
adm = adm[adm['科研患者编号'].isin(set(coh['科研患者编号']))]
for c in ['主诉', '现病史', '病史小结', '初步诊断']:
    adm[c] = adm[c].fillna('').astype(str) if c in adm else ''
txt_adm = (adm['主诉'] + ' ' + adm['现病史'] + ' ' + adm['病史小结'] + ' ' + adm['初步诊断']).groupby(adm['科研患者编号']).apply(' '.join)
FEAT = {'vomit': r'呕吐|吐奶|呕奶', 'bilious': r'胆汁|黄绿|绿色液|草绿', 'distension': r'腹胀',
        'bloody_stool': r'血便|便血|果酱', 'abd_pain': r'腹痛', 'shock': r'休克|循环衰竭|面色苍白|皮肤花纹'}
P1 = pat.set_index('科研患者编号').copy()
for k, rx in FEAT.items():
    P1[k] = txt_adm.reindex(P1.index).fillna('').str.contains(rx, regex=True)


# gastrointestinal symptoms for 1 month or longer: a threshold test on each clause of
# the chief complaint of the operative admission (written apart from clin.py's day count)
def long_gi(cc):
    for cl in re.split(r'[，,；;。\s]+', cc):
        if not re.search(r'呕|吐|腹痛|腹胀|腹部不适|便血|血便|哭吵|哭闹|体重不增|便秘|纳差|拒奶|腹泻', cl):
            continue
        if re.search(r'产检|产前|孕期|胎儿|发现|提示|术后|CT|B超|彩超|检查|立位片|造影', cl):
            continue
        if re.search(r'(\d+|[一二两三四五六七八九十数]+)\s*余?\s*个?\s*月|年', cl):
            return True
        if any(int(n) * (7 if u == '周' else 1) >= 30 for n, u in re.findall(r'(\d+)\s*余?\s*(天|日|周)', cl)):
            return True
    return False


cc_op = adm.merge(pat[['科研患者编号', '科研就诊编号']], on=['科研患者编号', '科研就诊编号']).set_index('科研患者编号')['主诉']
assert cc_op.index.is_unique and len(cc_op) == len(P1)
P1['symptoms_1m'] = cc_op.reindex(P1.index).map(long_gi)
FEAT['symptoms_1m'] = None
P1['older'] = P1['age_days'] > 365
GROUPS = {'All': set(P1.index), 'UGI': set(mat.loc[mat['UGI_detected'].notna(), '科研患者编号']),
          'CT': set(mat.loc[mat['CT_detected'].notna(), '科研患者编号']),
          'US': set(mat.loc[mat['US_detected'].notna(), '科研患者编号'])}
GROUPS['none'] = GROUPS['All'] - set(mat['科研患者编号'])
T1 = {}
for g, ids_ in GROUPS.items():
    d = P1.loc[sorted(ids_)]
    T1[g] = {'n': len(d), 'age': (d['age_days'].median(), d['age_days'].quantile(.25), d['age_days'].quantile(.75))}
    for k in ['neonate', 'older', 'male', 'era_late', 'volvulus'] + list(FEAT):
        T1[g][k] = int(d[k].sum())
F['T1'] = T1
F['us_rate_early'] = (int(P1.loc[sorted(GROUPS['US'])]['era_late'].eq(False).sum()), int((~P1['era_late']).sum()))
F['us_rate_late'] = (int(P1.loc[sorted(GROUPS['US'])]['era_late'].sum()), int(P1['era_late'].sum()))
F['us_given_volv'] = (len(GROUPS['US'] & set(P1.index[P1['volvulus']])), int(P1['volvulus'].sum()))
F['us_given_novolv'] = (len(GROUPS['US'] & set(P1.index[~P1['volvulus']])), int((~P1['volvulus']).sum()))

# ---------------------------------------------------------------- Table 2
POSS = r'可疑|可能|\?|？|不除外|不排除|待排|待除外|建议.{0,10}(除外|排除|进一步)|似'
PROB = r'多考虑|首先考虑|考虑|倾向|符合.{0,6}表现'
def tier(s):
    if re.search(POSS, s): return 'possible'
    if re.search(PROB, s): return 'probable'
    return 'definite'
def names_mal(t):
    for c in re.split(r'[。；;\n]+', str(t)):
        for m_ in re.finditer(r'旋转不良', c):
            if not re.search(r'未见|未探及|未显示|未发现|无明显|不明显|不考虑', c[max(0, m_.start() - 12):m_.start()]):
                return True
    return False
EP = IX.merge(long[['科研患者编号', 'mod', 'detected']], on=['科研患者编号', 'mod'])
assert len(EP) == len(IX)
EP['tier'] = EP['concl'].fillna('').astype(str).map(tier)
EP['named'] = EP['concl'].map(names_mal)
T2 = {}
for m in ['UGI', 'CT', 'US']:
    d = EP[EP['mod'] == m]; pos = d[d['detected'] == 1]
    t = pos['tier'].value_counts()
    T2[m] = {'k': int(d['detected'].sum()), 'n': len(d), 'def': int(t.get('definite', 0)),
             'prob': int(t.get('probable', 0)), 'poss': int(t.get('possible', 0)),
             'named': int(((d['detected'] == 1) & d['named']).sum())}
ct = EP[EP['mod'] == 'CT']; enh = ct['名称'].astype(str).str.contains('增强')
T2['CT_enh'] = (int(ct.loc[enh, 'detected'].sum()), int(enh.sum()))
T2['CT_unenh'] = (int(ct.loc[~enh, 'detected'].sum()), int((~enh).sum()))
# the tiers as the pipeline computed them (closest single report), for the comparison
old = pd.read_csv('pos_tier.csv')
T2['single_report_tiers'] = {m: old[old['mod'] == m]['tier'].value_counts().to_dict() for m in ['UGI', 'CT', 'US']}
F['T2'] = T2

# ---------------------------------------------------------------- Table 3
U = u.copy()
for k in ['vessel_us', 'gi_us', 'pyloric', 'bedside']:
    U[k] = U[k].astype(bool)
T3 = {}
for k in ['d3_or_djj', 'duodenum', 'sma_smv', 'inversion', 'fluid', 'dynamic', 'compress', 'cecum', 'doppler',
          'whirl_pos', 'gas_limit', 'vessel_us', 'gi_us', 'pyloric', 'bedside']:
    s = U[k].astype(bool)
    T3[k] = {'n': int(s.sum()), 'early': int((s & (U['late'] == 0)).sum()), 'late': int((s & (U['late'] == 1)).sum()),
             'det_yes': (int(U.loc[s, 'det'].sum()), int(s.sum())), 'det_no': (int(U.loc[~s, 'det'].sum()), int((~s).sum()))}
F['T3'] = T3; F['n_US_early'] = int((U['late'] == 0).sum()); F['n_US_late'] = int((U['late'] == 1).sum())
F['ovl'] = {'gi_vessel': int((U.gi_us & U.vessel_us).sum()), 'gi_pyloric': int((U.gi_us & U.pyloric).sum()),
            'vessel_pyloric': int((U.vessel_us & U.pyloric).sum()), 'any': int((U.gi_us | U.vessel_us | U.pyloric).sum())}
F['whirl_named_mal'] = int((U['whirl_pos'] & U['concl'].map(names_mal)).sum())
V = U.merge(pat[['科研患者编号']], on='科研患者编号')
F['whirl_in_volv'] = (int((U['whirl_pos'] & U['volvulus'].astype(bool)).sum()), int(U['volvulus'].astype(bool).sum()))
d3 = U[U['d3_or_djj']]
F['d3_years'] = sorted(pd.to_datetime(d3['检查时间']).dt.year.tolist())
F['us_pos_volvulus_only'] = int(((U['det'] == 1) & ~U['concl'].map(names_mal) & U['concl'].astype(str).str.contains('扭转')).sum())

# ---------------------------------------------------------------- reader agreement
A = pd.read_excel('review_returns/审稿核对表_S1-S3_已填.xlsx', sheet_name='S3_超声报告阅读_甲')
B = pd.read_excel('review_returns/S3超声报告阅读_阅读者乙_已填.xlsx', sheet_name='S3_超声报告阅读_乙')
items = list(A.columns[5:17])
KAP = {}
for c in items:
    a = (A[c] == '是').astype(int); b = (B[c] == '是').astype(int)
    KAP[c] = {'A': int(a.sum()), 'B': int(b.sum()), 'agree': int((a == b).sum()), 'kappa': kappa(a, b)[0]}
F['KAP'] = KAP; F['cells'] = len(A) * len(items)
F['cells_agree'] = sum(v['agree'] for v in KAP.values())
F['episodes_disagree'] = int(sum(((A[c] != B[c])) for c in items).astype(bool).sum())
sv = pd.read_excel(ROOT + '诊断效能_核对清单_精简版.xlsx', sheet_name='抽查验证')
ka, po, _ = kappa((sv['机判'] == '阳').astype(int), (sv['医师判读(阳/阴)'] == '阳').astype(int))
n_sv = len(sv)
se_k = math.sqrt(po * (1 - po) / (n_sv * (1 - _) ** 2))
F['val'] = {'n': n_sv, 'agree': int((sv['机判'] == sv['医师判读(阳/阴)']).sum()), 'kappa': ka,
            'ci': (ka - 1.96 * se_k, min(1.0, ka + 1.96 * se_k)),
            'by_mod': {m: (int((g['机判'] == g['医师判读(阳/阴)']).sum()), len(g)) for m, g in sv.groupby('模态')}}
tg = pd.read_excel(ROOT + '诊断效能_核对清单_精简版.xlsx', sheet_name='潜在漏判')
tgu = tg.drop_duplicates(['科研患者编号', '模态', '检查时间', '报告名称'])
F['targeted'] = {'rows': len(tg), 'unique': len(tgu), 'undercalls': int((tgu['医师判读(阳/阴)'] == '阳').sum())}
nine = pd.read_excel(ROOT + '待核标签清单_9例_已裁定.xlsx', sheet_name='待核清单')
F['nine'] = len(nine)

# ---------------------------------------------------------------- Table 4 and temporal
T4 = {}
for m in ['UGI', 'CT', 'US']:
    d = EP[EP['mod'] == m].merge(pat[['科研患者编号', 'era_late', 'op_year']], on='科研患者编号')
    d['late'] = d['era_late'].astype(int); d['det'] = d['detected'].astype(int)
    d['enh'] = d['名称'].astype(str).str.contains('增强').astype(int)
    d['ves'] = d['名称'].astype(str).str.contains('腹部大血管').astype(int)
    y = d['det'].to_numpy(float)
    X1 = np.column_stack([np.ones(len(d)), d['late']])
    b1, s1_ = irls(X1, y)
    r = {'early': (int(d.loc[d.late == 0, 'det'].sum()), int((d.late == 0).sum())),
         'late': (int(d.loc[d.late == 1, 'det'].sum()), int((d.late == 1).sum())),
         'or_crude': orci(b1, s1_, 1), 'ame_crude': ame(b1, X1)}
    cv = {'CT': 'enh', 'US': 'ves'}.get(m)
    if cv:
        X2 = np.column_stack([np.ones(len(d)), d['late'], d[cv]])
        b2, s2_ = irls(X2, y)
        r.update({'or_adj': orci(b2, s2_, 1), 'or_cov': orci(b2, s2_, 2), 'ame_adj': ame(b2, X2)})
    T4[m] = r
    if m == 'US':
        BND = {}
        for cut in [2019, 2020, 2021, 2022]:
            dd = d.copy(); dd['late'] = (dd['op_year'] >= cut).astype(int)
            Xa = np.column_stack([np.ones(len(dd)), dd['late']]); ba, sa = irls(Xa, y)
            Xb = np.column_stack([np.ones(len(dd)), dd['late'], dd['ves']]); bb, sb = irls(Xb, y)
            BND[cut] = {'n': (int((dd.late == 0).sum()), int((dd.late == 1).sum())),
                        'k': (int(dd.loc[dd.late == 0, 'det'].sum()), int(dd.loc[dd.late == 1, 'det'].sum())),
                        'or_crude': orci(ba, sa, 1), 'or_adj': orci(bb, sb, 1), 'or_ves': orci(bb, sb, 2),
                        'ame': (ame(ba, Xa), ame(bb, Xb))}
        F['BND'] = BND
        F['ves_share'] = ((int(d.loc[d.late == 0, 'ves'].sum()), int((d.late == 0).sum())),
                          (int(d.loc[d.late == 1, 'ves'].sum()), int((d.late == 1).sum())))
F['T4'] = T4
F['AME_boot'] = json.load(open('addstats.json'))['AME']

# ---------------------------------------------------------------- paired subgroup
pid = sorted(GROUPS['UGI'] & GROUPS['CT'] & GROUPS['US'])
M3 = mat.set_index('科研患者编号').loc[pid, ['UGI_detected', 'CT_detected', 'US_detected', 'US_whirlpool']].astype(int)
tt = idx[idx['科研患者编号'].isin(pid)].pivot_table(index='科研患者编号', columns='mod', values='检查时间', aggfunc='first')
span = ((tt.max(axis=1) - tt.min(axis=1)).dt.total_seconds() / 86400).reindex(pid)
PS = {}
for lab, sel in [('all', span.index), ('48h', span.index[span <= 2]), ('24h', span.index[span <= 1])]:
    d = M3.loc[sel]
    Q, pQ = cochran_q(d[['UGI_detected', 'CT_detected', 'US_detected']].values)
    def mc(a, b):
        bb = int(((d[a] == 1) & (d[b] == 0)).sum()); cc = int(((d[a] == 0) & (d[b] == 1)).sum())
        return bb, cc, mcnemar_exact(bb, cc)
    PS[lab] = {'n': len(d), 'UGI': int(d.UGI_detected.sum()), 'US': int(d.US_detected.sum()), 'CT': int(d.CT_detected.sum()),
               'WH': int(d.US_whirlpool.sum()), 'Q': (Q, pQ),
               'ugi_ct': mc('UGI_detected', 'CT_detected'), 'ugi_us': mc('UGI_detected', 'US_detected'),
               'ct_us': mc('CT_detected', 'US_detected')}
F['PS'] = PS
F['span'] = (span.median(), span.quantile(.25), span.quantile(.75))
oth = sorted(set(mat['科研患者编号']) - set(pid))
F['paired_chars'] = {g: (P1.loc[s, 'volvulus'].mean() * 100, P1.loc[s, 'neonate'].mean() * 100, P1.loc[s, 'era_late'].mean() * 100, len(s))
                     for g, s in [('three', pid), ('other', oth)]}
F['PAIR_boot'] = json.load(open('addstats.json'))['PAIR']

# ---------------------------------------------------------------- pathway position (order)
mult = idx.groupby('科研患者编号')['mod'].nunique()
mult_ids = set(mult[mult > 1].index)
last = idx[idx['科研患者编号'].isin(mult_ids)].sort_values('检查时间').groupby('科研患者编号').last()['mod']
EPd = EP.set_index(['科研患者编号', 'mod'])['detected']
POS = {}
for m in ['UGI', 'CT', 'US']:
    had = [p for p in mult_ids if (p, m) in EPd.index]
    is_last = [p for p in had if last.get(p) == m]
    not_last = [p for p in had if last.get(p) != m]
    POS[m] = {'had': len(had), 'last': len(is_last),
              'det_last': np.mean([EPd[(p, m)] for p in is_last]) * 100 if is_last else float('nan'),
              'det_earlier': np.mean([EPd[(p, m)] for p in not_last]) * 100 if not_last else float('nan')}
F['POS'] = POS

# ---------------------------------------------------------------- strata, volvulus sign, definitions
P1['agegrp'] = pd.cut(P1['age_days'], [-1, 28, 365, 1e9], labels=['neo', 'inf', 'old'])
ST = {}
for m in ['UGI', 'CT', 'US']:
    d = EP[EP['mod'] == m].set_index('科研患者编号')
    d = d.join(P1[['volvulus', 'agegrp']])
    for lab, sel in [('volv', d['volvulus']), ('novolv', ~d['volvulus']), ('neo', d['agegrp'] == 'neo'),
                     ('inf', d['agegrp'] == 'inf'), ('old', d['agegrp'] == 'old')]:
        ST[(m, lab)] = (int(d.loc[sel, 'detected'].sum()), int(sel.sum()))
F['ST'] = ST
rot = P1['rot_deg']
defA = P1['volvulus'] & ~(rot.notna() & (rot < 360))
defB = P1['volvulus'] & (rot.notna() & (rot >= 360))
usid = GROUPS['US']; wp = U.set_index('科研患者编号')['whirl_pos']
VD = {}
for lab, mask in [('primary', P1['volvulus']), ('A', defA), ('B', defB)]:
    ids_m = set(mask[mask].index)
    VD[lab] = (int(mask.sum()), len(ids_m & usid), int(wp.reindex(sorted(ids_m & usid)).sum()))
F['VD'] = VD
F['rot'] = {'stated': int((P1['volvulus'] & rot.notna()).sum()), 'ge360': int((P1['volvulus'] & (rot >= 360)).sum()),
            'lt360': int((P1['volvulus'] & (rot < 360)).sum())}

# ---------------------------------------------------------------- classifier agreement
import importlib.util
spec = importlib.util.spec_from_file_location('sc', ROOT + 'Supplement_1_classifier.py')
sc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
EP['ref'] = [sc.classify(str(c), m)[0] for c, m in zip(EP['concl'], EP['mod'])]
F['CLS'] = {m: (int((g['ref'] == g['detected']).sum()), len(g), int(((g['ref'] == 0) & (g['detected'] == 1)).sum()),
                int(((g['ref'] == 1) & (g['detected'] == 0)).sum())) for m, g in EP.groupby('mod')}

# ---------------------------------------------------------------- GEE (same software)
import statsmodels.api as sm, statsmodels.formula.api as smf
L = long.copy(); L['modality'] = pd.Categorical(L['mod'], categories=['UGI', 'CT', 'US'])
L['agegrp'] = pd.cut(L['age_days'], [-1, 28, 365, 1e9], labels=['neonate', '29d-1y', '>1y'])
L = L.sort_values('科研患者编号')
def gee(f):
    return smf.gee(f, '科研患者编号', data=L, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
g1 = gee('detected ~ C(modality)'); g2 = gee('detected ~ C(modality) + era_late + C(agegrp, Treatment(reference="neonate"))')
def gor(m, k):
    ci = m.conf_int().loc[k]; return (math.exp(m.params[k]), math.exp(ci[0]), math.exp(ci[1]), m.pvalues[k])
F['GEE'] = {'ct_u': gor(g1, 'C(modality)[T.CT]'), 'us_u': gor(g1, 'C(modality)[T.US]'),
            'ct_a': gor(g2, 'C(modality)[T.CT]'), 'us_a': gor(g2, 'C(modality)[T.US]'),
            'era': gor(g2, 'era_late[T.True]'),
            'inf': gor(g2, 'C(agegrp, Treatment(reference="neonate"))[T.29d-1y]'),
            'old': gor(g2, 'C(agegrp, Treatment(reference="neonate"))[T.>1y]')}

# ---------------------------------------------------------------- Firth closed form
k1 = ST[('US', 'volv')]; k0 = ST[('US', 'novolv')]
F['firth_or'] = ((k1[0] + .5) * (k0[1] - k0[0] + .5)) / ((k1[1] - k1[0] + .5) * (k0[0] + .5))
F['firth_cells'] = (k1[0] + .5, k0[1] - k0[0] + .5, k1[1] - k1[0] + .5, k0[0] + .5)
F['S13'] = json.load(open('or_add.json'))['S13']

# ---------------------------------------------------------------- CT / UGI content (Supplement Table S8)
F['S8'] = json.load(open('or3_pooled.json'))['S3']
F['S2b'] = {m: (int(r[1].split('/')[0]), int(r[1].split('/')[1])) for m, r in
            zip(['UGI', 'US', 'CT'], json.load(open('volsign2.json'))['S2b'][1:])}
F['S5'] = json.load(open('or_sens.json'))['S5']
F['software'] = {'python': __import__('sys').version.split()[0], 'statsmodels': sm.__version__,
                 'scipy': __import__('scipy').__version__}
