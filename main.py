import numpy as np
import matplotlib.pyplot as plt

# === Mash setup ===
x_min, x_max, x_steps = -5, 5, 100
y_min, y_max, y_steps = -5, 5, 100

x_vals = np.linspace(x_min, x_max, x_steps)
y_vals = np.linspace(y_min, y_max, y_steps)
X, Y = np.meshgrid(x_vals, y_vals)

# === System of equation setup ===
def equation1(x, y):
    return x**2 + y**2 - 4  # Circle radius 2

def equation2(x, y):
    return x - y**2         # Parabola y = sqrt(x)

Z1 = equation1(X, Y)
Z2 = equation2(X, Y)

# === Plot building method ===
def plot_equation(Z, title, subplot_index):
    plt.subplot(1, 2, subplot_index)
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            if Z[i, j] > 0:
                plt.text(x_vals[j], y_vals[i], 'o', color='red', ha='center', va='center', fontsize=6)
            elif Z[i, j] < 0:
                plt.text(x_vals[j], y_vals[i], 'x', color='blue', ha='center', va='center', fontsize=6)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.axis('equal')

# === Plot building ===
plt.figure(figsize=(12, 6))
plot_equation(Z1, 'Equation 1', 1)
plot_equation(Z2, 'Equation 2', 2)
plt.tight_layout()
plt.show()
