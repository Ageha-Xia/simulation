import numpy as np
import pandas as pd
import argparse
from objects import Object
from strings import String
from forces import *
from plot import plot
from tqdm import tqdm
from scipy.signal import find_peaks
from concurrent.futures import ProcessPoolExecutor

def double_spring_oscillator(f=0.68614, drive='sin', save=False, show=True):
    t = 100
    dt = 1e-4
    steps = int(t / dt)


    len1 = 10
    len2 = 10

    if drive == 'sin':
        force = Force_Sin(5, f, 0)
    elif drive == 'square':
        force = Force_Square(5, f)

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
    if save or show:
        print(f'Amplitude of m1: {a1:.4f} m, period: {t1:.4f} s')
        print(f'Amplitude of m2: {a2:.4f} m, period: {t2:.4f} s')

    plot([m1.x, m2.x], int(0.1 / dt), save=f'resonance, f={f}Hz, {drive}_wave' if save else None, 
         title=f if save else None, show=show)
    return (a1, a2, t1, t2)

def wrapper(args):
    return double_spring_oscillator(*args)

def p1_1():
    f1 = np.arange(0.4, 0.8 + 0.05, 0.01)
    f2 = np.arange(1.8, 2.2 + 0.05, 0.01)
    fs = np.concatenate((f1, f2))
    a1s = np.zeros_like(fs)
    a2s = np.zeros_like(fs)
    t1s = np.zeros_like(fs)
    t2s = np.zeros_like(fs)
    
    # for i in tqdm(range(len(fs))):
    #     f = fs[i]
    #     a1s[i], a2s[i], t1s[i], t2s[i] = double_spring_oscillator(f, 'sin', False, False)
    args = [(f, 'sin', False, False) for f in fs]
    
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
    df.round(4).to_csv('../report/p1_1_data_sin.csv', index=False)

def p1_2():
    f1 = np.arange(0.4, 0.8 + 0.05, 0.01)
    f2 = np.arange(1.8, 2.2 + 0.05, 0.01)
    fs = np.concatenate((f1, f2))
    a1s = np.zeros_like(fs)
    a2s = np.zeros_like(fs)
    t1s = np.zeros_like(fs)
    t2s = np.zeros_like(fs)
    
    args = [(f, 'square', False, False) for f in fs]
    
    # for i in tqdm(range(len(fs))):
    #     f = fs[i]
    #     a1s[i], a2s[i], t1s[i], t2s[i] = double_spring_oscillator(f, 'square', False, False)
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
    df.round(4).to_csv('../report/p1_1_data_square.csv', index=False)


def single_oscillator(gamma=0.5, save=None, show=True):
    t = 30
    dt = 1e-4
    steps = int(t / dt)

    len = 10
    s = String(l=-len, r=0, length=len, k=9)
    
    
    # 物体初始位置设为0，速度设为10
    m = Object(x0=0, v0=10, m=1, max_steps=steps)
    m.link(s, pos='r')
    # 没有外力，无需设force项，只需设定摩擦阻力
    m.add_friction(gamma)
    m.init(dt)
    for i in range(2, steps):
        m.update(dt)
    
    def find_period(x):
        peaks, _ = find_peaks(x, distance=10)
        return np.mean(np.diff(peaks)) * dt
    
    t = find_period(m.x)

    print(f'period: {t:.4f} s')
    print(f'frequency:{2 * np.pi / t:.4f} Hz')
    if show or save:
        plot([m.x], int(0.1 / dt), save=save, show=show)

def p2_1():
    single_oscillator(0.5, 'p2_1_gamma=0.5', False)

def p2_2():
    single_oscillator(6, 'p2_2_gamma=6', False)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Execute function based on arguments.')
    parser.add_argument('a1', type=str, default='1', nargs='?', help='Problem number')
    parser.add_argument('a2', type=str, default='1', nargs='?', help='Question number')
    
    args = parser.parse_args()
    func_name = f'p{args.a1}_{args.a2}'
    
    try:
        # Use globals() to get the current global symbol table, and then execute the corresponding function
        globals()[func_name]()
            
    except KeyError:
        print(f"Function {func_name} not found!")