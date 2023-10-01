import numpy as np
from method import *

class PlanetSystem():
    def __init__(self, M=1.989e30, m=5.965e24, initial_r=np.array([1.496e11,0]), initial_v=np.array([0, 3e4])):
        # M: solar mass
        # m: earth mass
        self.G = 6.6743 * 1e-11    # gravitational constant
        self.r = initial_r
        self.v = initial_v
        self.m = m
        self.M = M
        self.methods = {'euler':euler}
    
    def force(self, r):
        # r is supposed to a numpy array with shape (3,)
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 3) * r
    
    def simulate(self, t, delta_t=1, method='euler'):
        return self.methods[method](int(t / delta_t), self.force, self.r, self.v, self.m, delta_t)
        