import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk
from shapely.geometry import LineString
from shapely.ops import unary_union

def solve_and_plot(eq1_str, eq2_str, x_min, x_max, y_min, y_max, steps=300):
    try:
        x_vals = np.linspace(x_min, x_max, steps)
        y_vals = np.linspace(y_min, y_max, steps)
        X, Y = np.meshgrid(x_vals, y_vals)

        def safe_eval(expr, x, y):
            return eval(expr, {"__builtins__": None, "x": x, "y": y,
                               "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp})

        Z1 = safe_eval(eq1_str, X, Y)
        Z2 = safe_eval(eq2_str, X, Y)

        def plot_fast(Z, subplot_index):
            plt.subplot(1, 2, subplot_index)
            x_flat = X.flatten()
            y_flat = Y.flatten()
            z_flat = Z.flatten()

            mask_pos = z_flat > 0
            mask_neg = z_flat < 0

            plt.scatter(x_flat[mask_pos], y_flat[mask_pos], color='red', marker='o', s=10)
            plt.scatter(x_flat[mask_neg], y_flat[mask_neg], color='blue', marker='x', s=10)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axis('equal')

        plt.figure(figsize=(14, 7))
        plot_fast(Z1, 1)
        plot_fast(Z2, 2)
        plt.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08, wspace=0.25)
        plt.show()

        find_intersections(X, Y, Z1, Z2)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the calculation: {e}")

def find_intersections(X, Y, Z1, Z2):
    # Building contours
    contours1 = plt.contour(X, Y, Z1, levels=[0], colors='red', linewidths=2)
    contours2 = plt.contour(X, Y, Z2, levels=[0], colors='blue', linewidths=2)

    def extract_lines(contour):
        lines = []
        for collection in contour.collections:
            for path in collection.get_paths():
                v = path.vertices
                if len(v) > 1:
                    lines.append(LineString(v))
        return lines

    lines1 = extract_lines(contours1)
    lines2 = extract_lines(contours2)

    curve1 = unary_union(lines1)
    curve2 = unary_union(lines2)

    intersections = curve1.intersection(curve2)

    # Clearing the table
    for row in table.get_children():
        table.delete(row)

    plt.clf()
    plt.contour(X, Y, Z1, levels=[0], colors='red', linewidths=2)
    plt.contour(X, Y, Z2, levels=[0], colors='blue', linewidths=2)

    if intersections.is_empty:
        messagebox.showinfo("Information", "No intersection points.")
    else:
        if intersections.geom_type == 'Point':
            plt.plot(intersections.x, intersections.y, 'ko', markersize=6)
            table.insert("", "end", values=(f"{intersections.x:.4f}", f"{intersections.y:.4f}"))
        elif intersections.geom_type == 'MultiPoint':
            for pt in intersections:
                plt.plot(pt.x, pt.y, 'ko', markersize=6)
                table.insert("", "end", values=(f"{pt.x:.4f}", f"{pt.y:.4f}"))

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Curve intersection points Z1=0 і Z2=0')
    plt.axis('equal')
    plt.grid(True)
    plt.show()

# === GUI ===

def run():
    try:
        eq1 = entry_eq1.get()
        eq2 = entry_eq2.get()
        x_min = float(entry_x_min.get())
        x_max = float(entry_x_max.get())
        y_min = float(entry_y_min.get())
        y_max = float(entry_y_max.get())

        solve_and_plot(eq1, eq2, x_min, x_max, y_min, y_max)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("System of equations: graphs and points of intersection")

# Input fields
tk.Label(root, text="Equation 1 (x, y):").grid(row=0, column=0, sticky="e")
entry_eq1 = tk.Entry(root, width=40)
entry_eq1.insert(0, "x**2 + y**2 - 4")
entry_eq1.grid(row=0, column=1)

tk.Label(root, text="Equation 2 (x, y):").grid(row=1, column=0, sticky="e")
entry_eq2 = tk.Entry(root, width=40)
entry_eq2.insert(0, "y - x")
entry_eq2.grid(row=1, column=1)

tk.Label(root, text="x min").grid(row=2, column=0, sticky="e")
entry_x_min = tk.Entry(root)
entry_x_min.insert(0, "-5")
entry_x_min.grid(row=2, column=1)

tk.Label(root, text="x max").grid(row=3, column=0, sticky="e")
entry_x_max = tk.Entry(root)
entry_x_max.insert(0, "5")
entry_x_max.grid(row=3, column=1)

tk.Label(root, text="y min").grid(row=4, column=0, sticky="e")
entry_y_min = tk.Entry(root)
entry_y_min.insert(0, "-5")
entry_y_min.grid(row=4, column=1)

tk.Label(root, text="y max").grid(row=5, column=0, sticky="e")
entry_y_max = tk.Entry(root)
entry_y_max.insert(0, "5")
entry_y_max.grid(row=5, column=1)

btn = tk.Button(root, text="Build", command=run)
btn.grid(row=6, column=0, columnspan=2, pady=10)

# === Table for intersection points ===
frame = tk.LabelFrame(root, text="Coordinates of intersection points", padx=5, pady=5)
frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

table = ttk.Treeview(frame, columns=("x", "y"), show="headings", height=6)
table.heading("x", text="x")
table.heading("y", text="y")
table.column("x", width=100)
table.column("y", width=100)
table.pack()

root.mainloop()
