"""
Time series plot comparing complete and incomplete markets
"""

import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from phase_plot import phase_plot
from integrated_econ import *
from simulate_world_econ_ts import *

rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

gamma = 0.4
alpha = 0.55
z     = 10
p     = 0.25

n = 3
wx0, wy0 = 0.1, 0.9
ymin = 0.0
ymax = 1.0

country_x = Country(wx0, gamma=gamma, alpha=alpha, z=z, p=p)
country_y = Country(wy0, gamma=gamma, alpha=alpha, z=z, p=p)


fig, axes = plt.subplots(2, 1, figsize=(10, 6.0))


for ax in axes:
    ax.set_xlim(0, n-1)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(range(n))

# == Incomplete market == #
x, y, world_r, ca_x, ca_y = simulate_world_econ(n, country_x, country_y)

ax = axes[1]
ax.set_ylabel('moral hazard', fontsize=16)
ax.plot(range(n), x, '-', lw=2, alpha=0.8, label='country X')
ax.plot(range(n), y, '--', lw=2, alpha=0.8, label='country Y')
ax.plot(range(n+1), [country_x.wstar] * (n+1), 'k--', label=r'$w^*$')
ax.legend(ncol=3, frameon=0)

# == Complete markets == #
xc = np.zeros(n)
yc = np.zeros(n)
xc[0], yc[0] = wx0, wy0

def f(x, y):
    return (1 - alpha) * (z * p * 0.5 * (x + y))**alpha

for t in range(n-1):
    xc[t+1] = f(xc[t], yc[t])
    yc[t+1] = xc[t+1]

ax = axes[0]
ax.set_ylabel('no moral hazard', fontsize=16)
ax.plot(range(n), xc, '-', lw=2, alpha=0.8, label='country X')
ax.plot(range(n), yc, '--', lw=2, alpha=0.8, label='country Y')
ax.plot(range(n+1), [country_x.wstar] * (n+1), 'k--', label=r'$w^*$')
ax.legend(ncol=3, frameon=0)

plt.show()

