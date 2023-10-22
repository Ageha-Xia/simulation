import numpy as np
# from numba.experimental import jitclass

# @jitclass()
class Object:
    def __init__(self, x0, v0, m, max_steps):
        self.x = np.zeros(max_steps)
        self.v = np.zeros(max_steps)
        self.x[0] = x0
        self.v[0] = v0
        self.m = m
        self.t = 0
        
        self.strings = []   # 表示与物体相连的弹簧
        self.forces = []    # 表示物体受到的内力
        self.external_forces = []   # 表示物体受到的外力
    
    def link(self, string, pos='r'):
        '''
        pos参数表示物体相对弹簧的位置,默认物体在弹簧右侧
        '''
        
        self.strings.append((pos, string))
        if pos == 'r':
            self.forces.append(string.force)
        else:
            self.forces.append(lambda: -string.force())
    
    def add_force(self, force):
        self.external_forces.append(force)
    
    def force(self):
        force = 0
        for f in self.forces:
            force += f()
        
        for f in self.external_forces:
            force += f(self.t)
        
        return force
        
    def init(self, dt):
        self.v[1] = self.v[0] + self.force() / self.m * dt
        self.x[1] = self.x[0] + (self.v[0] + self.v[1]) / 2 * dt
        
        for s in self.strings:
            if s[0] == 'r':
                s[1].update(r=self.x[1])
            else:
                s[1].update(l=self.x[1])
                
        self.index = 2
        self.t += dt
        
    def update(self, dt):
        self.x[self.index] = 2 * self.x[self.index - 1] - self.x[self.index - 2] + self.force() / self.m * dt * dt
        self.v[self.index - 1] = (self.x[self.index] - self.x[self.index - 2]) / (2 * dt)
        
        # 状态更新
        for s in self.strings:
            if s[0] == 'r':
                s[1].update(r=self.x[self.index])
            else:
                s[1].update(l=self.x[self.index])
        self.index += 1
        self.t += dt