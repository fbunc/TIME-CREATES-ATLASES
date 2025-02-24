import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D  # registers 3D projection

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
    r"""
    Computes the carrier (time wave) for a 4D toy universe with:
    
      \(D=4\),
      \(r_{\phi}=\tfrac{1}{2}+\tfrac{\sqrt{D+1}}{2}\),
      \(r_o=\frac{1}{D}\),
      \(r_{\eta}=\frac{1}{2}+i\frac{\sqrt{D-1}}{2}=e^{i\pi/3}\),
      \(t_o=D+3+3+3\).
      
    Then, for \(n\ge0\):
    
      \[
      r_n=\frac{n+1}{r_o}\,,
      \]
      \[
      T_o=4\pi(1+\sqrt{D+1}),\quad \Omega=\frac{2\pi}{T_o}\,,
      \]
      and the time phase is
      \[
      \phi_n=\frac{n+1}{r_o}\exp\Bigl(i\,\Omega(n+1)\Bigr),
      \]
      while the time norm is
      \[
      \eta_n=(n+1)r_{\eta}\,.
      \]
      
      The sync factor is
      \[
      \tau_n=r_o\,r_{\eta}\,\exp\Bigl(-i\,\Omega(n+1)\Bigr)\,.
      \]
      
      Then define:
      \[
      \alpha_n=\Bigl(r_o+t_o-\frac{n+1}{2r_o}\Bigr)\Re(\tau_n),\quad
      \beta_n=\Bigl(r_o+t_o-\frac{\sqrt{D-1}(n+1)}{2}\Bigr)\Im(\tau_n),
      \]
      and the carrier is
      \[
      \gamma_n=\alpha_n+i\,\beta_n\,.
      \]
      
      For plotting we set:
      \[
      u_n=\Re(\gamma_n),\quad v_n=\Im(\gamma_n),\quad w_n=\log_2\bigl(|\gamma_n|\bigr).
      \]
    """
    r_phi = 0.5 + np.sqrt(D+1)/2
    r_o = 1.0 / D
    r_eta = 0.5 + 1j * np.sqrt(D-1)/2  # equals e^(iπ/3)
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
    # Hide the pane backgrounds
    ax.xaxis.pane.set_visible(False)
    ax.yaxis.pane.set_visible(False)
    ax.zaxis.pane.set_visible(False)
    # Hide the axis lines if possible.
    try:
        ax.w_xaxis.line.set_visible(False)
        ax.w_yaxis.line.set_visible(False)
        ax.w_zaxis.line.set_visible(False)
    except AttributeError:
        pass

# =============================================================================
# Basic Mirroring Transformations (for potential future use)
# =============================================================================
def mirror_xyz(u, v, w, sign_u=1, sign_v=1, sign_w=1):
    return sign_u*u, sign_v*v, sign_w*w

def mirror_yxz(u, v, w, sign_u=1, sign_v=1, sign_w=1):
    return sign_u*v, sign_v*u, sign_w*w

# =============================================================================
# Define the 48 rotation transforms (Wormholes & Flowers)
# =============================================================================
transforms = [
    # Wormhole_0, Flower_0: "xyz"
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: (  u,  v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: (  u, -v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: ( -u,  v,  w)},
    {"wormhole": 0, "flower": 0, "group": "xyz",    "func": lambda u,v,w: ( -u, -v,  w)},
    # Wormhole_0, Flower_0: "yxz"
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: (  v,  u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: (  v, -u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: ( -v,  u,  w)},
    {"wormhole": 0, "flower": 0, "group": "yxz",    "func": lambda u,v,w: ( -v, -u,  w)},
    
    # Wormhole_0, Flower_1: "xy(-z)"
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: (  u,  v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: (  u, -v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: ( -u,  v, -w)},
    {"wormhole": 0, "flower": 1, "group": "xy(-z)", "func": lambda u,v,w: ( -u, -v, -w)},
    # Wormhole_0, Flower_1: "yx(-z)"
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: (  v,  u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: (  v, -u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: ( -v,  u, -w)},
    {"wormhole": 0, "flower": 1, "group": "yx(-z)", "func": lambda u,v,w: ( -v, -u, -w)},
    
    # Wormhole_1, Flower_2: "zxy"
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w,  u,  v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w,  u, -v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w, -u,  v)},
    {"wormhole": 1, "flower": 2, "group": "zxy",    "func": lambda u,v,w: (  w, -u, -v)},
    # Wormhole_1, Flower_2: "zyx"
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w,  v,  u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w,  v, -u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w, -v,  u)},
    {"wormhole": 1, "flower": 2, "group": "zyx",    "func": lambda u,v,w: (  w, -v, -u)},
    
    # Wormhole_1, Flower_3: "(-z)xy"
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w,  u,  v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w,  u, -v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w, -u,  v)},
    {"wormhole": 1, "flower": 3, "group": "(-z)xy", "func": lambda u,v,w: (-w, -u, -v)},
    # Wormhole_1, Flower_3: "(-z)yx"
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w,  v,  u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w,  v, -u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w, -v,  u)},
    {"wormhole": 1, "flower": 3, "group": "(-z)yx", "func": lambda u,v,w: (-w, -v, -u)},
    
    # Wormhole_2, Flower_4: "xzy"
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: (  u,  w,  v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: (  u,  w, -v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: ( -u,  w,  v)},
    {"wormhole": 2, "flower": 4, "group": "xzy",    "func": lambda u,v,w: ( -u,  w, -v)},
    # Wormhole_2, Flower_4: "yzx"
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: (  v,  w,  u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: (  v,  w, -u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: ( -v,  w,  u)},
    {"wormhole": 2, "flower": 4, "group": "yzx",    "func": lambda u,v,w: ( -v,  w, -u)},
    
    # Wormhole_2, Flower_5: "x(-z)y"
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: (  u, -w,  v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: (  u, -w, -v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: ( -u, -w,  v)},
    {"wormhole": 2, "flower": 5, "group": "x(-z)y", "func": lambda u,v,w: ( -u, -w, -v)},
    # Wormhole_2, Flower_5: "y(-z)x"
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: (  v, -w,  u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: (  v, -w, -u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: ( -v, -w,  u)},
    {"wormhole": 2, "flower": 5, "group": "y(-z)x", "func": lambda u,v,w: ( -v, -w, -u)},
]

# =============================================================================
# Static Atom Plot Function (Scatter-focused)
# =============================================================================
def plot_atom(n_array, u, v, w, gamma, M_c, plot_mode='both',
              scatter_size=20, scatter_alpha=1.0,
              line_alpha=0.7, line_width=1.5, line_cmap='viridis'):
    """
    Create a static 3D atom plot (48 curves) using the rotated carrier.
    
    Parameters
    ----------
    n_array : ndarray
        Array of time indices.
    u, v, w : ndarray
        Carrier coordinates.
    gamma : ndarray
        Complex carrier (used for computing first differences).
    M_c : int
        Modulus for assigning scatter colors (n mod M_c).
    plot_mode : str
        Options: 'line' (lines only), 'scatter' (scatter only), 'both' (both).
    scatter_size : float
        Size of scatter dots.
    scatter_alpha : float
        Alpha transparency for scatter dots.
    line_alpha : float
        Alpha transparency for line segments.
    line_width : float
        Width of line segments.
    line_cmap : str
        Colormap name for line segments (gradient from |Δγ|).
    """
    N = len(n_array)
    dZ = np.abs(np.diff(gamma))
    norm_dZ = (dZ - dZ.min()) / (dZ.max() - dZ.min()) if dZ.max() - dZ.min() > 0 else np.zeros_like(dZ)
    line_cm = plt.get_cmap(line_cmap)
    scatter_colors = get_colors(n_array, M_c, cmap_name='hsv')
    
    fig = plt.figure(figsize=(16, 16), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    fig.patch.set_facecolor('black')
    
    # Loop through each transform and plot its rotated curve.
    for t in transforms:
        x, y, z = t["func"](u, v, w)
        if plot_mode in ['line', 'both']:
            segments = np.array([[[x[i], y[i], z[i]], [x[i+1], y[i+1], z[i+1]]] for i in range(N-1)])
            seg_colors = [line_cm(norm_dZ[i]) for i in range(N-1)]
            lc = Line3DCollection(segments, colors=seg_colors, linewidths=line_width, alpha=line_alpha)
            ax.add_collection3d(lc)
        if plot_mode in ['scatter', 'both']:
            ax.scatter(x, y, z, s=scatter_size, c=scatter_colors, alpha=scatter_alpha, depthshade=True)
    
    remove_axes(ax)
    ax.set_title("Atom Plot: 48 Curves with Gradient Line Segments", color='white', pad=20)
    plt.tight_layout()
    plt.show()

# =============================================================================
# Animated Atom Plot Function (Scatter-focused, with dynamic zoom-out)
# =============================================================================
def animate_atom(n_array, u, v, w, gamma, M_c, plot_mode='both',
                 scatter_size=20, scatter_alpha=1.0,
                 line_alpha=0.7, line_width=1.5, line_cmap='viridis',
                 frame_interval=1000, video_file=None):
    """
    Animate the atom plot over time with dynamic zoom-out.
    
    Each frame shows all points up to that index. The axis limits are updated
    dynamically to include all current points with a 10% margin.
    
    Parameters
    ----------
    n_array : ndarray
        Array of time indices.
    u, v, w : ndarray
        Carrier coordinates.
    gamma : ndarray
        Complex carrier.
    M_c : int
        Color modulus for scatter points.
    plot_mode : str
        'line', 'scatter', or 'both'.
    scatter_size : float
        Scatter dot size.
    scatter_alpha : float
        Scatter alpha.
    line_alpha : float
        Line segment alpha.
    line_width : float
        Line segment width.
    line_cmap : str
        Colormap for line segments (gradient based on |Δγ|).
    frame_interval : int
        Time (in ms) between frames (default 1000 ms/frame).
    video_file : str or None
        If provided, the animation is saved to this file.
    """
    N = len(n_array)
    dZ = np.abs(np.diff(gamma))
    norm_dZ = (dZ - dZ.min()) / (dZ.max() - dZ.min()) if dZ.max()-dZ.min()>0 else np.zeros_like(dZ)
    line_cm = plt.get_cmap(line_cmap)
    scatter_colors = get_colors(n_array, M_c, cmap_name='hsv')
    
    # Precompute rotated curves for all transforms.
    curves = []
    for t in transforms:
        x, y, z = t["func"](u, v, w)
        curves.append({'x': x, 'y': y, 'z': z})
    
    fig = plt.figure(figsize=(16, 16), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    fig.patch.set_facecolor('black')
    remove_axes(ax)
    
    # Create empty lists to hold the scatter and line objects.
    scatter_objs = []
    line_objs = []
    
    for curve in curves:
        if plot_mode in ['scatter', 'both']:
            sc = ax.scatter(curve['x'][:1], curve['y'][:1], curve['z'][:1],
                            s=scatter_size, c=np.array(scatter_colors[:1]), alpha=scatter_alpha, depthshade=True)
            scatter_objs.append(sc)
        else:
            scatter_objs.append(None)
        if plot_mode in ['line', 'both']:
            ln, = ax.plot(curve['x'][:1], curve['y'][:1], curve['z'][:1],
                          color=line_cm(0), lw=line_width, alpha=line_alpha)
            line_objs.append(ln)
        else:
            line_objs.append(None)
    
    ax.set_title("Animated Atom Plot", color='white', pad=20)
    
    def update(frame):
        # Lists to collect current points across all curves.
        all_x = []
        all_y = []
        all_z = []
        for i, curve in enumerate(curves):
            cur_x = curve['x'][:frame]
            cur_y = curve['y'][:frame]
            cur_z = curve['z'][:frame]
            all_x.extend(cur_x)
            all_y.extend(cur_y)
            all_z.extend(cur_z)
            if scatter_objs[i] is not None:
                scatter_objs[i]._offsets3d = (cur_x, cur_y, cur_z)
                new_colors = np.array(scatter_colors[:frame])
                scatter_objs[i].set_facecolors(new_colors)
            if line_objs[i] is not None:
                line_objs[i].set_data(cur_x, cur_y)
                line_objs[i].set_3d_properties(cur_z)
                if frame > 1:
                    idx = frame - 2 if frame - 2 < len(norm_dZ) else -1
                    line_objs[i].set_color(line_cm(norm_dZ[idx]))
        # Update axis limits dynamically based on current points, with a 10% margin.
        if all_x and all_y and all_z:
            min_x, max_x = np.min(all_x), np.max(all_x)
            min_y, max_y = np.min(all_y), np.max(all_y)
            min_z, max_z = np.min(all_z), np.max(all_z)
            margin_x = 0.1 * (max_x - min_x) if max_x > min_x else 1
            margin_y = 0.1 * (max_y - min_y) if max_y > min_y else 1
            margin_z = 0.1 * (max_z - min_z) if max_z > min_z else 1
            ax.set_xlim(min_x - margin_x, max_x + margin_x)
            ax.set_ylim(min_y - margin_y, max_y + margin_y)
            ax.set_zlim(min_z - margin_z, max_z + margin_z)
        return scatter_objs + line_objs

    ani = FuncAnimation(fig, update, frames=N, interval=frame_interval, blit=False)
    
    if video_file:
        writer = FFMpegWriter(fps=1)
        ani.save(video_file, writer=writer)
    else:
        plt.show()

# =============================================================================
# Main Execution
# =============================================================================
def main():
    # Parameters for the carrier
    N = 1000        # Number of points
    D = 4           # For our toy-universe: 3+1=4
    M_c = 13        # Color modulus (n mod M_c)
    
    # Compute the carrier using our formulas.
    n_array, u, v, w, gamma, alpha, beta = compute_carrier(N, D)
    
    # # To plot the Atom structure (all 48 curves) statically as scatter only:
    # plot_atom(n_array, u, v, w, gamma, M_c, plot_mode='scatter',
    #           scatter_size=7, scatter_alpha=0.5,
    #           line_alpha=0.7, line_width=2, line_cmap='hsv')
    
    # To animate the Atom structure with dynamic zoom-out, uncomment:
    animate_atom(n_array, u, v, w, gamma, M_c, plot_mode='scatter',
                 scatter_size=7, scatter_alpha=0.5,
                 line_alpha=0.7, line_width=2, line_cmap='hsv',
                 frame_interval=1000, video_file=None)

if __name__ == '__main__':
    main()
