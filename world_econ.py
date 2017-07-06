"""
Classes and functions for computing interest rates and dynamics in the
KSV economy.
"""

import numpy as np
import random
from scipy.optimize import brentq, bisect
from scipy.optimize.minpack import fixed_point


class Country:
    
    def __init__(self, v1=1, q0=0.2, q1 = 0.8, alpha=0.5, z=5):
        self.v1, self.q0, self.q1, self.alpha, self.z = v1, q0, q1, alpha, z
        
        self.calibrate()
        
    def calibrate(self, verbose=False):
        """
        Compute / recompute the implied constants
        """
        self.eta = np.exp(self.v1 / (self.q1 - self.q0))
        self.theta = ((self.eta - 1) * self.q1 + 1)/ self.eta**self.q0 - 1
        self.R = self.q1 * self.z
        self.wstar = ((1 - self.alpha) * self.R**self.alpha)**(1/(1 - self.alpha))
        self.wbar = (1 - self.alpha) * self.R**self.alpha
        self.stability_measure = (2 * self.alpha - 1) * self.theta * self.wstar / (1 - self.alpha)
        if verbose:
            v = (1 - self.alpha) * self.R**self.alpha
            print(f"should be < 1: {v}")
        
    def f_prime_inv(self, y):
        return (self.alpha / y)**(1/(1 - self.alpha))

    def phi(self, w, r):
        """
        Fraction of domestic entrepreneurs when not in autarky.  Computed from
        domestic wage w and interest rate r.
        """
        y = (1 / self.R) * self.f_prime_inv((1 + self.theta * w) * (r / self.R))
        return min(y, 1)

    def update_wage_from_phi(self, phi):
        """
        Compute next period wages when the fraction of entrepreneurs is phi.
        """
        return (1 - self.alpha) * (self.R * phi)**self.alpha  # Not self.phi!

    def update_wage(self, w, r):
        """
        Compute next period w given w and r.
        """
        phi = self.phi(w, r)
        return self.update_wage_from_phi(phi)

    def autarky_update_wage(self, w):
        """
        Compute next period wages in autarky
        """
        phi = w
        return self.update_wage_from_phi(phi)

    def autarky_r(self, w):
        """
        Interest rate in autarky at time t+1 given time t wage w.
        """
        c1 = self.alpha * self.R**self.alpha * w**(self.alpha - 1) # Rf'(k_{t+1})
        c2 = 1 + self.theta * w
        return c1 / c2

    def current_account(self, w, r):
        """
        Current account with interest rate r and domestic wage rate w.  
        """
        return w - self.phi(w, r)


    



def integrated_world_r(cx, wx, cy, wy):
    """
    Computes the equilibrium deposit rate for the integrated world economy.

    Parameters
    ----------

    cx : a Country
    wx : wage in country x
    cy : a Country
    wy : wage in country y

    """
    alpha_x, theta_x = cx.alpha, cx.theta
    alpha_y, theta_y = cy.alpha, cy.theta
    Rx = cx.R
    Ry = cy.R

    r_min_x = alpha_x * Rx**alpha_x / (1 + theta_x * (1 - alpha_x) * Rx**alpha_x)
    r_min_y = alpha_y * Ry**alpha_y / (1 + theta_y * (1 - alpha_y) * Ry**alpha_y)
    r_min = min(r_min_x, r_min_y) * 0.001
    r_max = r_min * 1e12

    f = lambda r: cx.phi(wx, r) + cy.phi(wy, r) - wx - wy
    try:
        out = brentq(f, r_min, r_max)
    except:
        print(wx, wy)
        out = 1
    return out

