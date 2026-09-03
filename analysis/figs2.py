exec(open('core.py').read())
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportion_confint as pci
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
OUT='/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
C={'UGI':'#B22222','CT':'#E08214','US':'#2C7FB8','US2':'#7FC0E8'}
# ---- Figure 2 ----
p=mat[mat[['US_detected','CT_detected','UGI_detected']].notna().all(axis=1)].copy()
pid=set(p['科研患者编号'])
tt=idx[idx['科研患者编号'].isin(pid)].pivot_table(index='科研患者编号',columns='mod',values='检查时间',aggfunc='first')
p=p.merge(((tt.max(axis=1)-tt.min(axis=1)).dt.total_seconds()/86400).rename('span'),on='科研患者编号')
panels=[('All 59 children',p),('All three within 48 h',p[p['span']<=2]),('All three within 24 h',p[p['span']<=1])]
series=[('UGI contrast series','UGI_detected',C['UGI']),('Gastrointestinal ultrasound','US_detected',C['US']),
        ('Abdominal CT','CT_detected',C['CT']),('Ultrasound whirlpool sign','US_whirlpool',C['US2'])]
fig,ax=plt.subplots(figsize=(11.5,5.8))
w=0.2; xs=np.arange(len(panels))
for j,(lab,col,c) in enumerate(series):
    vals=[];errs=[[],[]];ann=[]
    for _,d in panels:
        k=int(d[col].sum()); n=len(d); r=k/n*100; lo,hi=pci(k,n,method='wilson')
        vals.append(r); errs[0].append(r-lo*100); errs[1].append(hi*100-r); ann.append(f'{k}/{n}')
    pos=xs+(j-1.5)*w
    ax.bar(pos,vals,w*0.92,color=c,label=lab,edgecolor='white')
    ax.errorbar(pos,vals,yerr=errs,fmt='none',ecolor='#444',capsize=3,lw=1)
    for ii,(xi,v,a) in enumerate(zip(pos,vals,ann)):
        ax.text(xi,v+errs[1][ii]+2.0,f'{v:.0f}%\n{a}',ha='center',fontsize=9)
ax.set_xticks(xs); ax.set_xticklabels([f'{l}\n(n = {len(d)})' for l,d in panels],fontsize=11)
ax.set_ylim(0,116); ax.set_ylabel('Report-level detection (%), Wilson 95% CI')
ax.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(0.5,1.20),fontsize=10)
ax.grid(axis='y',color='#e2e2e2'); ax.set_axisbelow(True)
ax.text(0.5,-0.235,'Selected subgroup assembled by diagnostic uncertainty (97% volvulus, 83% neonates, 63% from 2019-2026).\nThis is not a population-level comparison of test accuracy.',
        transform=ax.transAxes,ha='center',fontsize=9.6,style='italic',color='#8a1c1c')
plt.tight_layout(); plt.savefig(OUT+'FigS1_paired_subgroup.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()

# ---- Figure 3 (ultrasound report audit) ----
u=pd.read_csv('us_audit4.csv')
items=[('Third portion of duodenum / DJ junction','d3_or_djj'),('Explicit vessel inversion','inversion'),
       ('Graded compression','compress'),('Enteric fluid administered','fluid'),
       ('Dynamic assessment','dynamic'),('Caecal position','cecum'),
       ('Duodenum mentioned at all','duodenum'),('SMA-SMV relationship','sma_smv'),
       ('Bowel gas limiting study','gas_limit'),('Whirlpool sign reported','whirl_pos')]
fig,axes=plt.subplots(1,2,figsize=(15.6,6.0),gridspec_kw={'width_ratios':[1.12,1]})
ax=axes[0]
vals=[u[k].astype(bool).mean()*100 for _,k in items]; ns=[int(u[k].astype(bool).sum()) for _,k in items]
y=np.arange(len(items))[::-1]
cols=['#B22222' if v<10 else '#2C7FB8' for v in vals]
ax.barh(y,vals,color=cols,height=0.62)
for yi,v,n in zip(y,vals,ns):
    ax.text(max(v,0)+1.2,yi,f'{n}/119  ({v:.1f}%)',va='center',fontsize=10)
ax.set_yticks(y); ax.set_yticklabels([l for l,_ in items],fontsize=10.5)
ax.set_xlim(0,72); ax.set_xlabel('Ultrasound examinations documenting the element (%)')
ax.set_title('a  What the 119 routine ultrasound examinations documented',fontsize=11.5,loc='left',fontweight='bold')
ax.grid(axis='x',color='#e8e8e8'); ax.set_axisbelow(True)
ax=axes[1]
groups=[('Whirlpool\nreported','whirl_pos',True),('Whirlpool\nnot reported','whirl_pos',False),
        ('Vessels\naddressed','sma_smv',True),('Vessels\nnot addressed','sma_smv',False),
        ('Great-vessel\nsession','vessel_us',True),('No great-\nvessel session','vessel_us',False)]
vals=[];ann=[];err=[[],[]]
for lab,k,v in groups:
    s2=u[u[k].astype(bool)==v]; kk=int(s2['det'].sum()); n=len(s2); r=kk/n*100
    lo,hi=pci(kk,n,method='wilson'); vals.append(r); err[0].append(r-lo*100); err[1].append(hi*100-r); ann.append(f'{kk}/{n}')
x=np.arange(len(groups)); cc=['#2C7FB8','#B22222']*3
ax.bar(x,vals,0.62,color=cc,edgecolor='white')
ax.errorbar(x,vals,yerr=err,fmt='none',ecolor='#444',capsize=3,lw=1)
for xi,v,a,eu in zip(x,vals,ann,err[1]): ax.text(xi,v+eu+3,f'{v:.0f}%\n{a}',ha='center',fontsize=9.5)
ax.set_xticks(x); ax.set_xticklabels([g[0] for g in groups],fontsize=9.0); ax.tick_params(axis='x',pad=4)
ax.set_ylim(0,118); ax.set_ylabel('Report-level detection (%)')
ax.set_title('b  Detection conditional on documented content',fontsize=11.5,loc='left',fontweight='bold')
ax.grid(axis='y',color='#e8e8e8'); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(OUT+'Fig3_ultrasound_report_audit.png',dpi=300,bbox_inches='tight',facecolor='white'); plt.close()
print('Fig3 rebuilt')
