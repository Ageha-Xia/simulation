import numpy as np
from planet import *
from plot import plot

def earth_orbit(delta_t=100):
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 1]))
    rs, vs = planetsystem.simulate(365.243 * 86400, delta_t=delta_t, method='euler_cromer')
    return rs, vs

def jupiter_orbit(delta_t=100):
    planetsystem = Jupiter(r=np.array([1, 0]), v=np.array([0, 1]))
    rs, vs = planetsystem.simulate(4332.38 * 86400, delta_t=delta_t, method='euler_cromer')
    return rs, vs

def p1_1():
    delta_t = 100
    rs, vs = earth_orbit(delta_t)    
    plot(rs, downsample=50000 // delta_t, save='p1_1', title='Earth\'s orbit by Euler Cromer method')
    
def p1_2():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 5]))
    delta_t = 10000
    rs, vs = planetsystem.simulate(t=1e11, delta_t=delta_t, method='euler_cromer', force='delta')
    plot(rs, downsample=10000, save='p1_2', title='Earth\'s orbit under fine-tuning gravity')

def p1_3():
    planetsystem = Earth(r=np.array([1, 0]), v=np.array([0, 2.5855e-6]))
    delta_t = int(1e7)
    rs, vs = planetsystem.simulate(t=1e14, delta_t=delta_t, method='euler_cromer', force='cube')
    plot(rs, downsample=10000, save='p1_3', title='Earth\'s orbit under cubic gravity')

def p2_1():
    # Earth
    rs, vs = earth_orbit()
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Earth): {max_distance:.4e}, Min distance(Earth): {min_distance:.4e}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.4e}%")
    
    # Jupiter
    rs, vs = jupiter_orbit()
    distances = np.linalg.norm(rs, axis=1)
    max_distance = np.max(distances)
    min_distance = np.min(distances)
    print(f"Max distance(Jupiter): {max_distance:.4e}, Min distance(Jupiter): {min_distance:.4e}, L2_Error={((max_distance - min_distance)/ max_distance * 100):.4e}%")
    plot(rs, downsample=10000, save='p2_1', title='Jupiter\'s orbit by Euler Cromer method')

def p2_2():
    def L2_Error(areas):
        differences = areas - areas.mean()
        return areas.mean(), np.linalg.norm(differences, ord=2) / np.linalg.norm(areas)
    
    # Earth
    delta_t = 100
    rs, vs = earth_orbit(delta_t)
    areas = 0.5 * np.abs(rs[:-1, 0] * rs[1:, 1] - rs[1:, 0] * rs[:-1, 1])
    mean, L2 = L2_Error(areas)
    print(f"mean area per step(Earth): {mean:.4e}, L2_Error(Earth): {(L2 * 100):.4e}%")
    
    # Jupiter
    delta_t = 100
    rs, vs = jupiter_orbit(delta_t)
    areas = 0.5 * np.abs(rs[:-1, 0] * rs[1:, 1] - rs[1:, 0] * rs[:-1, 1])
    mean, L2 = L2_Error(areas)
    print(f"mean area per step(Jupiter): {mean:.4e}, L2_Error(Jupiter): {(L2 * 100):.4e}%")


def p2_3():
    def kepler_third_law(rs, delta_t):
        # 计算每一点与太阳之间的距离
        distances = np.linalg.norm(rs, axis=1)
        
        # 找到最远和最近的距离
        r_max = np.max(distances)
        r_min = np.min(distances)
        
        # 计算半长轴 a
        a = 0.5 * (r_max + r_min)
        
        # 周期 T 是总时间，即 delta_t 乘以数据点的数量
        T = delta_t * len(rs)
        
        # 计算 a^3/T^2
        value = (a**3) / (T**2)
        
        return value
    
    # Earth
    delta_t = 100
    rs, vs = earth_orbit(delta_t)
    v_earth = kepler_third_law(rs, delta_t)
    
    # Jupiter
    delta_t = 100
    rs, vs = jupiter_orbit(delta_t)
    v_jupiter = kepler_third_law(rs, delta_t)
    print(f"A^3/T^2(Earth):{v_earth:.4e}, A^3/T^2(Jupiter):{v_jupiter:.4e}, relative_error={(np.abs(v_earth - v_jupiter) / v_jupiter * 100):.4e}%")
    
if __name__ == '__main__':
    p1_3()