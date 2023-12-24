import numpy as np
import matplotlib.pyplot as plt

def velocity_distribution(velocities, bins=10, save=False, filename='velocity_distribution.png'):
    # 计算所有粒子速度的大小
    speeds = np.linalg.norm(velocities, axis=1)

    # 计算直方图
    distribution, bin_edges = np.histogram(speeds, bins=bins, density=True)

    # 返回bin中心和对应的分布密度
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.figure(figsize=(8, 6))
    plt.bar(bin_centers, distribution, width=bin_centers[1] - bin_centers[0])
    plt.xlabel('Speed')
    plt.ylabel('Density')
    plt.title('Velocity Distribution')
    if save:
        plt.savefig(filename)
    plt.show()
    