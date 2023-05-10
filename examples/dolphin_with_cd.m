close all;
clear;

do_cd = true;
ym = 200 ; % youngs modulus stiffness
max_steps = 100; 

save_video = true;

%% Load Rig stuff
[V0, F, W, P0] = read_rig_from_json("./data/dolphin/skeleton_rig.json", d=2);
P = read_anim_from_json("./data/dolphin/anim.json", d=2)

W = W ./ sum(W, 2); % blender doesnt guarantee the sum to 1 property exactly
ff = size(P, 1); % number of frames;
bb = size(P, 2); % number of bones;

Prel = anim_world2rel(P, P0);       %lbs works on rest-to-deformed world space matrices
Prel2 = permute(Prel, [4 2 3 1]); % flatten this the way lbs_jacobian expects
Prel = reshape(squeeze(Prel2), [], ff);

J = lbs_jacobian(V0, W);


%% Simulation Parameters

uc =zeros(numel(V0), 1)
ur =J*Prel(:, 1) - V0(:);;% assume no rig displacement at the start
u = uc + ur;
u_curr = u; u_prev = u; u_hist = u;

% complementarity constraint.

M = repdiag(massmatrix(V0, F, 'barycentric'), 2);
D =otman_D_matrix(V0, F).^2; % momentum leaking matrix
Aeq = (D *M*J)';
bc = zeros(size(Aeq, 1), 1);
   
sim_params = default_sim_params(V0, F, ym=ym, Aeq=Aeq);
solver_params = default_local_global_solver_params();
sim = arap_sim(sim_params, solver_params);

if(save_video)
    v = VideoWriter('./dolphin_cd.mp4','MPEG-4');
    v.Quality = 100;
    v.FrameRate = 24;
    open(v)
end;


clf;
hold on;
axis equal;
face_alpha = 0.5;
edge_alpha = 0.1;
axis([-1 1 -1 1]*2)
t = tsurf(F,V0, 'FaceAlpha', face_alpha, 'EdgeAlpha', edge_alpha);
axis off;
drawnow;

Vs = [];
%% Simulation Loop
for step=1:max_steps

    ur = J*Prel(:, mod(step, size(Prel, 2))+1) - V0(:); % get rig displacement;
    if (do_cd)
        u_hist = 2*u_curr - u_prev; % displacement history for inertia    
        f_ext = zeros(numel(V0), 1);
        bc = -J'*M*ur;
        u = sim.step(u_curr, u_hist, f_ext, Aeq*(ur));
     
        % update state of simulation
        u_prev = u_curr;
        u_curr = u;            
    else
        u = ur;
    end
    
    U = reshape(u, [], 2);
    
    t.Vertices = U + V0;
   
    drawnow;


  if(save_video)
        frame = getframe(gcf);
        writeVideo(v,frame);
    end
   
    Vs = [Vs, U(:) + V0(:)];
end

if save_video
    writeVideo(v,frame);
    close(v);
end


writeOBJSequence("./siqi_dolphin_recording/", Vs', F, d=2)
