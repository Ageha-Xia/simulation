import numpy as np
from tqdm import tqdm

def euler(steps, force, r, v, m, delta_t=1):
    rs = np.empty((steps, 2)) 
    vs = np.empty((steps, 2))
    
    for i in tqdm(range(steps)):
        rs[i] = r
        vs[i] = v
        a = force(r) / m
        r += v * delta_t
        v += a * delta_t
        
    return rs, vs