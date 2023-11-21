% Parameters
k1 = 600; % 弹性系数
k2 = 1000; % 弹性系数
m1 = 20; % 质量
m2 = 10; % 质量

% 构造系统矩阵
M = [m1 0; 0 m2];
K = [k1 + k2, -k2; -k2, k2];

% 计算特征值
inv(M)*K
[A, B] = eig(inv(M)*K);

% 自然频率 (特征值的平方根)
frequencies = sqrt(diag(B)) / (2*pi);

% 输出自然频率
disp(['Natural Frequency 1: ', num2str(frequencies(1)), ' Hz']);
disp(['Natural Frequency 2: ', num2str(frequencies(2)), ' Hz']);
