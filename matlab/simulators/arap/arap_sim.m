function sim = arap_sim( sim_params, solver_params )
%REDUCED_CD_SIM Summary of this function goes here
%   Detailed explanation goes here

    sim = {};
    
    sim.params = sim_params;
    sim.solver_params = solver_params;
    sim.spre = arap_static_precompute(sim.params)
    sim.step = @(u, u_hist, f_ext, bc) step(u, u_hist, f_ext, bc, sim.params, sim.solver_params, sim.spre  );
end

function u_next = step(u, u_hist, f_ext, bc, sim_params, solver_params, spre )
    dpre = arap_dynamic_precompute( u_hist,  sim_params, spre, f_ext, bc);
    u_next = arap_local_global_solver(u, sim_params, dpre, spre, solver_params);
end
