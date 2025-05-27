import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import LineString
from shapely.ops import unary_union
import tkinter as tk
from tkinter import ttk, messagebox

# ==== Appropriation and computing values from GUI ====
def compute_values(f1, f2, x_range, y_range, step):
    x = np.arange(*x_range, step)
    y = np.arange(*y_range, step)
    X, Y = np.meshgrid(x, y)
    Z1 = eval(f1)
    Z2 = eval(f2)
    return X, Y, Z1, Z2

# ==== Finding intersection points ====
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

# ==== Plotting ====
def plot_graphs():
    try:
        x_min = float(x_min_entry.get())    # x_min value appropriation from GUI
        x_max = float(x_max_entry.get())    # x_max value appropriation from GUI
        y_min = float(y_min_entry.get())    # y_min value appropriation from GUI
        y_max = float(y_max_entry.get())    # y_max value appropriation from GUI
        step = float(step_entry.get())      # Step value appropriation from GUI
        func1 = func1_entry.get()           # Function 1 appropriation from GUI
        func2 = func2_entry.get()           # Function 2 appropriation from GUI
    except Exception as e:
        messagebox.showerror("Input Error", str(e))     # Handling possible errors
        return

    try:
        X, Y, Z1, Z2 = compute_values(func1, func2, (x_min, x_max), (y_min, y_max), step)   # Compute values
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Error evaluating functions:\n{e}")  # Handling possible errors
        return

    for row in table.get_children():
        table.delete(row)   # Cleaning table

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))      # Initializing fist figure with values "x" and "o"
    for ax, Z, title in zip(axs, [Z1, Z2], ["Equation 1", "Equation 2"]):
        ax.set_xlabel("x")      # Set Ox label
        ax.set_ylabel("y")      # Set Oy label
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                symbol = "o" if Z[i, j] > 0 else "x"    # Assigning a symbol to a value depending on the sign
                color = "red" if Z[i, j] > 0 else "blue"    # Assigning a color to a value depending on the sign
                ax.text(X[i, j], Y[i, j], symbol, color=color, ha='center', va='center', fontsize=8)    # Symbol setup
        ax.contour(X, Y, Z, levels=[0], colors='black')     # Set coordinate plane
        ax.set_title(title)     # Set title
        ax.set_xlim(x_min, x_max)   # Set x axes values
        ax.set_ylim(y_min, y_max)   # Set y axes values

    plt.tight_layout()
    plt.show()  # Show figure 1

    intersections = find_intersections(X, Y, Z1, Z2)    # Intersection finding

    fig2, ax2 = plt.subplots(figsize=(6, 6))    # Initializing second figure
    ax2.contour(X, Y, Z1, levels=[0], colors='red')     # Adding first graphic intersection
    ax2.contour(X, Y, Z2, levels=[0], colors='blue')    # Adding second graphic intersection

    if intersections.is_empty:
        messagebox.showinfo("Result", "No intersection points found.")      # Message if no intersection points found
    elif intersections.geom_type == 'Point':        # Main logic if graphs has only one intersection point
        ax2.plot(intersections.x, intersections.y, 'ko')    # Adding points is graph
        table.insert("", "end", values=(f"{intersections.x:.4f}", f"{intersections.y:.4f}"))    # Adding points in table
    elif intersections.geom_type == 'MultiPoint':   # Main logic if graphs has multiple intersection points
        for pt in intersections.geoms:
            ax2.plot(pt.x, pt.y, 'ko')  # Adding points is graph
            table.insert("", "end", values=(f"{pt.x:.4f}", f"{pt.y:.4f}"))  # Adding points in table

    ax2.set_xlabel("x")     # Set Ox label for figure 2
    ax2.set_ylabel("y")     # Set Oy label for figure 2
    ax2.set_title("Intersection Points")    # Set title for figure 2
    ax2.grid(True)      # Set grid
    ax2.axis('equal')
    plt.tight_layout()
    plt.show()

# ==== GUI ====
root = tk.Tk()  # Initialization window
root.title("Equation System Visualizer")    # Select window name

tk.Label(root, text="Function 1 (use X, Y):").grid(row=0, column=0) # Label for func 1
func1_entry = tk.Entry(root, width=40)  # Textbox for func 1
func1_entry.insert(0, "np.sin(X) + np.cos(Y)")  # Preinsert func 1
func1_entry.grid(row=0, column=1)   # Func 1 textbox placement

tk.Label(root, text="Function 2 (use X, Y):").grid(row=1, column=0) # Label for func 1
func2_entry = tk.Entry(root, width=40)  # Textbox for func 2
func2_entry.insert(0, "X**2 - Y")   # Preinsert func 2
func2_entry.grid(row=1, column=1)   # Func 2 textbox placement

tk.Label(root, text="x min:").grid(row=2, column=0) # Label for x_min value
x_min_entry = tk.Entry(root)    # Textbox for x_min value
x_min_entry.insert(0, "-5") # Preinsert x_min
x_min_entry.grid(row=2, column=1)   # x_min textbox placement

tk.Label(root, text="x max:").grid(row=3, column=0) # Label for x_max value
x_max_entry = tk.Entry(root)    # Textbox for x_max value
x_max_entry.insert(0, "5")  # Preinsert x_max
x_max_entry.grid(row=3, column=1)   # x_max textbox placement

tk.Label(root, text="y min:").grid(row=4, column=0) # Label for y_min value
y_min_entry = tk.Entry(root)    # Textbox for y_min value
y_min_entry.insert(0, "-5") # Preinsert y_min
y_min_entry.grid(row=4, column=1)   # y_min textbox placement

tk.Label(root, text="y max:").grid(row=5, column=0) # Label for y_max value
y_max_entry = tk.Entry(root)    # Textbox for y_max value
y_max_entry.insert(0, "5")  # Preinsert y_max
y_max_entry.grid(row=5, column=1)   # y_max textbox placement

tk.Label(root, text="Step:").grid(row=6, column=0)  # Label for step value
step_entry = tk.Entry(root) # Textbox for step value
step_entry.insert(0, "0.3") # Preinsert step
step_entry.grid(row=6, column=1)    # Step textbox placement

tk.Button(root, text="Plot", command=plot_graphs).grid(row=7, column=0, columnspan=2, pady=10)  # "Build" button placement

tk.Label(root, text="Intersection Points:").grid(row=8, column=0, columnspan=2) # Table name and placement
table = ttk.Treeview(root, columns=("x", "y"), show="headings", height=8)   # Columnarization
table.heading("x", text="x")    # Column 1 label
table.heading("y", text="y")    # Column 2 label
table.grid(row=9, column=0, columnspan=2, padx=10, pady=10) # Table front

root.mainloop()
