"""
Functions for simulated two country time series
"""

import numpy as np
from integrated_econ import *

def simulate_world_econ(n, 
        country_x, 
        country_y, 
        x0=None, 
        y0=None, 
        stochastic=False):

    # == Initialize arrays == #
    x   = np.empty(n)
    y   = np.empty(n)
    ca_x    = np.empty(n)
    ca_y    = np.empty(n)
    world_r = np.empty(n+1)
    
    if x0 is not None:
        country_x.w = x0
    if y0 is not None:
        country_y.w = y0


    for t in range(n):
        if stochastic:
            country_x.z = random.uniform(15, 25) 
            country_y.z = random.uniform(15, 25) 
        r = global_deposit_rate(country_x, country_y)
        world_r[t+1] = r
        x[t], y[t] = country_x.w, country_y.w
        ca_x[t] = country_x.current_account(r)  
        ca_y[t] = country_y.current_account(r)  

        country_x.update(r)
        country_y.update(r)

    return x, y, world_r, ca_x, ca_y


def simulate_autarky(n, country_x):

    # == Initialize arrays == #
    x   = np.empty(n)
    autarky_r = np.empty(n+1)
    
    for t in range(n):
        r = country_x.autarky_r()
        autarky_r[t+1] = r
        x[t] = country_x.w
        country_x.update(r)

    return x, autarky_r
