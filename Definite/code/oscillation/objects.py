import numpy as np
from .dampers import Damper
from .strings import String
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
        
        self.connectors = []   # 表示与物体相连的弹簧
        self.forces = []    # 表示物体受到的内力
        self.external_forces = []   # 表示物体受到的外力
        self.index = 1
    
    def link(self, connector, pos='r'):
        '''
        pos参数表示物体相对弹簧/阻尼器的位置,默认物体在弹簧/阻尼器右侧
        '''
        
        self.connectors.append((pos, connector))
        if pos == 'r':
            self.forces.append(connector.force)
        else:
            self.forces.append(lambda : -connector.force())
    
    def add_force(self, force):
        '''
        force表示物体受到的外力
        '''
        self.external_forces.append(force)
        
    def add_friction(self, k):
        '''
        k表示摩擦系数
        '''
        self.forces.append(lambda : -k * self.v[self.index - 1])
    
    def force(self):
        # 当考虑阻尼时，v1和v2必须给定
        
        force = 0
        for f in self.forces:
            force += f()
        
        for f in self.external_forces:
            force += f(self.t)
        
        return force
        
    def init(self, dt):
        self.v[1] = self.v[0] + self.force() / self.m * dt
        self.x[1] = self.x[0] + (self.v[0] + self.v[1]) / 2 * dt
        
        for s in self.connectors:
            if isinstance(s[1], String):
                if s[0] == 'r':
                    s[1].update(x_r=self.x[1])
                else:
                    s[1].update(x_l=self.x[1])
                
            elif isinstance(s[1], Damper):
                if s[0] == 'r':
                    s[1].update(v_r=self.v[1])
                else:
                    s[1].update(v_l=self.v[1])
                
        self.index = 2
        self.t += dt
    
    def get_energy(self):
        return 0.5 * self.m * self.v[self.index - 1] ** 2
    
    def update(self, dt):
        # Verlet法
        # self.x[self.index] = 2 * self.x[self.index - 1] - self.x[self.index - 2] + self.force() / self.m * dt * dt
        # self.v[self.index - 1] = (self.x[self.index] - self.x[self.index - 2]) / (2 * dt)
        
        def flash(x=None, v=None, dt=None, index=False):
            # 状态更新
            for s in self.connectors:
                
                # 更新相邻的弹簧
                if isinstance(s[1], String):
                    if s[0] == 'r':
                        s[1].update(x_r=self.x[self.index] if x is None else x)
                    else:
                        s[1].update(x_l=self.x[self.index] if x is None else x)
                        
                # 更新相邻的阻尼器        
                elif isinstance(s[1], Damper):
                    if s[0] == 'r':
                        s[1].update(v_r=self.v[self.index] if v is None else v)
                    else:
                        s[1].update(v_l=self.v[self.index] if v is None else v)
                        
            # 位置和速度更新
            if index:
                self.index += 1
            if dt:
                self.t = t0 + dt
            if v:
                self.v[self.index] = v

        # 4阶Runge-Kutta
        x0 = self.x[self.index - 1]
        v0 = self.v[self.index - 1]
        t0 = self.t
        k1x = dt * v0
        k1v = dt * self.force() / self.m
        k2x = dt * (v0 + 0.5 * k1v)
        flash(x=x0 + 0.5 * k1x, v=v0 + 0.5 * k1v)
        k2v = dt * self.force() / self.m
        k3x = dt * (v0 + 0.5 * k2v)
        flash(x=x0 + 0.5 * k2x, v=v0 + 0.5 * k2v)
        k3v = dt * self.force() / self.m
        k4x = dt * (v0 + k3v)
        flash(x=x0 + k3x, v=v0 + k3v)
        k4v = dt * self.force() / self.m
        
        self.x[self.index] = x0 + (k1x + 2 * k2x + 2 * k3x + k4x) / 6
        self.v[self.index] = v0 + (k1v + 2 * k2v + 2 * k3v + k4v) / 6
        
        flash(dt=dt, index=True)