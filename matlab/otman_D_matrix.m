function phi = otman_D_matrix(V, F, dt)
%OTMAN_D_MATRIX momentum leaking matrix computed by diffusing surface to
%interior for a short amount of time
arguments;
V; F; 
dt = mean(edge_lengths(V, edges(F))).^2;
end;

bI = unique(boundary_faces(F));
bc = ones(size(bI));

M = massmatrix(V, F);
L = -cotmatrix(V, F);

Z = zeros(size(L, 1), 1);
Z(bI) = bc;
phi = min_quad_with_fixed(dt*L + M, zeros(size(L, 1), 1), bI, bc);
phi = phi - min(phi);
phi = phi ./ max(phi);

phi = 1 - phi;

phi = kron(speye(2), diag(phi));


end

