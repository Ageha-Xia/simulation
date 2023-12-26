import numpy as np
import pandas as pd
import argparse
import oscillation
from plot import *
from tqdm import tqdm
from scipy.signal import find_peaks
from concurrent.futures import ProcessPoolExecutor

def Step_Response(save=False, show=True, disable_tqdm=False):
    x1 = 0
    v1 = 0
    x2 = 1
    v2 = 1
    
    M1 = 500
    M2 = 50
    K1 = 20000
    K2 = 200000
    C = 200
    t = 10
    dt = 1e-2
    steps = int(t / dt)

    len1 = 10
    len2 = 10
    
    s1 = oscillation.String(x_l=len2 + x2, x_r=len2 + len1 + x1, length=len1, k=K1)
    s2 = oscillation.String(x_l=0, x_r=len2 + x2, length=len2, k=K2)
    
    d1 = oscillation.Damper(v_l=v2, v_r=v1, damping=C)
    
    m1 = oscillation.Object(x0=len2 + len1 + x1, v0=v1, m=M1, max_steps=steps)
    m2 = oscillation.Object(x0=len2 + x2, v0=v2, m=M2, max_steps=steps)

    m2.link(s2, pos='r')
    m2.link(d1, pos='l')
    m2.link(s1, pos='l')
    m1.link(d1, pos='r')
    m1.link(s1, pos='r')

    system = oscillation.System(objects=[m1, m2], strings=[s1, s2], dampers=[d1])
    system.run(dt, steps, disable_tqdm)
    
    a1 = (np.max(m1.x) - np.min(m1.x)) / 2
    a2 = (np.max(m2.x) - np.min(m2.x)) / 2

    def find_period(x):
        peaks, _ = find_peaks(x)
        return np.mean(np.diff(peaks)) * dt

    t1 = find_period(m1.x)
    t2 = find_period(m2.x)
    if save or show:
        print(f'Amplitude of m1: {a1:.4f} m, period: {t1:.4f} s')
        print(f'Amplitude of m2: {a2:.4f} m, period: {t2:.4f} s')
        plot_static([m1.x - len1 - len2, m2.x - len2], t, save=save, show=show)
        
    return (a1, a2, t1, t2)


def Sine_Response(A, f, save=False, show=True, disable_tqdm=False):
    x1 = 0
    v1 = 0
    x2 = 1
    v2 = 1
    
    M1 = 500
    M2 = 50
    K1 = 20000
    K2 = 200000
    C = 200
    t = 10
    dt = 1e-2
    steps = int(t / dt)

    len1 = 10
    len2 = 10
    
    s1 = oscillation.String(x_l=len2 + x2, x_r=len2 + len1 + x1, length=len1, k=K1)
    s2 = oscillation.String(x_l=0, x_r=len2 + x2, length=len2, k=K2)
    
    d1 = oscillation.Damper(v_l=v2, v_r=v1, damping=C)
    
    m1 = oscillation.Object(x0=len2 + len1 + x1, v0=v1, m=M1, max_steps=steps)
    m2 = oscillation.Object(x0=len2 + x2, v0=v2, m=M2, max_steps=steps)

    force = oscillation.Force_Sin(A=A, f=f, phi=np.pi / 2)
    
    m2.link(s2, pos='r')
    m2.link(d1, pos='l')
    m2.link(s1, pos='l')
    m1.link(d1, pos='r')
    m1.link(s1, pos='r')
    m2.add_force(force)

    system = oscillation.System(objects=[m1, m2], strings=[s1, s2], dampers=[d1])
    system.run(dt, steps, disable_tqdm)
    
    a1 = (np.max(m1.x[len(m1.x) // 2:]) - np.min(m1.x[len(m1.x) // 2:])) / 2
    a2 = (np.max(m2.x[len(m2.x) // 2:]) - np.min(m2.x[len(m2.x) // 2:])) / 2

    def find_period(x):
        peaks, _ = find_peaks(x)
        return np.mean(np.diff(peaks)) * dt

    t1 = find_period(m1.x)
    t2 = find_period(m2.x)
    if save or show:
        print(f'Amplitude of m1: {a1:.4f} m, period: {t1:.4f} s')
        print(f'Amplitude of m2: {a2:.4f} m, period: {t2:.4f} s')
        plot_static([m1.x - len1 - len2, m2.x - len2], t, save=save, show=show)
        
    return (a1, a2, t1, t2)

def wrapper(args):
    return Sine_Response(*args)

def Multi_Sine_Response():
    fs = np.arange(0, 15, 0.001)
    a1s = np.zeros_like(fs)
    a2s = np.zeros_like(fs)
    t1s = np.zeros_like(fs)
    t2s = np.zeros_like(fs)
    
    args = [(1000, f, False, False, True) for f in fs]
    
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(wrapper, args), total=len(fs)))

    a1s, a2s, t1s, t2s = zip(*results)
    
    df = pd.DataFrame({
        'f': fs,
        'a1': a1s,
        'a2': a2s,
        't1': t1s,
        't2': t2s
    })
    df.round(4).to_csv('../report/Sine_Response.csv', index=False)
    
if __name__ == "__main__":
    # Step_Response()
    # Sine_Response(A=1000, f=10.555)
    Multi_Sine_Response()