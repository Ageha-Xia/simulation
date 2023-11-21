import numpy as np
import platform
import matplotlib.pyplot as plt
from numba import jit

if platform.system() == 'Windows':
    plt.rcParams["font.sans-serif"]=["SimHei"] 
    plt.rcParams["axes.unicode_minus"]=False 
elif platform.system() == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['Hiragino Sans GB'] 
    plt.rcParams['font.size'] = 15  
    plt.rcParams['axes.unicode_minus'] = False

n = int(1e6)
m = int(1e4)
a = 4
l = 3

@jit(nopython=True)
def get_pis():
    count = 0
    fs = np.zeros(n // m)
    pis = np.zeros(n // m)

    for i in range(n + 1):
        # 生成随机角度
        theta = np.random.uniform(0, np.pi)
        # 生成随机位置
        x = np.random.uniform(0, a)
        # 判断是否相交
        if x <= l * np.sin(theta):
            count += 1
        
        if i % m == 0 and i != 0:
            # 计算频率和pi的估计值
            f = count / (i + 1)
            fs[i // m - 1] = f
            if f != 0:
                pi = 2 * l / (a * f)
                pis[i // m - 1] = pi
    
    return fs, pis

fs, pis = get_pis()

@jit(nopython=True)
def get_error():
    delta_pis = np.zeros(n // m)
    ideal_delta_pis = np.zeros(n // m)
    
    for i in range(n // m):
        delta_pis[i] = np.abs(pis[i] - np.pi)
        p = 2 * l / (np.pi * a)
        ideal_delta_pis[i] = 2 * np.pi * np.sqrt((1 - p) / (m * (i + 1) * p))
    
    return delta_pis, ideal_delta_pis

delta_pis, ideal_delta_pis = get_error()

print(f"pi = {pis[-1]}")

# 绘制 pi 的估计值
plt.figure(figsize=(10, 6))
plt.plot(np.arange(n // m), pis)
plt.title("π 的估计值随时间的变化")
plt.xlabel("试验次数")
plt.ylabel("π 的估计值")
plt.savefig('../figs/pi_estimation.png')  # 保存为图片
plt.show()

# 绘制理论误差和实际误差
plt.figure(figsize=(10, 6))
plt.plot(np.arange(n // m), delta_pis, label='实际误差', color='blue')
plt.plot(np.arange(n // m), ideal_delta_pis, label='理论误差', color='red')
plt.title("理论误差与实际误差随时间的变化")
plt.xlabel("试验次数")
plt.ylabel("误差值")
plt.legend()
plt.savefig('../figs/error_comparison.png')
plt.show()