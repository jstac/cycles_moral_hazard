
import numpy as np

def phase_plot(ax, g, h, xmin, xmax, ymin, ymax, gridsize=100):
    """
    Plots the phase diagram for the system x' = g(x,y), y' = h(x,y)
    over the square [xmin, xmax] times [ymin, ymax].
    """

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    delta_g = np.vectorize(lambda x, y: x - g(x, y))
    delta_h = np.vectorize(lambda x, y: y - h(x, y))
    xgrid = np.linspace(xmin, xmax, gridsize)
    ygrid = np.linspace(ymin, ymax, gridsize)
    X, Y = np.meshgrid(xgrid, ygrid)
    Zg, Zh = delta_g(X, Y), delta_h(X, Y)
 
    ax.contour(X, Y, Zg, [.0], lw=2, alpha=0.8)
    ax.contour(X, Y, Zh, [.0], lw=2, alpha=0.8)

    def draw_arrow(x, y):
        eps = 0.0001
        v1, v2 = g(x, y) - x, h(x, y) - y
        nrm = np.sqrt(v1**2 + v2**2)
        scale = eps / nrm
        ax.arrow(x, y, scale * v1, scale * v2,
                antialiased=True, 
                alpha=0.8,
                head_length=0.025*(xmax - xmin), 
                head_width=0.012*(xmax - xmin),
                fill=False)

    xgrid = np.linspace(xmin * 1.1, xmax * 0.95, 12)
    ygrid = np.linspace(ymin * 1.1, ymax * 0.95, 12)
    for x in xgrid:
        for y in ygrid:
            draw_arrow(x, y)



