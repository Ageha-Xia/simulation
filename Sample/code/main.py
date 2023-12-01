import numpy as np
import matplotlib.pyplot as plt
import argparse
import time
from numba import jit

@jit(nopython=True)
def f(x):
    return (1 + x) / 2

@jit(nopython=True)
def F_(x):
    return -1 + 2 * np.sqrt(x)

@jit(nopython=True)
def directly_sample(n):
    xs = np.zeros(n)
    for i in range(n):
        eps = np.random.uniform(0, 1)
        xs[i] = F_(eps)
    return xs

@jit(nopython=True)
def select_sample(n):
    xs = np.zeros(n)
    # we use h(x) = 1/2 to generate the samples
    i = 0
    while i < n:
        eps = np.random.uniform(0, 1)
        x = np.random.uniform(-1, 1)
        if eps <= f(x):
            xs[i] = x
            i = i + 1
    return xs

# Sample size
n = int(1e8)

parser = argparse.ArgumentParser(description='Execute selecting method')
parser.add_argument('--method', type=str, default='direct', nargs='?', help='Method to generate samples, direct or select') 
args = parser.parse_args()

time_start = time.perf_counter()
# Generating samples
if args.method == 'direct':
    xs = directly_sample(n)
elif args.method == 'select':
    xs = select_sample(n)
else:
    print('Invalid method')
    exit()
time_end = time.perf_counter()
duration = time_end - time_start
print(f"Time elapsed: {duration:.4f}s")

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
plt.savefig(f'../fig/{args.method}_distribution.png')
plt.show()


