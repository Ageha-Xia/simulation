import numpy as np
from ase import Atoms
from ase.calculators.lj import LennardJones
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md import VelocityVerlet
from ase.units import kJ, mol, nm
from scipy.optimize import curve_fit

# 定义计算压强的函数
def virial_pressure(atoms):
    volume = atoms.get_volume()
    positions = atoms.get_positions(wrap=True)
    forces = atoms.get_forces()
    virial = 0.0
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            rij = positions[i] - positions[j]
            distance = np.linalg.norm(rij)
            Fij = forces[i] - forces[j]
            virial += np.dot(Fij, rij)
    pressure = (1/3) * virial / volume
    return pressure

# 模拟不同体积下的压强
V_data = []  # 体积数据
P_data = []  # 压强数据
for cell_size in np.linspace(2 * nm, 5 * nm, 5):  # 调整体积范围和步长
    atoms = Atoms('Ar2', positions=[(0, 0, 0), (0.5 * nm, 0.5 * nm, 0.5 * nm)])
    atoms.set_cell([cell_size, cell_size, cell_size])
    atoms.set_pbc(True)  # 设置周期性边界条件

    epsilon = 0.0103 * kJ / mol
    sigma = 0.340 * nm
    calc = LennardJones(epsilon=epsilon, sigma=sigma)
    atoms.set_calculator(calc)

    MaxwellBoltzmannDistribution(atoms, temperature_K=300)
    dyn = VelocityVerlet(atoms, 1 * 1e-14)

    # 运行模拟
    for step in range(100):
        dyn.run(1)

    # 计算平均压强
    pressure = virial_pressure(atoms)
    V_data.append(atoms.get_volume())
    P_data.append(pressure)

# 定义范德华方程
def van_der_Waals(V, a, b):
    n = 1  # mol
    R = 0.0821  # L·atm/(mol·K)
    T = 300  # K
    return (n * R * T) / (V - n * b) - a * n**2 / V**2

# 拟合范德华参数
popt, pcov = curve_fit(van_der_Waals, V_data, P_data)
a, b = popt
print("范德华方程参数 a =", a)
print("范德华方程参数 b =", b)
