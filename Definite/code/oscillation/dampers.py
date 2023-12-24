from .connector import Connector

class Damper(Connector):
    def __init__(self, v_l, v_r, damping=0):
        self.v_l = v_l
        self.v_r = v_r
        self.damping = damping
    
    def force(self):
        return - self.damping * (self.v_r - self.v_l) 
    
    def update(self, v_l=None, v_r=None):
        if v_l:
            self.v_l = v_l
        if v_r:
            self.v_r = v_r
            
    def get_energy(self):
        return 0
    