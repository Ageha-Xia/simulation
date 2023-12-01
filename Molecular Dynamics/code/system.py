import numpy as np


class System:
    def __init__(self, L, n, temperature):
        self.L = L  # 区域边长
        self.n = n  # 粒子数量
        
        grid_size = int(np.sqrt(n))
        if grid_size ** 2 != n:
            raise ValueError("粒子数量必须是完全平方数以实现均匀分布")
        x, y = np.linspace(0, L, grid_size, endpoint=False), np.linspace(0, L, grid_size, endpoint=False)
        self.positions = np.array(np.meshgrid(x, y)).T.reshape(-1, 2)
        
        self.temperature = temperature
        self.epsilon = 1.0  # Lennard-Jones参数
        self.sigma = 1.0    # Lennard-Jones参数

        # 初始速度分布
        self.velocities = np.random.normal(0, 1, (n, 2))
        
        # 确保总动量为零
        self.velocities -= np.mean(self.velocities, axis=0)
        
        # 调整速度以匹配预期的总动能
        kinetic_energy = 0.5 * np.sum(self.velocities ** 2)
        desired_kinetic_energy = 1.5 * n * self.temperature 
        velocity_scale = np.sqrt(desired_kinetic_energy / kinetic_energy)
        self.velocities *= velocity_scale
        
    def lj_force(self, r):
        r6 = (self.sigma / r)**6
        r12 = r6 * r6
        force = 24 * self.epsilon * (2 * r12 - r6) / r
        return force
    
    def soft_core_potential(self, r):
        # 软球势
        epsilon = self.epsilon
        sigma = self.sigma
        r6 = (sigma / r)**6
        return epsilon * (r6 / (1 + r6))  
    
    def eval_temperature(self):
        # 计算当前动能
        current_kinetic_energy = 0.5 * np.sum(self.velocities ** 2)
        # 反推温度
        current_temperature = current_kinetic_energy / (1.5 * self.n)
        return current_temperature
    
    def eval_freepath(self):
        # 计算所有粒子的平均移动距离
        total_distance = 0
        for i in range(self.n):
            # 计算自上次碰撞以来粒子i移动的距离
            distance = np.linalg.norm(self.velocities[i]) * self.time_since_last_collision[i]
            total_distance += distance

        # 计算平均自由程
        avg_freepath = total_distance / self.n
        return avg_freepath
        
    def velocity_distribution(self, bins=10):
        # 计算所有粒子速度的大小
        speeds = np.linalg.norm(self.velocities, axis=1)

        # 计算直方图
        distribution, bin_edges = np.histogram(speeds, bins=bins, density=True)

        # 返回bin中心和对应的分布密度
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        return bin_centers, distribution
    
    def average_speed(self):
        # 计算所有粒子速度的大小（绝对值）
        speeds = np.linalg.norm(self.velocities, axis=1) ** 2

        # 计算速度大小的平均值
        avg_speed = np.sqrt(np.mean(speeds))
        return avg_speed
    
class PotentialSystem(System):
    def __init__(self, L, n, temperature):
        super().__init__(L, n, temperature)
        
    def run(self, dt, num_steps):
        # 初始加速度
        accelerations = self.calculate_accelerations()

        for step in range(num_steps):
            # Velocity Verlet算法
            self.positions += self.velocities * dt + 0.5 * accelerations * dt**2
            new_accelerations = self.calculate_accelerations()
            self.velocities += 0.5 * (accelerations + new_accelerations) * dt
            accelerations = new_accelerations

            # 应用周期性边界条件
            self.positions %= self.L
    
    def calculate_accelerations(self):
        # 初始化加速度为零
        accelerations = np.zeros((self.n, 2))

        # 设置截断距离和最大力限制
        cutoff_distance = 2.5 * self.sigma

        # 计算加速度
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r_vec = self.positions[j] - self.positions[i]
                r_vec -= np.round(r_vec / self.L) * self.L
                r = np.linalg.norm(r_vec)

                if r < cutoff_distance:
                    # 使用软球势
                    potential_derivative = self.soft_core_potential(r)
                    force_vec = -potential_derivative * r_vec / r
                    accelerations[i] += force_vec
                    accelerations[j] -= force_vec
                else:
                    # 使用Lennard-Jones势
                    force_magnitude = self.lj_force(r)
                    force_vec = force_magnitude * r_vec / r
                    accelerations[i] += force_vec
                    accelerations[j] -= force_vec

        return accelerations

class HardSphereSystem(System):
    def __init__(self, L, n, temperature):
        super().__init__(L, n, temperature)
        self.time_since_last_collision = np.zeros(self.n)

    def run(self, dt, num_steps):
        for step in range(num_steps):
            # 更新位置
            self.positions += self.velocities * dt

            # 更新自上次碰撞以来的时间
            self.time_since_last_collision += dt
            
            # 检测碰撞并更新速度
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    r_vec = self.positions[j] - self.positions[i]
                    
                    # 这里不应使用周期性边界条件
                    # r_vec -= np.round(r_vec / self.L) * self.L  # 周期性边界条件
                    r = np.linalg.norm(r_vec)

                    if r < self.sigma:
                        # 碰撞发生，重置碰撞时间
                        self.time_since_last_collision[i] = 0
                        self.time_since_last_collision[j] = 0
                        
                        # 计算径向单位向量
                        r_hat = r_vec / r

                        # 计算径向速度分量
                        v1_radial = np.dot(self.velocities[i], r_hat)
                        v2_radial = np.dot(self.velocities[j], r_hat)

                        # 交换径向速度分量
                        self.velocities[i] += (v2_radial - v1_radial) * r_hat
                        self.velocities[j] += (v1_radial - v2_radial) * r_hat
                        
                        overlap = self.sigma - r
                        displacement = (overlap / 2) * (r_vec / r)
                        self.positions[i] -= displacement
                        self.positions[j] += displacement

            # 应用周期性边界条件
            self.positions %= self.L

