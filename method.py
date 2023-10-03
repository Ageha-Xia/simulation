import numpy as np
from tqdm import tqdm

def euler(steps, force, r, v, m, r0, v0, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    r = r / r0
    v = v / v0
    
    for i in tqdm(range(steps)):
        rs[i] = r 
        vs[i] = v
        a = force(r) / m 
        r += v * delta_t * v0 / r0
        v += a * delta_t / (v0 * (r0 ** 2))
        
    return rs, vs

def euler_cromer(steps, force, r, v, m, r0, v0, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    r = r / r0
    v = v / v0
    
    for i in tqdm(range(steps)):
        rs[i] = r
        vs[i] = v
        a = force(r) / m
        v += a * delta_t / (v0 * (r0 ** 2))
        r += v * delta_t * v0 / r0
        
    return rs, vs