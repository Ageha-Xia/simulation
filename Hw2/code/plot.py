import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def plot(x1, x2, downsample=100, save=None, title=None):
    x1 = x1[::downsample]
    x2 = x2[::downsample]
    # Ensure that x1 and x2 have the same shape
    assert x1.shape == x2.shape, "Both trajectories should have the same shape"
    
    # Setting up the figure, the axis, and the plot element we want to animate
    fig, ax = plt.subplots()
    time_text = ax.text(0.05, 0.95, '', transform=ax.transAxes)
    line1, = ax.plot([], [], 'r-', lw=1, label='M')
    line2, = ax.plot([], [], 'b-', lw=1, label='m')
    ax.set_xlim(0, len(x1))
    ax.set_ylim(min(min(x1), min(x2)), max(max(x1), max(x2)))
    ax.set_xlabel('Time step')
    ax.set_ylabel('Position')
    ax.legend()

    # Initialization function: plot the background of each frame
    def init():
        ax.set_xlim(0, len(x1))  
        ax.set_ylim(min(min(min(x1), min(x2)) * 0.5, min(min(x1), min(x2)) * 1.5), max(max(x1), max(x2)) * 1.5)  
        line1.set_data([], [])
        line2.set_data([], [])
        if title:
            time_text.set_text(f'frequency={title}Hz')
        return line1, line2,

    # Animation function which updates figure data. This is called sequentially
    def animate(i):
        x = np.arange(i + 1)
        y1 = x1[:i + 1]
        y2 = x2[:i + 1]
        line1.set_data(x, y1)
        line2.set_data(x, y2)
        return line1, line2,

    # Call the animator.
    anim = FuncAnimation(fig, animate, init_func=init, frames=len(x1), interval=20, blit=True, repeat=False)
    if save:
        anim.save(f'../fig/{save}.gif', writer='pillow', fps=120)
    # plt.show()