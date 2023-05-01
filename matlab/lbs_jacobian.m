function J = lbs_jacobian(V, W)
    d = size(V, 2);
    n = size(V, 1);
    b = size(W, 2);
    
    one_w = ones(1, b);
    one_d = ones(1, d+1);
    one_n = ones(n, 1);
    U = [V one_n];
    
    A = kron(one_w, U);
    B = kron(W, one_d);
    J = repdiag( A .* B, 3);
    
end