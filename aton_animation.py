from manim import *
import numpy as np

# -----------------------------------------------------------
# Helper function to compute the "carrier" based on your formulas.
# -----------------------------------------------------------
def compute_carrier(N, D=4):
    r_phi = 0.5 + np.sqrt(D+1) / 2
    r_o = 1.0 / D
    r_eta = 0.5 + 1j * np.sqrt(D-1) / 2  # equals e^(iπ/3)
    t_o = D + 3 + 3 + 3
    T_o = 4 * np.pi * (1 + np.sqrt(D+1))
    Omega = 2 * np.pi / T_o
    n_array = np.arange(N)
    # Compute the sync factor tau and then alpha, beta, gamma
    tau = r_o * r_eta * np.exp(-1j * Omega * (n_array + 1))
    alpha = (r_o + t_o - ((n_array + 1) / (2 * r_o))) * np.real(tau)
    beta  = (r_o + t_o - ((np.sqrt(D - 1) * (n_array + 1)) / 2)) * np.imag(tau)
    gamma = alpha + 1j * beta
    u = np.real(gamma)
    v = np.imag(gamma)
    w = np.log2(np.abs(gamma) + 1e-9)
    return n_array, u, v, w, gamma, alpha, beta

# -----------------------------------------------------------
# Main Manim Scene: AtomAnimation
# -----------------------------------------------------------
class AtomAnimation(ThreeDScene):
    def construct(self):
        # ----------------------------
        # Introduction & Formulas
        # ----------------------------
        title = Text("The Cosmic Atom", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Display core formulas using MathTex:
        formula1 = MathTex(r"\gamma_n = \alpha_n + i\,\beta_n")
        formula2 = MathTex(
            r"\alpha_n = \left(r_o+t_o-\frac{n+1}{2r_o}\right)\Re(\tau_n)",
            r"\quad",
            r"\beta_n = \left(r_o+t_o-\frac{\sqrt{D-1}(n+1)}{2}\right)\Im(\tau_n)"
        )
        formula3 = MathTex(r"u_n=\Re(\gamma_n),\quad v_n=\Im(\gamma_n),\quad w_n=\log_2\left(|\gamma_n|\right)")
        formulas = VGroup(formula1, formula2, formula3).arrange(DOWN, aligned_edge=LEFT).scale(0.7).to_edge(LEFT)
        self.play(Write(formulas))
        self.wait(2)
        
        # Transition from formulas to the animation:
        self.play(FadeOut(formulas), FadeOut(title))
        self.wait(1)
        
        # ----------------------------
        # Set up 3D camera orientation
        # ----------------------------
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # ----------------------------
        # Compute the carrier for the atom curves
        # ----------------------------
        N = 200  # Use fewer points for a smooth animation
        D = 4
        n_array, u, v, w, gamma, alpha, beta = compute_carrier(N, D)
        
        # -----------------------------------------------------
        # Define a subset of transforms (e.g., flower_0 from wormhole_0)
        # For simplicity, we pick 8 transforms based on simple symmetry.
        # -----------------------------------------------------
        transforms = [
            {"func": lambda u, v, w: (  u,  v,  w)},
            {"func": lambda u, v, w: (  u, -v,  w)},
            {"func": lambda u, v, w: ( -u,  v,  w)},
            {"func": lambda u, v, w: ( -u, -v,  w)},
            {"func": lambda u, v, w: (  v,  u,  w)},
            {"func": lambda u, v, w: (  v, -u,  w)},
            {"func": lambda u, v, w: ( -v,  u,  w)},
            {"func": lambda u, v, w: ( -v, -u,  w)}
        ]
        
        # Create a VGroup to hold all curves.
        curves = VGroup()
        for transform in transforms:
            # Apply the transform to get new coordinates.
            x, y, z = transform["func"](u, v, w)
            # Build a list of 3D points from the arrays.
            points = [np.array([x[i], y[i], z[i]]) for i in range(N)]
            curve = VMobject()
            curve.set_points_as_corners(points)
            curve.set_color(BLUE)
            curves.add(curve)
        
        # ----------------------------
        # Animate the drawing of the curves
        # ----------------------------
        self.play(*[Create(curve) for curve in curves], run_time=3)
        self.wait(2)
        
        # ----------------------------
        # Rotate the camera to showcase the 3D structure
        # ----------------------------
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=5)
        self.wait(2)
        
        # Fade out the curves at the end of the scene.
        self.play(FadeOut(curves))
        self.wait(1)
