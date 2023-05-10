function z_next = arap_local_global_solver(z, sim_params, dpre, spre, solver_params)
%ARAP_CD_LOCAL_GLOBAL_SOLVER Summary of this function goes here
%   Detailed explanation goes here
  iter = 1;
  while(1)
      [r] = arap_local_step(z, sim_params, spre, dpre);
      z_next = arap_global_step(z, sim_params, spre, dpre, r);
      
      r = norm(z_next - z, 'inf');
      
      if (solver_params.to_convergence)
        if ( r < solver_params.convergence_threshold)
          %if (e < threshold)
              %disp(strcat('residual norm : ', string(r)));
            break;
      end;
      elseif iter == solver_params.max_iters
          break;
      end
      z = z_next;
      iter = iter + 1;
  end

end


