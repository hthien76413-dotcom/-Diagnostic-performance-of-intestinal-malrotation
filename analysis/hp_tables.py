# -*- coding: utf-8 -*-
"""Tables S16 to S19 of Supplement 2, from hp_sens.json (written by hp_sens.py).
Writes hp_tables.json in the list-of-rows format the supplement builder reads."""
import json
from statsmodels.stats.proportion import proportion_confint as pci

H = json.load(open('hp_sens.json'))
M = '−'   # true minus sign


def sg(v, nd=1, plus=False):
    s = f'{abs(v):.{nd}f}'
    if v < 0 and round(abs(v), nd) != 0: return M + s
    return ('+' if plus else '') + s


def pp(v, lo, hi):
    return f'{sg(v, plus=True)} ({sg(lo, plus=True)} to {sg(hi, plus=True)})'


def orf(t):
    return f'{t[0]:.2f} ({t[1]:.2f}–{t[2]:.2f})'


def nn(k, n):
    return f'{k}/{n} ({100 * k / n:.1f})'


def wcell(k, n):
    lo, hi = pci(k, n, method='wilson')
    return f'{k} ({100 * k / n:.1f}; {100 * lo:.1f}–{100 * hi:.1f})'


MODS = ['UGI', 'CT', 'US']
DEFS = ['primary', 'named', 'strict', 'ref']
AB = H['AB']

# ---- Table S16: outcome definitions, detection and adjusted odds ratios
S16 = [['Outcome definition', 'UGI series, n/N (%)', 'CT, n/N (%)', 'Ultrasound, n/N (%)',
        'CT vs UGI series, adjusted OR (95% CI)', 'Ultrasound vs UGI series, adjusted OR (95% CI)',
        'Ultrasound vs CT, adjusted OR (95% CI)']]
for k in DEFS:
    r = AB[k]
    S16.append([r['label']] + [nn(*r['rates'][m]) for m in MODS] +
               [orf(r['ors'][c]) for c in ('CT vs UGI', 'US vs UGI', 'US vs CT')])

# ---- Table S17: standardized detection and risk differences
S17 = [['Outcome definition', 'UGI series, % (95% CI)', 'CT, % (95% CI)', 'Ultrasound, % (95% CI)',
        'CT minus UGI series, percentage points (95% CI)', 'Ultrasound minus UGI series, percentage points (95% CI)',
        'Ultrasound minus CT, percentage points (95% CI)']]
for k in DEFS:
    r = AB[k]; st = r['std']; ci = r['ci']
    S17.append([r['label']] +
               [f"{st[m]:.1f} ({ci[m][0]:.1f}–{ci[m][1]:.1f})" for m in MODS] +
               [pp(st['CT'] - st['UGI'], *ci['CT−UGI']), pp(st['US'] - st['UGI'], *ci['US−UGI']),
                pp(st['US'] - st['CT'], *ci['US−CT'])])

# ---- Table S18: timing and index-unit definition
C = H['C']; I = C['interval']; U = C['units']; R = C['restricted']
S18 = [['Measure', 'UGI series', 'CT', 'Ultrasound']]
S18.append(['Index examinations, n'] + [str(I[m]['n']) for m in MODS])
S18.append(['Calendar days from index examination to operation, median (IQR)'] +
           [f"{I[m]['median']:.0f} ({I[m]['q1']:.0f}–{I[m]['q3']:.0f})" for m in MODS])
for lab, key in [('Same day, n (%)', 'd0'), ('1 day before, n (%)', 'd1'), ('2–7 days before, n (%)', 'd2_7'),
                 ('More than 7 days before, n (%)', 'd8')]:
    S18.append([lab] + [f"{I[m][key]} ({100 * I[m][key] / I[m]['n']:.1f})" for m in MODS])
S18.append(['Detection, final label, closest episode (primary), n/N (%)'] + [nn(U[m]['final'], U[m]['n']) for m in MODS])
S18.append(['Detection, conclusion-only classifier, closest episode, n/N (%)'] + [nn(U[m]['closest'], U[m]['n']) for m in MODS])
S18.append(['Detection, conclusion-only classifier, earliest episode, n/N (%)'] + [nn(U[m]['earliest'], U[m]['n']) for m in MODS])
S18.append(['Detection, conclusion-only classifier, any preoperative episode positive, n/N (%)'] + [nn(U[m]['anypos'], U[m]['n']) for m in MODS])
S18.append(['Children with more than one preoperative episode, n'] + [str(U[m]['n_multi']) for m in MODS])
r2 = R['le2']
S18.append(['Detection, final label, examinations within 2 days of operation, n/N (%)'] + [nn(*r2['rates'][m]) for m in MODS])
S18.append(['Adjusted OR vs UGI series, examinations within 2 days (95% CI)', '–', orf(r2['ors']['CT vs UGI']), orf(r2['ors']['US vs UGI'])])
S18.append(['Adjusted OR vs CT, examinations within 2 days (95% CI)', '–', '–', orf(r2['ors']['US vs CT'])])

# ---- Table S19: content documentation by booking category
S19 = [['Denominator', 'Examinations, n', 'D3 or duodenojejunal junction, n (%; 95% CI)',
        'Artery–vein relationship, n (%; 95% CI)', 'Enteric fluid, n (%; 95% CI)',
        'Whirlpool reported, n (%; 95% CI)', 'Positive report, n (%; 95% CI)']]
for d in H['D']:
    n = d['n']
    S19.append([d['label'], str(n), wcell(d['d3'], n), wcell(d['sma'], n), wcell(d['fluid'], n), wcell(d['whirl'], n), wcell(d['det'], n)])

json.dump({'S16': S16, 'S17': S17, 'S18': S18, 'S19': S19}, open('hp_tables.json', 'w'), ensure_ascii=False, indent=1)
for T in (S16, S17, S18, S19):
    for r in T: print(' | '.join(r))
    print()
