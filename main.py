import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import LineString
from shapely.ops import unary_union
import tkinter as tk
from tkinter import ttk, messagebox

def compute_values(f1, f2, x_range, y_range, step):
    x = np.arange(*x_range, step)
    y = np.arange(*y_range, step)
    X, Y = np.meshgrid(x, y)
    Z1 = eval(f1)
    Z2 = eval(f2)
    return X, Y, Z1, Z2

def find_intersections(X, Y, Z1, Z2):
    fig, ax = plt.subplots()
    c1 = ax.contour(X, Y, Z1, levels=[0], colors='none')
    c2 = ax.contour(X, Y, Z2, levels=[0], colors='none')
    plt.close(fig)

    def extract_lines(contour):
        lines = []
        for seg in contour.allsegs[0]:
            if len(seg) > 1:
                lines.append(LineString(seg))
        return lines

    lines1 = extract_lines(c1)
    lines2 = extract_lines(c2)

    merged1 = unary_union(lines1)
    merged2 = unary_union(lines2)

    intersections = merged1.intersection(merged2)
    return intersections

def plot_graphs():
    try:
        x_min = float(x_min_entry.get())
        x_max = float(x_max_entry.get())
        y_min = float(y_min_entry.get())
        y_max = float(y_max_entry.get())
        step = float(step_entry.get())
        func1 = func1_entry.get()
        func2 = func2_entry.get()
    except Exception as e:
        messagebox.showerror("Input Error", str(e))
        return

    try:
        X, Y, Z1, Z2 = compute_values(func1, func2, (x_min, x_max), (y_min, y_max), step)
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Error evaluating functions:\n{e}")
        return

    for row in table.get_children():
        table.delete(row)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    for ax, Z, title in zip(axs, [Z1, Z2], ["Equation 1", "Equation 2"]):
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                symbol = "o" if Z[i, j] > 0 else "x"
                color = "red" if Z[i, j] > 0 else "blue"
                ax.text(X[i, j], Y[i, j], symbol, color=color, ha='center', va='center', fontsize=8)
        ax.contour(X, Y, Z, levels=[0], colors='black')
        ax.set_title(title)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    plt.tight_layout()
    plt.show()

    intersections = find_intersections(X, Y, Z1, Z2)

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.contour(X, Y, Z1, levels=[0], colors='red')
    ax2.contour(X, Y, Z2, levels=[0], colors='blue')

    if intersections.is_empty:
        messagebox.showinfo("Result", "No intersection points found.")
    elif intersections.geom_type == 'Point':
        ax2.plot(intersections.x, intersections.y, 'ko')
        table.insert("", "end", values=(f"{intersections.x:.4f}", f"{intersections.y:.4f}"))
    elif intersections.geom_type == 'MultiPoint':
        for pt in intersections.geoms:
            ax2.plot(pt.x, pt.y, 'ko')
            table.insert("", "end", values=(f"{pt.x:.4f}", f"{pt.y:.4f}"))

    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_title("Intersection Points")
    ax2.grid(True)
    ax2.axis('equal')
    plt.tight_layout()
    plt.show()

# GUI
root = tk.Tk()
root.title("Equation System Visualizer")

tk.Label(root, text="Function 1 (use X, Y):").grid(row=0, column=0)
func1_entry = tk.Entry(root, width=40)
func1_entry.insert(0, "np.sin(X) + np.cos(Y)")
func1_entry.grid(row=0, column=1)

tk.Label(root, text="Function 2 (use X, Y):").grid(row=1, column=0)
func2_entry = tk.Entry(root, width=40)
func2_entry.insert(0, "X**2 - Y")
func2_entry.grid(row=1, column=1)

tk.Label(root, text="x min:").grid(row=2, column=0)
x_min_entry = tk.Entry(root)
x_min_entry.insert(0, "-5")
x_min_entry.grid(row=2, column=1)

tk.Label(root, text="x max:").grid(row=3, column=0)
x_max_entry = tk.Entry(root)
x_max_entry.insert(0, "5")
x_max_entry.grid(row=3, column=1)

tk.Label(root, text="y min:").grid(row=4, column=0)
y_min_entry = tk.Entry(root)
y_min_entry.insert(0, "-5")
y_min_entry.grid(row=4, column=1)

tk.Label(root, text="y max:").grid(row=5, column=0)
y_max_entry = tk.Entry(root)
y_max_entry.insert(0, "5")
y_max_entry.grid(row=5, column=1)

tk.Label(root, text="Step:").grid(row=6, column=0)
step_entry = tk.Entry(root)
step_entry.insert(0, "0.3")
step_entry.grid(row=6, column=1)

tk.Button(root, text="Plot", command=plot_graphs).grid(row=7, column=0, columnspan=2, pady=10)

tk.Label(root, text="Intersection Points:").grid(row=8, column=0, columnspan=2)
table = ttk.Treeview(root, columns=("x", "y"), show="headings", height=8)
table.heading("x", text="x")
table.heading("y", text="y")
table.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
