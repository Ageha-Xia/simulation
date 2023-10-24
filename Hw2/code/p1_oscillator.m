function dy = p1_oscillator(t, y, k1, k2, m1, m2, l1, l2, F)
    x1 = y(1);
    v1 = y(2);
    x2 = y(3);
    v2 = y(4);
    
    dx1 = v1;
    dv1 = (-k1*(x1-l1) + k2*(x2-x1-l2))/m1;
    dx2 = v2;
    dv2 = (-k2*(x2-x1-l2) - F(t))/m2;
    
    dy = [dx1; dv1; dx2; dv2];
end