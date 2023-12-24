import numpy as np
import pandas as pd
import argparse
import oscillation
from plot import *
from scipy.signal import find_peaks

def double_spring_oscillator(save=False, show=True):
    x1 = 0.1
    v1 = 0.1
    x2 = -0.1
    v2 = -0.1
    
    M1 = 500
    M2 = 20
    K1 = 20000
    K2 = 200000
    C = 1000
    
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
    system.run(dt, steps)
    
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

    plot_static([m1.x - len1 - len2, m2.x - len2], t, show=show)
    return (a1, a2, t1, t2)

# def wrapper(args):
#     return double_spring_oscillator(*args)

# def p1_1():
#     f1 = np.arange(0.4, 0.8 + 0.05, 0.01)
#     f2 = np.arange(1.8, 2.2 + 0.05, 0.01)
#     fs = np.concatenate((f1, f2))
#     a1s = np.zeros_like(fs)
#     a2s = np.zeros_like(fs)
#     t1s = np.zeros_like(fs)
#     t2s = np.zeros_like(fs)
    
#     # for i in tqdm(range(len(fs))):
#     #     f = fs[i]
#     #     a1s[i], a2s[i], t1s[i], t2s[i] = double_spring_oscillator(f, 'sin', False, False)
#     args = [(f, 'sin', False, False) for f in fs]
    
#     with ProcessPoolExecutor() as executor:
#         results = list(tqdm(executor.map(wrapper, args), total=len(fs)))

#     a1s, a2s, t1s, t2s = zip(*results)
    
#     df = pd.DataFrame({
#         'f': fs,
#         'a1': a1s,
#         'a2': a2s,
#         't1': t1s,
#         't2': t2s
#     })
#     df.round(4).to_csv('../report/p1_1_data_sin.csv', index=False)

# def p1_2():
#     f1 = np.arange(0.4, 0.8 + 0.05, 0.01)
#     f2 = np.arange(1.8, 2.2 + 0.05, 0.01)
#     fs = np.concatenate((f1, f2))
#     a1s = np.zeros_like(fs)
#     a2s = np.zeros_like(fs)
#     t1s = np.zeros_like(fs)
#     t2s = np.zeros_like(fs)
    
#     args = [(f, 'square', False, False) for f in fs]
    
#     # for i in tqdm(range(len(fs))):
#     #     f = fs[i]
#     #     a1s[i], a2s[i], t1s[i], t2s[i] = double_spring_oscillator(f, 'square', False, False)
#     with ProcessPoolExecutor() as executor:
#         results = list(tqdm(executor.map(wrapper, args), total=len(fs)))

#     a1s, a2s, t1s, t2s = zip(*results)
    
#     df = pd.DataFrame({
#         'f': fs,
#         'a1': a1s,
#         'a2': a2s,
#         't1': t1s,
#         't2': t2s
#     })
#     df.round(4).to_csv('../report/p1_1_data_square.csv', index=False)
    
if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Execute function based on arguments.')
    # parser.add_argument('a1', type=str, default='1', nargs='?', help='Problem number')
    # parser.add_argument('a2', type=str, default='1', nargs='?', help='Question number')
    
    # args = parser.parse_args()
    # func_name = f'p{args.a1}_{args.a2}'
    
    # try:
    #     # Use globals() to get the current global symbol table, and then execute the corresponding function
    #     globals()[func_name]()
            
    # except KeyError:
    #     print(f"Function {func_name} not found!")
    
    double_spring_oscillator()