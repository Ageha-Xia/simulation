from planet_motion import PlanetSystem
from plot import plot

def main():
    planetsystem = PlanetSystem()
    delta_t = 1
    rs, _ = planetsystem.simulate(365 * 86400, delta_t=delta_t)
    plot(rs, delta_t)
    
if __name__ == '__main__':
    main()