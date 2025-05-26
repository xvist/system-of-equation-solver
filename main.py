import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox

# === Main logic of plot building ===
def solve_and_plot(eq1_str, eq2_str, x_min, x_max, y_min, y_max, steps=200):
    try:
        x_vals = np.linspace(x_min, x_max, steps)
        y_vals = np.linspace(y_min, y_max, steps)
        X, Y = np.meshgrid(x_vals, y_vals)

        def safe_eval(expr, x, y):
            return eval(expr, {"__builtins__": None, "x": x, "y": y, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp})

        Z1 = safe_eval(eq1_str, X, Y)
        Z2 = safe_eval(eq2_str, X, Y)

        def plot_equation(Z, subplot_index):
            plt.subplot(1, 2, subplot_index)
            for i in range(Z.shape[0]):
                for j in range(Z.shape[1]):
                    if Z[i, j] > 0:
                        plt.text(x_vals[j], y_vals[i], 'o', color='red', ha='center', va='center', fontsize=8)
                    elif Z[i, j] < 0:
                        plt.text(x_vals[j], y_vals[i], 'x', color='blue', ha='center', va='center', fontsize=8)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axis('equal')

        plt.figure(figsize=(14, 7))  # a little bit larger
        plot_equation(Z1, 1)
        plot_equation(Z2, 2)

        # Margin regulation
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08, wspace=0.25)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the calculation: {e}")


# === GUI ===
def launch_gui():
    root = tk.Tk()
    root.withdraw()  # Hide main window

    eq1 = simpledialog.askstring("Equation 1", "Enter the first equation (for example: x**2 + y**2 - 4):")
    eq2 = simpledialog.askstring("Equation 2", "Enter the second equation (for example: x - y**2):")

    x_min = simpledialog.askfloat("min x", "Enter the minimum value x:", initialvalue=-5)
    x_max = simpledialog.askfloat("max x", "Enter the maximum value x:", initialvalue=5)
    y_min = simpledialog.askfloat("min y", "Enter the minimum value y:", initialvalue=-5)
    y_max = simpledialog.askfloat("max y", "Enter the maximum value y:", initialvalue=5)

    if None not in [eq1, eq2, x_min, x_max, y_min, y_max]:
        solve_and_plot(eq1, eq2, x_min, x_max, y_min, y_max)

launch_gui()
