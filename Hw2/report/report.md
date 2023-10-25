### 计算机模拟物理作业
##### 2023年10月18日
##### 夏泽宇 2021012242

##### 1.1
$设左侧弹簧长度为l_1,M初始位置为x_1。中间弹簧长度为l_2，m初始位置为x_2。可列出运动方程:$
$$
\begin{align}
    m_1\frac{d^2x_1}{dt^2}&=-k_1(x_1-l_1)+k_2(x_2-x_1-l_2)
    \\m_2\frac{d^2x_2}{dt^2}&=-Asin(\omega t)-k_2(x_2-x_1-l_2)
\end{align}
$$
$令X=\begin{bmatrix}
x_1 \\
x_2 \\
\end{bmatrix}，M=\begin{bmatrix}
m_{1} & 0  \\
0 & m_{2}\\
\end{bmatrix}，K=\begin{bmatrix}
-k_{1} - k_{2}& k_2  \\
k_2 & -k_2\\
\end{bmatrix}，
则有MX''=KX+b$
$共振频率仅有系统本身决定，因此可不考虑由外力带来的影响，即上式中的b项，仅考虑线性方程组MX''=KX$
$线性方程组可变形为X''=M^{-1}KX$
$注意到M^{-1}K可逆，因此可对角化为P^{-1}DP，其中D=diag\{\lambda_1,\lambda_2, \cdots \}$
$因此由PX''=DPX$
$令Z=PX，有Z''=DZ，即z_i''=\lambda_iz_i, i=1,2，可得z_i=Ae^{\sqrt{\lambda_i}x}+Be^{-\sqrt{\lambda_i}x}$
$代入数值得M=\begin{bmatrix}
20 & 0  \\
0 & 10\\
\end{bmatrix}，K=\begin{bmatrix}
-1600 & 1000  \\
1000 & -1000\\
\end{bmatrix}，M^{-1}K=\begin{bmatrix}
-80 & 50  \\
100 & -100\\
\end{bmatrix}$
$M^{-1}K的特征值\lambda_1=-18.5857, \lambda_2=-161.4143$
$$
\begin{aligned}
    z_1&=Ae^{\sqrt{18.5857}ix}+Be^{-\sqrt{18.5857}ix}=Asin(4.311x)+Bcos(4.311x)
    \\z_2&=Ae^{\sqrt{161.4143}ix}+Be^{-\sqrt{161.4143}ix}=Asin(12.705x)+Bcos(12.705x)
\end{aligned}
$$
$因此固有频率\omega_1=4.311，\omega_2=12.705。当驱动力为这2个频率时会发生共振$
\
$\omega=4.311 rad/s时，物体运动随时间变化的x-t图像如下$
![image](../fig/resonance,%20f=0.68614Hz,%20sin_wave.gif)
$\omega=12.705 rad/s时，物体运动随时间变化的x-t图像如下$
![image](../fig/resonance,%20f=2.022Hz,%20sin_wave.gif)

$通过分析共振频率附近频谱的振幅，可得到如下图像$