close all;
clear;



%% Load Rig stuff
[V0, F] = readOBJ("./data/green/green.obj");
V0 = V0(:, 1:2)

%% Simulation Parameters
ym = 100           
max_steps = 400;    
sim_params = default_sim_params(V0, F, ym=ym);
solver_params = default_local_global_solver_params();
sim = arap_sim(sim_params, solver_params);





clf;
hold on;
axis equal;
face_alpha = 0.5;
edge_alpha = 0.1;
t = tsurf(F,V0, 'FaceAlpha', face_alpha, 'EdgeAlpha', edge_alpha);
drawnow;

a = 0.1;
u = (rand(numel(V0), 1)-0.5); %zeros(numel(V0), 1);
u_curr = u; u_prev = u; u_hist = u;



%% Simulation Loop
for step=0:max_steps
    u_hist = 2*u_curr - u_prev; % displacement history for inertia
    
    
    f_ext = zeros(numel(V0), 1);
    u_next = sim.step(u_curr, u_hist, f_ext, []);
  
    % update state of simulation
    u_prev = u_curr;
    u_curr = u_next;           
    
    U = reshape(u_curr, size(u_curr, 1)/2, 2);
    
    t.Vertices = U + V0;
    drawnow;
end
