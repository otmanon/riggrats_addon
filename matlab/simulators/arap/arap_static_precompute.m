function spre = arap_cd_static_precompute(sim_params)
%ARAP_STATIC_PRE Summary of this function goes here
%   Detailed explanation goes here
spre = {};

M = kron(speye(2), massmatrix(sim_params.X, sim_params.F, 'barycentric'));
K = tetrahedron_gradient(sim_params.X, sim_params.F);



tri_area = triangle_area(sim_params.X, sim_params.F);
Mt = kron(speye(2), kron(diag(tri_area), speye(2)));
mu = kron(speye(2), kron(diag(sim_params.mu), speye(2)));
L = K'*Mt*mu*K;
spre.A = 0.5 * (sim_params.invh2 * sim_params.do_inertia * M +   L);

spre.M = M;
spre.L = L;
spre.MK = Mt * mu * K;

spre.MKx = spre.MK*sim_params.X(:);

spre.Mx = M*sim_params.X(:);

spre.Lx = L*sim_params.X(:);



%spre.H = [0.5*spre.A sim.Aeq' ; sim.Aeq sparse(size(sim.Aeq, 1), size(sim.Aeq, 1))];
[uc_null, spre.factorization] = min_quad_with_fixed(spre.A , zeros(size(spre.A, 1), 1), [], [], sim_params.Aeq, zeros(size(sim_params.Aeq, 1), 1));

end

