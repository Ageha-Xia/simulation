import numpy as np
from numba import jit

# @jit(forceobj=True)
# def display(i, steps):
#     if i % (steps // 100) == 0:
#         percentage = (i / steps) * 100
#         print('\r%.2f%%' % percentage, end='')

@jit(nopython=True)
def euler(steps, force, r, v, m, r0, v0, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    r = r / r0
    v = v / v0
    
    for i in range(steps):
        rs[i] = r 
        vs[i] = v
        a = force(m, r, r0) / m 
        r += v * delta_t * v0 / r0
        v += a * delta_t / (v0 * (r0 ** 2))
        
    return rs, vs

@jit(nopython=True)
def euler_cromer(steps, force, r, v, m, r0, v0, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    r = r / r0
    v = v / v0
    
    for i in range(steps):
        rs[i] = r
        vs[i] = v
        a = force(m, r, r0) / m
        v += a * delta_t / (v0 * (r0 ** 2))
        r += v * delta_t * v0 / r0
    
    return rs, vs

@jit(nopython=True)
def euler_richardson(steps, force, r, v, m, r0, v0, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    r = r / r0
    v = v / v0
    
    for i in range(steps):
        rs[i] = r
        vs[i] = v
        a = force(m, r, r0) / m
        r_ = r + 0.5 * v * delta_t * v0 / r0
        v_ = v + 0.5 * a * delta_t / (v0 * (r0 ** 2))
        
        a_ = force(m, r_, r0) / m
        v += a_ * delta_t / (v0 * (r0 ** 2))
        r += v_ * delta_t * v0 / r0
    
    return rs, vs