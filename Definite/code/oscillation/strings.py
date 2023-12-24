from .connector import Connector

class String(Connector):
    def __init__(self, x_l, x_r, length, k):
        self.x_l = x_l
        self.x_r = x_r
        self.length = length
        self.k = k
    
    def force(self):
        return -self.k * (self.x_r - self.x_l - self.length)
    
    def update(self, x_l=None, x_r=None):
        if x_l:
            self.x_l = x_l
        if x_r:
            self.x_r = x_r
            
    def get_energy(self):
        return 0.5 * self.k * (self.x_r - self.x_l - self.length) ** 2