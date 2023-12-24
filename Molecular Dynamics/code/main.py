from system import *
from plot import *
import matplotlib.pyplot as plt

l_u = 3.4e-10
e_u = 1.65e-21
m_u = 6.69e-26
t_u = 2.17e-12
v_u = 1.57e2
f_u = 4.85e-12
p_u = 1.43e-2
t_u = 1.2e2
kb = 1.38e-23

def p1_1():
    sys1 = PotentialSystem(10, 64, 1)
    sys1.run(0.01, 100)
    print(f'temperature:{sys1.eval_temperature()}')
    
def p1_2():
    v = []
    for i in range(10):
        sys1 = PotentialSystem(10, 64, 3.6)
        sys1.run(0.01, 100)
        print(sys1.eval_temperature())
        print(sys1.average_speed())
        v.append(sys1.velocities)
    v = np.vstack(v)
    velocity_distribution(v, bins=50, save=True, filename='../fig/p1_2.png')
    

def p1_3():
    sys2 = HardSphereSystem(10, 64, 1)
    sys2.run(0.01, 1000)
    print(f'freepath:{sys2.eval_freepath()}')
        

def p2_1_1():
    sys1 = PotentialSystem(6, 16, 2.7)
    print(f'speed:{sys1.average_speed() * v_u}')
    print(f'temperature_before:{sys1.eval_temperature()}')
    sys1.run(0.01, 1000)
    print(f'temperature_after:{sys1.eval_temperature()}')
    
def p2_1_2():
    sys1 = PotentialSystem(6, 16, 3.6)
    print(f'speed:{sys1.average_speed() * v_u}')
    print(f'temperature_before:{sys1.eval_temperature()}')
    sys1.run(0.01, 1000)
    print(f'temperature_after:{sys1.eval_temperature()}')
    
def p2_2_1():
    v = []
    for i in range(50):
        sys1 = PotentialSystem(6, 16, 2.7)
        sys1.run(0.01, 100)
        # print(f'temperature:{sys1.eval_temperature()}')
        v.append(sys1.velocities)
    v = np.vstack(v)
    
    velocity_distribution(v, bins=50, save=True, filename='../fig/p2_2_1.png')
    
def p2_2_2():
    v = []
    for i in range(50):
        sys1 = PotentialSystem(6, 16, 3.6)
        sys1.run(0.01, 100)
        # print(f'temperature:{sys1.eval_temperature()}')
        v.append(sys1.velocities)
    v = np.vstack(v)
    
    velocity_distribution(v, bins=50, save=True, filename='../fig/p2_2_2.png')

if __name__ == '__main__':
    # p1_1()
    # p1_2()
    # p1_3()
    # p2_1_1()
    # p2_1_2()
    # p2_2_1()
    p2_2_2()