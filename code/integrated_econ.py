"""
The main file for the two country economy containing basic class
and functions.
"""
import numpy as np
import random
from scipy.optimize import brentq
from scipy.optimize.minpack import fixed_point


class Country:

    def __init__(self, w, gamma=0.5, alpha=0.66, z=20, p=0.2):
        # == Current wage == #
        self.w = w  
        # == Parameters == #
        self.gamma, self.alpha, self.z, self.p = gamma, alpha, z, p

        # == Implied values == #
        self.lmda = p**((gamma - 1) / gamma) - 1
        self.wbar = (1 - alpha) * (z * p)**alpha
        self.wstar = self.wbar**(1 / (1 - alpha))

        assert z * p < (1 - alpha)**(-1/alpha), 'Warning: Equity condition failed'

    def phi(self, r):
        """
        Fraction of domestic entrepreneurs given domestic wage w and interest
        rate r.
        """
        alpha, p, z, lmda = self.alpha, self.p, self.z, self.lmda
        a = alpha * (p * z)**alpha
        b = r * (1 + lmda * self.w)
        return min((a / b)**(1/(1 - alpha)), 1)

    def current_account(self, r):
        """
        Current account with interest rate r and domestic wage rate w.  
        """
        return self.w - self.phi(r)

    def update_function(self, r):
        """
        Compute next period wages given r.
        """
        z, alpha, p = self.z, self.alpha, self.p
        return (1 - alpha) * (p * z * self.phi(r))**alpha 

    def update(self, r):
        """
        Update wages from w_t to w_{t+1} given r_{t+1}.
        """
        self.w = self.update_function(r)

    def autarky_r(self):
        """
        Interest rate in autarky at time t+1 given time t wage w.
        """
        gamma, alpha, z, p = self.gamma, self.alpha, self.z, self.p
        c1 = alpha * (z * p)**alpha 
        c2 = self.w**(1 - alpha) * (1 + self.lmda * self.w)
        return c1 / c2

    def autarky_update_function(self):
        """
        Compute next period wages.
        """
        z, alpha, p = self.z, self.alpha, self.p
        return (1 - alpha) * (p * z * self.w)**alpha 



def global_deposit_rate(country_x, country_y, incomplete=True):
    """
    Computes the equilibrium deposit rate for the integrated world economy.
    Currently we assume for simplicity that all parameters except z are the
    same value for both countries.
    """
    cx, cy = country_x, country_y
    assert cx.alpha == cy.alpha and cx.p == cy.p and cx.lmda == cy.lmda, \
            "All country parameters except z need to be identical."

    alpha, lmda, p = cx.alpha, cx.lmda, cx.p
    x, y = cx.w, cy.w

    if incomplete:
        # Smallest r we need to consider, makes phi(x, r) = phi(y, r) = 1 
        z = min(cx.z, cy.z)
        r_min = alpha * (z * p)**alpha / (1 + lmda * max(x, y))
        f = lambda r: cx.phi(r) + cy.phi(r) - x - y
        try:
            out = brentq(f, r_min, 1e2)
        except:
            import ipdb; ipdb.set_trace()
        return out

    else:
        # This needs to be finished
        return 42

