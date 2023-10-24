function dxdt = p2_1_oscillator(t, y, gamma)
    omega0 = 3;
    
    dxdt = zeros(2,1);
    
    dxdt(1) = y(2);                                 % dx/dt = v
    dxdt(2) = -omega0^2 * y(1) - gamma * y(2);     % dv/dt = -omega0^2 x - gamma v
end
