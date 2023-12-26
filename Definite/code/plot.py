import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot_animation(xs, downsample=100, save=None, title=None, show=False):
    # Downsample each trajectory
    xs = [x[::downsample] for x in xs]
    
    # Ensure that all trajectories have the same length
    lengths = [len(x) for x in xs]
    assert all(l == lengths[0] for l in lengths), "All trajectories should have the same length"
    
    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k']  # A list of colors to use
    
    fig, ax = plt.subplots()
    time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)
    
    lines = []
    for idx, x in enumerate(xs):
        line, = ax.plot([], [], f'-{colors[idx]}', lw=1, label=f'x{idx + 1}')
        lines.append(line)
    
    ax.set_xlim(0, lengths[0])
    ax.set_ylim(min(np.min(x) for x in xs), max(np.max(x) for x in xs))
    ax.set_xlabel('Time step')
    ax.set_ylabel('Position')
    ax.legend()

    # Initialization function
    def init():
        ax.set_xlim(0, lengths[0])
        ax.set_ylim(min(np.min(x) for x in xs) * 0.5 if min(np.min(x) for x in xs) > 0 else min(np.min(x) for x in xs) * 1.5, 
                    max(np.max(x) for x in xs) * 1.5)
        for line in lines:
            line.set_data([], [])
        if title:
            time_text.set_text(f'frequency={title}Hz')
        return lines

    # Animation function
    def animate(i):
        for idx, x in enumerate(xs):
            x_data = np.arange(i + 1)
            y_data = x[:i + 1]
            lines[idx].set_data(x_data, y_data)
        return lines

    anim = FuncAnimation(fig, animate, init_func=init, frames=lengths[0], interval=20, blit=True, repeat=False)
    
    if save:
        anim.save(f'../fig/{save}.gif', writer='pillow', fps=120)
    
    if show:
        plt.show()

    return anim  # Return the animation object for further manipulations if needed


import numpy as np
import matplotlib.pyplot as plt

def plot_static(xs, length, title=None, save=None, show=True):

    # Define colors for plotting
    colors = ['r', 'b', 'g', 'c', 'm', 'y', 'k']

    # Create a plot
    fig, ax = plt.subplots()

    # Plot each trajectory
    for idx, x in enumerate(xs):
        ax.plot(np.linspace(0, length, len(x)), x, f'-{colors[idx]}', lw=1, label=f'x{idx + 1}')

    # Set plot properties
    ax.set_xlim(0, length)
    ax.set_ylim(min(np.min(x) for x in xs) * 0.5 if min(np.min(x) for x in xs) > 0 else min(np.min(x) for x in xs) * 1.5, 
                    max(np.max(x) for x in xs) * 1.5)
    ax.set_xlabel('Time')
    ax.set_ylabel('Position')
    if title:
        ax.set_title(title)
    ax.legend()

    # Save the plot if required
    if save:
        plt.savefig(f'../fig/{save}.png')

    # Show the plot
    if show:
        plt.show()

