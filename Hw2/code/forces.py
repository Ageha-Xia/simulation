import numpy as np

class Force:
    def __init__(self) -> None:
        pass
    
class Force_Sin(Force):
    def __init__(self, A, f, phi):
        self.A = A
        self.f = f * 2 * np.pi
        self.phi = phi
        
    def __call__(self, t):
        return -self.A * np.sin(self.f * t + self.phi)
    
class Force_Square(Force):
    def __init__(self, f, A):
        self.T = 1 / f  # 周期
        self.A = A  # 振幅

    def __call__(self, t):
        # 判断 t 在一个周期内的位置
        if (t % self.T) < (self.T / 2.0):
            return -self.A
        else:
            return self.A