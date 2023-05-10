function u_next = arap_global_step(u, sim, spre, dpre, r)
%REDUCED_ARAP_GLOBAL_STEP Summary of this function goes here
%   Detailed explanation goes here

     inertia =  -dpre.My;
    
     arap =  spre.Lx - spre.MK' * r;
     
     g = sim.invh2 * sim.do_inertia * inertia +  arap + dpre.f_ext ;
     [u_next] = min_quad_with_fixed(spre.A, g, [], [],  sim.Aeq, dpre.bc, spre.factorization);
     u_next = u_next(1:size(u, 1));
end

