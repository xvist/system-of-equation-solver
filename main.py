import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from shapely.geometry import LineString
from shapely.ops import unary_union
import tkinter as tk
from tkinter import ttk, messagebox

# Function to compute values for the two equations on a grid of x and y
# Takes expressions as strings and converts them using eval()
def compute_values(f1, f2, x_range, y_range, step):
    x = np.arange(*x_range, step)  # generate x values
    y = np.arange(*y_range, step)  # generate y values
    X, Y = np.meshgrid(x, y)       # create a 2D grid of coordinates
    Z1 = eval(f1)  # evaluate first equation on the grid
    Z2 = eval(f2)  # evaluate second equation on the grid
    return X, Y, Z1, Z2

# Function to find intersection points of the contour lines (where functions equal zero)
def find_intersections(X, Y, Z1, Z2):
    fig, ax = plt.subplots()
    c1 = ax.contour(X, Y, Z1, levels=[0], colors='none')  # contour for first function
    c2 = ax.contour(X, Y, Z2, levels=[0], colors='none')  # contour for second function
    plt.close(fig)  # close the temporary figure

    def extract_lines(contour):
        lines = []
        for seg in contour.allsegs[0]:  # get all contour segments at level 0
            if len(seg) > 1:
                lines.append(LineString(seg))  # convert segment to a LineString object
        return lines

    lines1 = extract_lines(c1)
    lines2 = extract_lines(c2)

    # Combine all line segments for each equation
    merged1 = unary_union(lines1)
    merged2 = unary_union(lines2)

    # Find intersection of the two sets of contour lines
    intersections = merged1.intersection(merged2)
    return intersections

# Main plotting function triggered by button in GUI
def plot_graphs():
    try:
        # Retrieve values from GUI input fields
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
        # Calculate function values over the grid
        X, Y, Z1, Z2 = compute_values(func1, func2, (x_min, x_max), (y_min, y_max), step)
    except Exception as e:
        messagebox.showerror("Calculation Error", f"Error evaluating functions:\n{e}")
        return

    # Clear previous table content
    for row in table.get_children():
        table.delete(row)

    # Clear previous canvas content
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    # Create 3 side-by-side subplots
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot function values with symbols on the first two plots
    for ax, Z, title in zip(axs[:2], [Z1, Z2], ["Equation 1", "Equation 2"]):
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # Loop over grid and plot symbol depending on sign
        for i in range(Z.shape[0]):
            for j in range(Z.shape[1]):
                symbol = "o" if Z[i, j] > 0 else "x"
                color = "red" if Z[i, j] > 0 else "blue"
                ax.text(X[i, j], Y[i, j], symbol, color=color, ha='center', va='center', fontsize=6)
        ax.contour(X, Y, Z, levels=[0], colors='black')  # draw the zero contour line
        ax.set_title(title)
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    # Find intersections between contour lines
    intersections = find_intersections(X, Y, Z1, Z2)

    # Plot overlapping contours and intersections on third plot
    ax3 = axs[2]
    ax3.contour(X, Y, Z1, levels=[0], colors='red')
    ax3.contour(X, Y, Z2, levels=[0], colors='blue')
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_title("Intersections")
    ax3.grid(True)
    ax3.axis('equal')

    # Mark and save intersection points into table
    if intersections.is_empty:
        messagebox.showinfo("Result", "No intersection points found.")
    elif intersections.geom_type == 'Point':
        ax3.plot(intersections.x, intersections.y, 'ko')
        table.insert("", "end", values=(f"{intersections.x:.4f}", f"{intersections.y:.4f}"))
    elif intersections.geom_type == 'MultiPoint':
        for pt in intersections.geoms:
            ax3.plot(pt.x, pt.y, 'ko')
            table.insert("", "end", values=(f"{pt.x:.4f}", f"{pt.y:.4f}"))

    fig.tight_layout()  # arrange layout of subplots

    # Render the figure inside Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# === GUI Setup ===
root = tk.Tk()
root.title("Equation System Visualizer")

# Input fields for equations and ranges
# Function 1 input
tk.Label(root, text="Function 1 (use X, Y):").grid(row=0, column=0, sticky="e")
func1_entry = tk.Entry(root, width=40)
func1_entry.insert(0, "np.sin(X) + np.cos(Y)")
func1_entry.grid(row=0, column=1)

# Function 2 input
tk.Label(root, text="Function 2 (use X, Y):").grid(row=1, column=0, sticky="e")
func2_entry = tk.Entry(root, width=40)
func2_entry.insert(0, "X**2 - Y")
func2_entry.grid(row=1, column=1)

# Axis limits and step size input
tk.Label(root, text="x min:").grid(row=2, column=0, sticky="e")
x_min_entry = tk.Entry(root)
x_min_entry.insert(0, "-5")
x_min_entry.grid(row=2, column=1)

tk.Label(root, text="x max:").grid(row=3, column=0, sticky="e")
x_max_entry = tk.Entry(root)
x_max_entry.insert(0, "5")
x_max_entry.grid(row=3, column=1)

tk.Label(root, text="y min:").grid(row=4, column=0, sticky="e")
y_min_entry = tk.Entry(root)
y_min_entry.insert(0, "-5")
y_min_entry.grid(row=4, column=1)

tk.Label(root, text="y max:").grid(row=5, column=0, sticky="e")
y_max_entry = tk.Entry(root)
y_max_entry.insert(0, "5")
y_max_entry.grid(row=5, column=1)

tk.Label(root, text="Step:").grid(row=6, column=0, sticky="e")
step_entry = tk.Entry(root)
step_entry.insert(0, "0.3")
step_entry.grid(row=6, column=1)

# Button to trigger plotting
tk.Button(root, text="Plot", command=plot_graphs).grid(row=7, column=0, columnspan=2, pady=10)

# Frame to embed the Matplotlib figure
canvas_frame = tk.Frame(root, width=800, height=400)
canvas_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Table to show coordinates of intersections
tk.Label(root, text="Intersection Points:").grid(row=9, column=0, columnspan=2)
table = ttk.Treeview(root, columns=("x", "y"), show="headings", height=8)
table.heading("x", text="x")
table.heading("y", text="y")
table.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

# Configure adaptive resizing of grid and canvas
root.columnconfigure(1, weight=1)
root.rowconfigure(8, weight=1)
canvas_frame.rowconfigure(0, weight=1)
canvas_frame.columnconfigure(0, weight=1)

# Start the GUI event loop
root.mainloop()
