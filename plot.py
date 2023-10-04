import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from planet import PlanetSystem

def rounded_max_abs_value(arr):
    max_abs_val = np.max(np.abs(arr))
    
    # calculate the magnitude
    order_of_magnitude = 10 ** (int(np.log10(max_abs_val)))
    
    # get the ceiling number with figure divided by magnitude
    rounded_value = np.ceil(max_abs_val / order_of_magnitude) * order_of_magnitude
    
    return int(rounded_value)

def plot(rs, downsample, save=None, magnitude=None):
    rs = rs[::downsample]
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  # 设置纵横比使x和y轴的刻度一致
    size = 6
    fig.set_size_inches(size, size)
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'r-', animated=True)  # 'r-' 表示红色实线
    point, = plt.plot([], [], 'bo', animated=True)  # 'bo' 表示蓝色圆点
    
    def init():
        if magnitude:
            r = magnitude
        else:
            r = rounded_max_abs_value(rs)
        ax.set_xlim(-r, r)  # 设置x轴的范围
        ax.set_ylim(-r, r)  # 设置y轴的范围
        return ln,

    def update(frame):
        x, y = rs[frame]  # 获取当前帧的坐标
        xdata.append(x)
        ydata.append(y)
        ln.set_data(xdata, ydata)
        point.set_data([x], [y])  # 在当前帧的位置画一个小圆点
        return ln, point,
    
    ani = FuncAnimation(fig, update, frames=range(len(rs)), init_func=init, blit=True, interval=20, repeat=False)
    if save:
        ani.save(f'{save}.gif', writer='pillow', fps=60)
        
    plt.show()