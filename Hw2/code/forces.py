import numpy as np

class Force:
    def __init__(self, A, f, phi):
        self.A = A
        self.f = f
        self.phi = phi
        
    def __call__(self, t):
        return -self.A * np.sin(self.f * t + self.phi)