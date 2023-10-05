import numpy as np
from method import *

class Planet():
    def __init__(self):
        self.M = 1.988e30   # solar mass
        self.G = 6.67408e-11    # gravitational constant
        self.methods = {
            'euler':euler, 
            'euler_cromer': euler_cromer,
            'euler_richardson':euler_richardson
        }
    
    def force(self, r):
        # r is supposed to a numpy array with shape (2,)
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 3) * r
    
    def force_delta(self, r):
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 3.05) * r
    
    def force_cube(self, r):
        return -self.G * self.M * self.m / (np.linalg.norm(r, ord=2) ** 4) / self.r0 * r
    
    def simulate(self, t, delta_t=1, method='euler', force='default'):
        force_list = {
            'default': self.force,
            'delta': self.force_delta,
            'cube': self.force_cube
        }
        
        normalized_r, normalized_v =  self.methods[method](int(t / delta_t), force_list[force], self.r, self.v, self.m, self.r0, self.v0, delta_t)
        return normalized_r * self.r0, normalized_v * self.v0

class Earth(Planet):
    def __init__(self, r, v):
        super().__init__()
        
        self.m = 5.965e24   # earth mass
        self.r0 = 1.496e11
        self.v0 = 2.978e4
        
        self.r = self.r0 * r    # r expects a numpy.array with shape (2,)
        self.v = self.v0 * v
        
class Jupiter(Planet):
    def __init__(self, r, v):
        super().__init__()
        
        self.m = 1.8986e27   # jupiter mass
        self.r0 = 7.78e11
        self.v0 = 1.306e4
        
        self.r = self.r0 * r    # r expects a numpy.array with shape (2,)
        self.v = self.v0 * v
    