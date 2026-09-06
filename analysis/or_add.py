# -*- coding: utf-8 -*-
"""Assemble or_add.json (Online Resource 2, Tables S2b and S11-S13).

Everything here is read from the analysis outputs or refitted on the spot, so
the supplement cannot drift away from the scripts that produced it.
Run after addstats.py and volsign2.py.
"""
exec(open('core.py').read())
import json, statsmodels.api as sm, statsmodels.formula.api as smf

A = json.load(open('addstats.json'))
V = json.load(open('volsign2.json'))

def pp(v, ci):
    return f'{v:+.1f} ({ci[0]:+.1f} to {ci[1]:+.1f})'

S11 = [['Modality and model',
        'Average marginal effect of later era, percentage points (95% CI)']]
S11 += [[k, pp(v[0], v[1])] for k, v in A['AME'].items()]

S12 = [['Comparison (n=59)', 'Detection', 'Difference, percentage points (95% CI)',
        'Discordant pairs', 'Exact McNemar p']] + A['PAIR']

# modality x volvulus interaction where it is estimable (UGI vs CT only)
long['modality'] = pd.Categorical(long['mod'], categories=['UGI', 'CT', 'US'])
sub = long[long['mod'].isin(['UGI', 'CT'])].sort_values('科研患者编号').copy()
sub['modality'] = pd.Categorical(sub['mod'], categories=['UGI', 'CT'])
m = smf.gee('detected ~ C(modality)*volvulus + era_late + neonate', '科研患者编号',
            data=sub, family=sm.families.Binomial(),
            cov_struct=sm.cov_struct.Exchangeable()).fit()
t = 'C(modality)[T.CT]:volvulus[T.True]'
ci = m.conf_int().loc[t]
gee_int = (f'CT x volvulus odds ratio {np.exp(m.params[t]):.2f} '
           f'({np.exp(ci[0]):.2f}–{np.exp(ci[1]):.2f})', f'{m.pvalues[t]:.3f}')

orv, plo, phi, pval = A['FIRTH_PROFILE']

S13 = [['Analysis', 'Estimate (95% CI)', 'p'],
       ['Modality x volvulus interaction, upper gastrointestinal series vs CT '
        '(GEE; estimable)', gee_int[0], gee_int[1]],
       ['Modality x volvulus interaction including ultrasound (GEE)',
        'Not estimable (complete separation)', '–'],
       ['Ultrasound detection given midgut volvulus, Firth penalised logistic',
        f'Odds ratio {orv:.1f} ({plo:.2f}–{phi:.0f}, profile penalised likelihood)',
        f'{pval:.3f}'],
       ['Era x examination-content interaction, ultrasound', A['INT'][0][1], A['INT'][0][2]],
       ['Era x examination-content interaction, CT',        A['INT'][1][1], A['INT'][1][2]]]

json.dump({'S11': S11, 'S12': S12, 'S13': S13, 'S2b': V['S2b']},
          open('or_add.json', 'w'), ensure_ascii=False, indent=1)
for T in (S11, S12, S13):
    print(); [print(' | '.join(map(str, r))) for r in T]
