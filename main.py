import numpy as np
from planet import *
from plot import plot

def p1_1():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 1]))
    delta_t = 100
    rs, vs = planetsystem.simulate(365.243 * 86400, delta_t=delta_t, method='euler_cromer')
    plot(rs, downsample=50000 / delta_t, save='p1_1', title='Earth\'s orbit by Euler Cromer method')
    
def p1_2():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 5]))
    delta_t = 10000
    rs, vs = planetsystem.simulate(t=1e11, delta_t=delta_t, method='euler_cromer', force='delta')
    plot(rs, downsample=10000, save='p1_2', title='Earth\'s orbit under fine-tuning gravity')

def p1_3():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 2.5855e-6]))
    delta_t = int(1e7)
    rs, vs = planetsystem.simulate(t=1e14, delta_t=delta_t, method='euler_cromer', force='cube')
    plot(rs, downsample=10000, save='p1_3', title='Earth\'s orbit under cubic gravity')

def p2_1():
    # Earth
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 1]))
    delta_t = 100
    rs, vs = planetsystem.simulate(365.243 * 86400, delta_t=delta_t, method='euler_cromer')
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Earth): {max_distance}, Min distance(Earth): {min_distance}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.2f}%")
    
    # Jupiter
    planetsystem = Jupiter(r=np.array([1, 0]), v=np.array([0, 1]))
    delta_t = 100
    rs, vs = planetsystem.simulate(4332.38 * 86400, delta_t=delta_t, method='euler_cromer')
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Jupiter): {max_distance}, Min distance(Jupiter): {min_distance}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.2f}%")
    plot(rs, downsample=10000, save='p2_1', title='Jupiter\'s orbit by Euler Cromer method')


if __name__ == '__main__':
    p2_1()