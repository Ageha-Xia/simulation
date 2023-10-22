import numpy as np
from objects import Object
from strings import String
from forces import Force
from plot import plot
from tqdm import tqdm
from scipy.signal import find_peaks

def p1_1():
    t = 100
    dt = 1e-4
    steps = int(t / dt)


    len1 = 10
    len2 = 10

    f = 2.022 * 2 * np.pi
    force = Force(5, f, 0)

    s1 = String(l=0, r=len1, length=len1, k=600)
    s2 = String(l=len1, r=len1 + len2, length=len2, k=1000)
    m1 = Object(x0=len1, v0=0, m=20, max_steps=steps)
    m2 = Object(x0=len1 + len2, v0=0, m=10, max_steps=steps)

    m1.link(s1, pos='r')
    m1.link(s2, pos='l')
    m2.link(s2, pos='r')
    m2.add_force(force)

    m1.init(dt)
    m2.init(dt)

    for i in range(2, steps):
        m1.update(dt)
        m2.update(dt)

    a1 = (np.max(m1.x) - np.min(m1.x)) / 2
    a2 = (np.max(m2.x) - np.min(m2.x)) / 2

    def find_period(x):
        peaks, _ = find_peaks(x)
        return np.mean(np.diff(peaks)) * dt

    t1 = find_period(m1.x)
    t2 = find_period(m2.x)
    print(f'Amplitude of m1: {a1:.4f} m, period: {t1:.4f} s')
    print(f'Amplitude of m2: {a2:.4f} m, period: {t2:.4f} s')

    plot(m1.x, m2.x, int(0.1 / dt), save='resonance, f=2.022Hz', title=f / (2 * np.pi))

if __name__ == "__main__":
    p1_1()

