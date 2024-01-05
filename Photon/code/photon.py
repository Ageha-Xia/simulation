import numpy as np
import warnings
from data import compton_and_photoelectric

class Photon:
    def __init__(self, r0, E0, Omega0, H=4, R=2):
        '''
        r: position
        E0: Energy
        Omega0: Direction
        '''
        
        # Initialize the photon
        self.r = [r0]
        self.E = [E0]
        self.Omega = [Omega0]
        
        # Initialize the cross-section functions
        self.compton, self.photoelectric = compton_and_photoelectric()
        self.H = H
        self.R = R
        self.within = True
        
    def transport(self):
        '''
        Transport the photon
        '''
        if not self.within:
            warnings.warn('The photon isn\'t in the detector.')
            return 
        
        eps = np.random.uniform(0, 1)
        rho = -np.log(eps)  
        L = rho / self.compton(self.E[-1])  
        r = self.r[-1] + L * self.Omega[-1]
        
        if r[2] <= 0 or r[2] >= self.H or np.linalg.norm(r[:2]) >= self.R:
            self.r.append(r)
            self.E.append(self.E[-1])   # energy retains for the photon has gone out of the detector
            self.Omega.append(self.Omega[-1])
            self.within = False
            return 
        
        S_pe = self.photoelectric(self.E[-1])
        S_c = self.compton(self.E[-1])
        p_pe = S_pe / (S_pe + S_c)
        eps = np.random.uniform(0, 1)
        if eps < p_pe:
            # Photoelectric effect
            self.r.append(r)
            self.E.append(0)
            self.Omega.append(self.Omega[-1])   # Absorption, the direction does not change
        
        else:
            # compton dispersion
            E0 = 0.511  # MeV, electron rest mass
            alpha = self.E[-1] / E0
            while(True):
                eps1 = np.random.uniform(0, 1)
                eps2 = np.random.uniform(0, 1)
                eps3 = np.random.uniform(0, 1)
                
                if eps1 <= 27 / (4 * alpha + 29):
                    x1 = (1 + 2 * alpha) / (1 + 2 * alpha * eps2)
                    
                    if eps3 <= 0.5 * (((alpha + 1 - x1) / alpha) ** 2 + 1):
                        x = x1
                        break
                else:
                    x2 = 1 + 2 * alpha * eps2
                    
                    if eps3 <= 27 / 4 * (x2 - 1) ** 2 / x2 ** 3:
                        x = x2
                        break
            E = self.E[-1] / x
            alpha_new = alpha / x
            mu_L = 1 - 1 / alpha_new + 1 / alpha
            
            a = mu_L
            b = np.sqrt(1 - a ** 2)
            phi = np.random.uniform(0, 2 * np.pi)
            c = np.cos(phi)
            d = np.sin(phi)
            
            u_m0 = self.Omega[-1][0]
            v_m0 = self.Omega[-1][1]
            w_m0 = self.Omega[-1][2]
            
            if u_m0**2 + v_m0**2 > 1e-4:
                u_m = (-b * c * w_m0 * u_m0 + b * d * v_m0) / np.sqrt(u_m0**2 + v_m0**2) + a * u_m0
                v_m = (-b * c * w_m0 * v_m0 - b * d * u_m0) / np.sqrt(u_m0**2 + v_m0**2) + a * v_m0
                w_m = b * c * np.sqrt(u_m0**2 + v_m0**2) + a * w_m0
            
            else:
                u_m = b * c
                v_m = b * d
                w_m = a * w_m0
            
            # Update the photon
            self.r.append(r)
            self.E.append(E)
            self.Omega.append(np.array([u_m, v_m, w_m]))
            
    def simulate(self):
        while(self.within and self.E[-1] > 0):
            self.transport()
        
        # E_D records the energy deposited in the detector
        E_D = self.E[0] - self.E[-1]
        return E_D