import numpy as np
import matplotlib.pyplot as plt
from numba import jit

@jit(nopython=True)
def f(x):
    return (1 + x) / 2

@jit(nopython=True)
def F_(x):
    return -1 + 2 * np.sqrt(x)

@jit(nopython=True)
def generate_samples(n):
    xs = np.zeros(n)
    for i in range(n):
        eps = np.random.uniform(0, 1)
        xs[i] = F_(eps)
    return xs

# Sample size
n = int(1e7)

# Generating samples
xs = generate_samples(n)

# Plotting the empirical distribution
plt.figure(figsize=(10, 6))
plt.hist(xs, bins=1000, density=True, alpha=0.5, label='Empirical Distribution')

# Plotting the theoretical distribution
x_theoretical = np.linspace(-1, 1, 1000)  # Adjusted for the range of x
y_theoretical = f(x_theoretical)
plt.plot(x_theoretical, y_theoretical, 'r', label='Theoretical Distribution $f(x)$')

# Labeling the plot
plt.xlabel('x')
plt.ylabel('Density')
plt.title('Comparison of Empirical and Theoretical Distributions')
plt.legend()
plt.grid(True)
plt.savefig('../fig/distribution.png')
plt.show()
