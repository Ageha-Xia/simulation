import numpy as np
from planet_motion import PlanetSystem
from plot import plot

def main():
    planetsystem = PlanetSystem(r=np.array([1, 0]), v=np.array([0, 1]))
    delta_t = 100
    rs = planetsystem.simulate(365 * 86400, delta_t=delta_t, method='euler')
    plot(rs, delta_t)
    
if __name__ == '__main__':
    main()