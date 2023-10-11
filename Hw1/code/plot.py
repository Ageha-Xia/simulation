import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def rounded_max_abs_value(arr):
    max_abs_val = np.max(np.abs(arr))
    
    # calculate the magnitude
    order_of_magnitude = 10 ** (int(np.log10(max_abs_val)))
    
    # get the ceiling number with figure divided by magnitude
    rounded_value = np.ceil(max_abs_val / order_of_magnitude) * order_of_magnitude
    
    return int(rounded_value)

def plot(rs, downsample, save=None, title=None):
    rs = rs[::downsample]
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  
    size = 6
    fig.set_size_inches(size, size)
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'r-', animated=True)
    point, = plt.plot([], [], 'bo', animated=True)
    
    def init():
        r = rounded_max_abs_value(rs)
        ax.set_xlim(-r, r)  
        ax.set_ylim(-r, r)  
        # 添加文本在左下角
        if title:
            text = ax.text(0.02, 0.02, title, transform=ax.transAxes)
            return [ln, text]
        return [ln]

    def update(frame):
        x, y = rs[frame]  
        xdata.append(x)
        ydata.append(y)
        ln.set_data(xdata, ydata)
        point.set_data([x], [y])  
        return ln, point,
    
    ani = FuncAnimation(fig, update, frames=range(len(rs)), init_func=init, blit=True, interval=20, repeat=False)
    if save:
        ani.save(f'./fig/{save}.gif', writer='pillow', fps=120)
        
    plt.show()

