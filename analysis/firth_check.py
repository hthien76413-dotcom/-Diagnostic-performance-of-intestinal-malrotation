# -*- coding: utf-8 -*-
"""Cross-check the in-house Firth fit against an independent implementation
(firthlogist, which reports penalised likelihood-ratio intervals as R's logistf does)."""
exec(open('usaudit4.py').read().split('ROWS=')[0])
import numpy as np
from firthlogist import FirthLogisticRegression
# newer scikit-learn removed BaseEstimator._validate_data; restore a minimal shim
if not hasattr(FirthLogisticRegression,'_validate_data'):
    from sklearn.utils.validation import check_X_y
    def _validate_data(self,X,y=None,**kw):
        kw.pop('ensure_min_samples',None); kw.pop('dtype',None)
        return check_X_y(np.asarray(X,float),np.asarray(y))
    FirthLogisticRegression._validate_data=_validate_data
from firth import firth_logit

us=IX[IX['mod']=='US'].merge(mat[['科研患者编号','US_detected']],on='科研患者编号',how='left') \
                      .merge(pat[['科研患者编号','volvulus']],on='科研患者编号',how='left')
y=us['US_detected'].astype(int).values
V=us['volvulus'].astype(int).values.reshape(-1,1)
print('data: volvulus %d/%d positive, no volvulus %d/%d positive'%(
      y[V.ravel()==1].sum(),(V.ravel()==1).sum(),y[V.ravel()==0].sum(),(V.ravel()==0).sum()))

print('\n--- in-house firth.py (Wald interval) ---')
X=np.column_stack([np.ones(len(y)),V.ravel()])
b,se=firth_logit(X,y.astype(float))
print(f'  beta_volvulus = {b[1]:.4f}   SE = {se[1]:.4f}')
print(f'  OR = {np.exp(b[1]):.2f}  Wald 95% CI {np.exp(b[1]-1.96*se[1]):.2f} to {np.exp(b[1]+1.96*se[1]):.1f}')

print('\n--- firthlogist (independent; profile penalised likelihood interval) ---')
f=FirthLogisticRegression()
f.fit(V,y)
print(f'  beta_volvulus = {f.coef_[0]:.4f}   intercept = {f.intercept_:.4f}')
lo,hi=f.ci_[0]
print(f'  OR = {np.exp(f.coef_[0]):.2f}  profile 95% CI {np.exp(lo):.2f} to {np.exp(hi):.1f}')
print(f'  penalised likelihood-ratio p = {f.pvals_[0]:.4f}')
print(f'\n  coefficient agreement: |difference| = {abs(b[1]-f.coef_[0]):.6f}')
