function r = arap_local_step(z, sim_params,  spre, dpre)
%REDUCED_ARAP_LOCAL_STEP Summary of this function goes here
%   Detailed explanation goes here
    f = spre.MKx + spre.MK * z;
    F_stack = reshape(f, size(f, 1)/2, 2);
    
    for i= 1:size(F_stack, 1)/2;
       R = fit_rotation(transpose(F_stack(2*(i-1) + 1: 2*i, 1:2)));
       R_stack(2*(i-1) + 1: 2*i, 1:2) = R;
    end

    r = R_stack(:) ;
end

