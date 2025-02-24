import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
# Enforce a pure black background (dark style)
# =============================================================================
plt.style.use('dark_background')
plt.rcParams.update({
    "lines.color": "black",
    "patch.edgecolor": "black",
    "text.color": "black",
    "axes.facecolor": "black",
    "axes.edgecolor": "black",
    "axes.labelcolor": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "grid.color": "black",
    "figure.facecolor": "black",
    "figure.edgecolor": "black",
    "savefig.facecolor": "black",
    "savefig.edgecolor": "black"
})

# =============================================================================
# Compute the Carrier using the Toy-Universe Formulas
# =============================================================================
def compute_carrier(N, D=4):
    r_phi = 0.5 + np.sqrt(D+1)/2
    r_o = 1.0 / D
    r_eta = 0.5 + 1j * np.sqrt(D-1)/2  
    t_o = D + 3 + 3 + 3
    T_o = 4 * np.pi * (1 + np.sqrt(D+1))
    Omega = 2 * np.pi / T_o
    n_array = np.arange(N)
    phi = ((n_array+1)/r_o) * np.exp(1j * Omega*(n_array+1))
    eta = (n_array+1) * r_eta
    tau = r_o * r_eta * np.exp(-1j * Omega*(n_array+1))
    alpha = (r_o+t_o - ((n_array+1)/(2*r_o))) * np.real(tau)
    beta  = (r_o+t_o - ((np.sqrt(D-1)*(n_array+1))/2)) * np.imag(tau)
    gamma = alpha + 1j*beta
    u = np.real(gamma)
    v = np.imag(gamma)
    w = np.log2(np.abs(gamma) + 1e-9)
    return n_array, u, v, w, gamma, alpha, beta

# =============================================================================
# Helper Functions for Coloring and Plotting
# =============================================================================
def get_colors(n_array, M_c, cmap_name='hsv'):
    indices = n_array % M_c
    cmap = plt.get_cmap(cmap_name, M_c)
    return [cmap(i) for i in indices]

def remove_axes(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.xaxis.pane.set_visible(False)
    ax.yaxis.pane.set_visible(False)
    ax.zaxis.pane.set_visible(False)
    try:
        ax.w_xaxis.line.set_visible(False)
        ax.w_yaxis.line.set_visible(False)
        ax.w_zaxis.line.set_visible(False)
    except AttributeError:
        pass

# =============================================================================
# Define the 48 rotation transforms (Wormholes & Flowers)
# =============================================================================
transforms = [{"wormhole": w, "flower": f, "group": g, "func": fn}
              for w, f, g, fn in [
    (0, 0, "xyz", lambda u,v,w: ( u,  v,  w)),
    (0, 0, "xyz", lambda u,v,w: ( u, -v,  w)),
    (0, 0, "xyz", lambda u,v,w: (-u,  v,  w)),
    (0, 0, "xyz", lambda u,v,w: (-u, -v,  w)),
    (0, 1, "xy(-z)", lambda u,v,w: ( u,  v, -w)),
    (0, 1, "xy(-z)", lambda u,v,w: ( u, -v, -w)),
    (1, 2, "zxy", lambda u,v,w: ( w,  u,  v)),
    (1, 2, "zyx", lambda u,v,w: ( w,  v,  u)),
    (1, 3, "(-z)xy", lambda u,v,w: (-w,  u,  v)),
    (1, 3, "(-z)yx", lambda u,v,w: (-w,  v,  u)),
    (2, 4, "xzy", lambda u,v,w: ( u,  w,  v)),
    (2, 5, "x(-z)y", lambda u,v,w: ( u, -w,  v))
] * 4]

# =============================================================================
# Filter Transforms
# =============================================================================
def filter_transforms(flower_index=None, wormhole_index=None):
    filtered = transforms
    if flower_index is not None:
        filtered = [t for t in filtered if t["flower"] == flower_index]
    if wormhole_index is not None:
        filtered = [t for t in filtered if t["wormhole"] == wormhole_index]
    return filtered

# =============================================================================
# Plot and Animate Functions
# =============================================================================
def plot_atom(n_array, u, v, w, gamma, M_c, flower_index=None, wormhole_index=None):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    for t in filter_transforms(flower_index, wormhole_index):
        x, y, z = t["func"](u, v, w)
        ax.plot(x, y, z, alpha=0.7)
    remove_axes(ax)
    plt.show()

def animate_atom(n_array, u, v, w, gamma, M_c, flower_index=None, wormhole_index=None, interval=100):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    curves = [t["func"](u, v, w) for t in filter_transforms(flower_index, wormhole_index)]

    def update(frame):
        ax.clear()
        for x, y, z in curves:
            ax.plot(x[:frame], y[:frame], z[:frame], alpha=0.7)
        remove_axes(ax)
    
    ani = FuncAnimation(fig, update, frames=len(n_array), interval=interval, repeat=False)
    plt.show()

# =============================================================================
# Main Execution
# =============================================================================
N = 1000
D = 4
M_c = 13
n_array, u, v, w, gamma, alpha, beta = compute_carrier(N, D)

# Plot full atom
plot_atom(n_array, u, v, w, gamma, M_c)

# Plot specific flower or wormhole
plot_atom(n_array, u, v, w, gamma, M_c, flower_index=1)
plot_atom(n_array, u, v, w, gamma, M_c, wormhole_index=2)

# Animate full atom
animate_atom(n_array, u, v, w, gamma, M_c, interval=50)
