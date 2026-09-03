# -*- coding: utf-8 -*-
"""Firth penalised (Jeffreys-prior) logistic regression.

Reports profile penalised-likelihood confidence intervals and penalised
likelihood-ratio p-values, as R's logistf does. Wald intervals are NOT used:
under separation they are unreliable, and for the separated contrast in this
study the Wald and profile intervals disagree on whether unity is excluded.

Running this file as a script performs two checks:
  1. against the ordinary MLE on data that are not separated;
  2. against a worked separated example, where the profile interval must be
     asymmetric and much wider on the upper side than a Wald interval.
"""
import numpy as np
from scipy.optimize import brentq

def _plogl(X, y, b):
    """Penalised log-likelihood: l(b) + 0.5*log|I(b)|."""
    eta = X @ b
    ll = np.sum(y*eta - np.logaddexp(0.0, eta))
    mu = 1/(1+np.exp(-eta)); w = np.clip(mu*(1-mu), 1e-12, None)
    sign, logdet = np.linalg.slogdet(X.T @ (X*w[:, None]))
    return ll + 0.5*logdet

def firth_logit(X, y, fixed=None, tol=1e-10, maxit=500):
    """Fit by penalised IRLS. `fixed` = (index, value) holds one coefficient."""
    X = np.asarray(X, float); y = np.asarray(y, float); n, p = X.shape
    b = np.zeros(p)
    if fixed is not None: b[fixed[0]] = fixed[1]
    free = [j for j in range(p) if fixed is None or j != fixed[0]]
    for _ in range(maxit):
        eta = X @ b; mu = 1/(1+np.exp(-eta)); w = np.clip(mu*(1-mu), 1e-12, None)
        XW = X*w[:, None]; I = X.T @ XW
        Iinv = np.linalg.pinv(I)
        h = np.einsum('ij,jk,ik->i', XW, Iinv, X)
        U = X.T @ (y - mu + h*(0.5 - mu))
        if free:
            Isub = I[np.ix_(free, free)]
            step = np.zeros(p); step[free] = np.linalg.pinv(Isub) @ U[free]
        else:
            step = np.zeros(p)
        t = 1.0
        while t > 1e-8 and np.max(np.abs(t*step)) > 5: t /= 2
        b = b + t*step
        if np.max(np.abs(t*step)) < tol: break
    eta = X @ b; mu = 1/(1+np.exp(-eta)); w = np.clip(mu*(1-mu), 1e-12, None)
    se = np.sqrt(np.diag(np.linalg.pinv(X.T @ (X*w[:, None]))))
    return b, se

def profile_ci(X, y, j, level=0.95, span=60.0):
    """Profile penalised-likelihood CI and likelihood-ratio p for coefficient j."""
    from scipy.stats import chi2
    X = np.asarray(X, float); y = np.asarray(y, float)
    b_hat, se = firth_logit(X, y)
    l_max = _plogl(X, y, b_hat)
    crit = chi2.ppf(level, 1)
    def g(v):
        b, _ = firth_logit(X, y, fixed=(j, v))
        return 2*(l_max - _plogl(X, y, b)) - crit
    def hunt(direction):
        lo, hi = b_hat[j], b_hat[j]
        step = max(se[j], 0.5)
        for _ in range(200):
            hi = hi + direction*step
            if abs(hi - b_hat[j]) > span: return direction*np.inf
            if g(hi) > 0: return brentq(g, min(lo, hi), max(lo, hi), xtol=1e-6)
            lo = hi; step *= 1.5
        return direction*np.inf
    lo, hi = hunt(-1), hunt(+1)
    b0, _ = firth_logit(X, y, fixed=(j, 0.0))
    lr = 2*(l_max - _plogl(X, y, b0))
    return lo, hi, 1 - chi2.cdf(lr, 1)

if __name__ == '__main__':
    import statsmodels.api as sm
    rng = np.random.default_rng(0)
    n = 400; x = rng.normal(size=n); X = np.column_stack([np.ones(n), x])
    y = (rng.random(n) < 1/(1+np.exp(-(-0.4+0.8*x)))).astype(float)
    b, se = firth_logit(X, y); m = sm.Logit(y, X).fit(disp=0)
    print('check 1 - no separation, Firth should approach the MLE')
    print('  MLE   ', np.round(m.params, 4), 'se', np.round(m.bse, 4))
    print('  Firth ', np.round(b, 4), 'se', np.round(se, 4))
    print('  max |coefficient difference| = %.4f' % np.max(np.abs(b - m.params)))
    yy = np.r_[np.ones(65), np.zeros(48), np.zeros(6)]
    xx = np.r_[np.ones(113), np.zeros(6)]
    XX = np.column_stack([np.ones(len(yy)), xx])
    bb, ss = firth_logit(XX, yy); lo, hi, p = profile_ci(XX, yy, 1)
    print('check 2 - separated 65/113 vs 0/6')
    print('  OR %.2f' % np.exp(bb[1]))
    print('  Wald    95%% CI %.2f to %.1f' % (np.exp(bb[1]-1.96*ss[1]), np.exp(bb[1]+1.96*ss[1])))
    print('  profile 95%% CI %.2f to %.1f ; penalised LR p = %.4f' % (np.exp(lo), np.exp(hi), p))
