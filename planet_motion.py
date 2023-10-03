import numpy as np
from method import *

class PlanetSystem():
    def __init__(self, r, v, M=1.988e30, m=5.965e24):
        # M: solar mass
        # m: earth mass
        self.G = 6.6743 * 1e-11    # gravitational constant
        self.r0 = 1.496e11
        self.v0 = 2.978e4
        self.r = self.r0 * r    # r expects a numpy.array with shape (2,)
        self.v = self.v0 * v
        self.m = m
        self.M = M
        self.methods = {
            'euler':euler, 
            'euler_cromer': euler_cromer
        }
    
    def force(self, r):
        # r is supposed to a numpy array with shape (2,)
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 3) * r
    
    def neoforce(self, r):
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 3.05) * r
    
    def simulate(self, t, delta_t=1, method='euler'):
        normalized_r, normalized_v =  self.methods[method](int(t / delta_t), self.force, self.r, self.v, self.m, self.r0, self.v0, delta_t)
        return normalized_r * self.r0
        