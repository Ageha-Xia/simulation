import numpy as np
import pandas as pd
from objects import Object
from strings import String
from forces import *
from plot import plot
from tqdm import tqdm
from scipy.signal import find_peaks

def double_spring_oscillator(f=0.68614):
    t = 100
    dt = 1e-5
    steps = int(t / dt)


    len1 = 10
    len2 = 10

    # force = Force_Sin(5, f, 0)
    force = Force_Square(f, 5)

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

    # plot(m1.x, m2.x, int(0.1 / dt), save=f'resonance, f={f}Hz, square_wave', title=f, show=True)
    return (a1, a2, t1, t2)

def p1_1():
    f1 = np.arange(0.4, 0.8 + 0.05, 0.01)
    f2 = np.arange(1.8, 2.2 + 0.05, 0.01)
    fs = np.concatenate((f1, f2))
    a1s = np.zeros_like(fs)
    a2s = np.zeros_like(fs)
    t1s = np.zeros_like(fs)
    t2s = np.zeros_like(fs)
    
    for i in tqdm(range(len(fs))):
        f = fs[i] * 2 * np.pi
        a1s[i], a2s[i], t1s[i], t2s[i] = double_spring_oscillator(f)
    
    df = pd.DataFrame({
        'f': fs,
        'a1': a1s,
        'a2': a2s,
        't1': t1s,
        't2': t2s
    })
    df.round(4).to_csv('../report/p1_1_data.csv', index=False)
    
if __name__ == "__main__":
    p1_1()
    # double_spring_oscillator(2.022)