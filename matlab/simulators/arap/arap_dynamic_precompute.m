function dpre = arap_dynamic_precompute(z_hist, sim_params, spre, f_ext, bc)
%ARAP_DYNAMIC_PRE Summary of this function goes here
%   Detailed explanation goes here

arguments
    z_hist;
    sim_params; spre;
    f_ext = zeros(size(z_hist));
    bc = zeros(size(spre.Aeq, 1), 1);
end
dpre = {};

dpre.f_ext = -f_ext;

dpre.bc = bc;
dpre.My =spre.M*z_hist;

end

