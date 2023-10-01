import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from planet_motion import PlanetSystem

def plot(rs, delta_t=100, save=False):
    downsample = 5000 // delta_t
    rs = rs[::downsample]
    
    fig, ax = plt.subplots()
    ax.set_aspect('equal')  # 设置纵横比使x和y轴的刻度一致
    size = 6
    fig.set_size_inches(size, size)
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'r-', animated=True)  # 'r-' 表示红色实线
    point, = plt.plot([], [], 'bo', animated=True)  # 'bo' 表示蓝色圆点
    
    def init():
        r = 2e11
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
    
    ani = FuncAnimation(fig, update, frames=range(len(rs)), init_func=init, blit=True, interval=1, repeat=False)
    if save:
        ani.save('Planet_Motion.gif', writer='pillow', fps=1000)
        
    plt.show()