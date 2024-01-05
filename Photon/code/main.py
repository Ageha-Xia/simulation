import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from photon import Photon
from scipy.signal import find_peaks

n = int(1e5)
H = 4
E0 = 0.662
E_Ds = []
E_Detects = []
Nm = 0

for i in tqdm(range(n)):
    photon = Photon(np.array([0, 0, H]), E0, np.array([0, 0, -1]), H=H, R=2)
    E_D = photon.simulate()
    if E_D > 0: # The undetected photon should be ignored
        Nm += 1
        E_Ds.append(E_D)
        F = 0.01 + 0.05 * np.sqrt(E_D + 0.4 * E_D ** 2)
        sigma = 0.4247 * F
        x = np.random.randn()
        E_Detects.append(E_D + sigma * x)   # The detected energy is a random variable influced by the energy fluctuation
        
print(f'Efficiency:{Nm / n}')
sigma0 = 0.4247 * (0.01 + 0.05 * np.sqrt(E0 + 0.4 * E0 ** 2))
Np = np.count_nonzero((E_Ds >= E0 - 3 * sigma0) & (E_Ds <= E0 + 3 * sigma0))
print(f'Peak total ratio:{Np / n}')

E_Detects = np.array(E_Detects)
bins = np.arange(0, 0.85, 0.002)  # 生成bins数组，从0开始，0.85结束，步长为0.002

plt.hist(E_Detects, bins=bins, density=True)
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.xlim([0, 0.85])
plt.savefig('../fig/E_D_distribution.png')
plt.clf()

counts, bin_edges = np.histogram(E_Detects, bins=200)
bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

# 找到峰值
peaks, _ = find_peaks(counts)
peak = peaks[np.argmax(counts[peaks])]  # 最大峰值位置

# 找到峰值对应的半高度
half_max = counts[peak] / 2

# 找到峰值左侧和右侧的半高宽位置
left_idx = np.where(counts[:peak] < half_max)[0][-1]
right_idx = np.where(counts[peak:] < half_max)[0][0] + peak

# 计算半高宽
fwhm = bin_centers[right_idx] - bin_centers[left_idx]
print(f'L:{bin_centers[left_idx]}, R:{bin_centers[right_idx]}')
# 输出结果和绘图
print(f"FWHM: {fwhm}")
plt.bar(bin_centers, counts, width=bin_edges[1]-bin_edges[0], edgecolor='black')
plt.plot(bin_centers[peaks], counts[peaks], "x")
plt.axhline(y=half_max, color='r', linestyle='--')
plt.axvline(x=bin_centers[left_idx], color='g', linestyle='--')
plt.axvline(x=bin_centers[right_idx], color='g', linestyle='--')
plt.xlabel('Energy')
plt.ylabel('Counts')
plt.title('Energy Spectrum with FWHM')
plt.savefig('../fig/E_D_spectrum_with_FWHM.png')

