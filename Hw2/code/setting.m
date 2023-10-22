% Parameters
k1 = 600; % 弹性系数
k2 = 1000; % 弹性系数
m1 = 20; % 质量
m2 = 10; % 质量
l1 = 10; % 原始长度
l2 = 10; % 原始长度

% 驱动力的定义
% F = @(t) 5*sin(2.022 * 2 * pi * t);
F = @(t) 5 * square(2 * pi * 0.68614 * t);

% 初始条件
initial_conditions = [10; 0; 20; 0]; % 可根据需要修改

% 时间跨度
tspan = [0, 100];

% 使用ode45求解
[t, Y] = ode45(@(t, y) oscillator(t, y, k1, k2, m1, m2, l1, l2, F), tspan, initial_conditions);



% 为m1计算周期和振幅
[pks_m1, locs_m1] = findpeaks(Y(:, 1));
if length(locs_m1) > 1
    period_m1 = mean(diff(t(locs_m1)));
else
    period_m1 = NaN;
end
amplitude_m1 = (max(Y(:, 1)) - min(Y(:, 1))) / 2;

% 为m2计算周期和振幅
[pks_m2, locs_m2] = findpeaks(Y(:, 3));
if length(locs_m2) > 1
    period_m2 = mean(diff(t(locs_m2)));
else
    period_m2 = NaN;
end
amplitude_m2 = (max(Y(:, 3)) - min(Y(:, 3))) / 2;

% 显示结果
disp(['m1 - Period: ', num2str(period_m1), ' seconds']);
disp(['m1 - Amplitude: ', num2str(amplitude_m1), ' meters']);
disp(['m2 - Period: ', num2str(period_m2), ' seconds']);
disp(['m2 - Amplitude: ', num2str(amplitude_m2), ' meters']);

% 绘图
figure; % 新建图形窗口
plot(t, Y(:, 1), 'b'); % m1的位移随时间变化
hold on;
plot(t, Y(:, 3), 'r'); % m2的位移随时间变化
xlabel('Time (s)');
ylabel('Displacement (m)');
legend('m1', 'm2');
title('Displacement vs. Time');
grid on;
