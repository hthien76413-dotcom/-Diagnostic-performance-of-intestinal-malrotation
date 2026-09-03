# -*- coding: utf-8 -*-
"""Firth penalised (Jeffreys-prior) logistic regression, with a validation check
against the ordinary MLE on data that are not separated."""
import numpy as np
def firth_logit(X, y, tol=1e-10, maxit=200):
    X=np.asarray(X,float); y=np.asarray(y,float); n,p=X.shape
    b=np.zeros(p)
    for _ in range(maxit):
        eta=X@b; mu=1/(1+np.exp(-eta)); w=mu*(1-mu)
        XW=X*w[:,None]; I=X.T@XW
        Iinv=np.linalg.pinv(I)
        h=np.einsum('ij,jk,ik->i',XW,Iinv,X)      # hat diagonal
        U=X.T@(y-mu+h*(0.5-mu))                   # penalised score
        step=Iinv@U
        # step halving
        t=1.0
        for _ in range(30):
            nb=b+t*step
            if np.all(np.isfinite(nb)) and np.max(np.abs(t*step))<10: break
            t/=2
        b=b+t*step
        if np.max(np.abs(t*step))<tol: break
    eta=X@b; mu=1/(1+np.exp(-eta)); w=mu*(1-mu)
    cov=np.linalg.pinv(X.T@(X*w[:,None]))
    se=np.sqrt(np.diag(cov))
    return b,se

if __name__=='__main__':
    import statsmodels.api as sm
    rng=np.random.default_rng(0)
    n=400; x=rng.normal(size=n); X=np.column_stack([np.ones(n),x])
    y=(rng.random(n) < 1/(1+np.exp(-(-0.4+0.8*x)))).astype(float)
    b,se=firth_logit(X,y)
    m=sm.Logit(y,X).fit(disp=0)
    print('validation on non-separated data (Firth should be close to MLE):')
    print('  MLE  ',np.round(m.params,4),'se',np.round(m.bse,4))
    print('  Firth',np.round(b,4),'se',np.round(se,4))
    print('  max abs difference in coefficients: %.4f'%np.max(np.abs(b-m.params)))
