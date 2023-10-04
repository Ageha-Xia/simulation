import numpy as np
from planet import PlanetSystem
from plot import plot

def p1_1():
    planetsystem = PlanetSystem(r=np.array([1, 0]), v=np.array([0, 1]))
    delta_t = 100
    rs = planetsystem.simulate(365.243 * 86400, delta_t=delta_t, method='euler_cromer')
    plot(rs, downsample=50000 / delta_t)
    
def p1_2():
    planetsystem = PlanetSystem(r=np.array([1, 0]), v=np.array([0, 5]))
    delta_t = 10000
    rs = planetsystem.simulate(t=1e11, delta_t=delta_t, method='euler_cromer', force='delta')
    plot(rs, downsample=10000)

def p1_3():
    planetsystem = PlanetSystem(r=np.array([1, 0]), v=np.array([0, 2.586e-6]))
    delta_t = int(1e7)
    rs = planetsystem.simulate(t=1e14, delta_t=delta_t, method='euler_cromer', force='cube')
    plot(rs, downsample=10000, save='cube')

if __name__ == '__main__':
    p1_3()