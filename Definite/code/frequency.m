% 参数值 (需要具体数值)
m1 = 500;
m2 = 50;
c = 200;
k1 = 20000;
k2 = 200000;

% 矩阵定义
A = [m1, 0; 0, m2];
B = [c, -c; -c, c];
C = [k1, -k1; -k1, k1+k2];

% 计算 A^-1 * B 和 A^-1 * C
A_invB = inv(A)*B;
A_invC = inv(A)*C;

% 构造一个增广矩阵
augmented_matrix = [zeros(2), eye(2); -A_invC, -A_invB];

% 计算特征值
eigenvalues = eig(augmented_matrix);

% 提取频率
frequencies = abs(imag(eigenvalues)) / (2*pi);

% 显示频率
disp('The frequencies of the system are:');
disp(frequencies);