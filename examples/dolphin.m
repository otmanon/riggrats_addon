close all;
clear;

[V0, F, W, P0] = read_rig_from_json("./data/dolphin/fin_bone_rig.json", d=2);


P = read_anim_from_json("./data/dolphin/anim.json", d=2)

W = W ./ sum(W, 2); % blender doesnt guarantee the sum to 1 property exactly
ff = size(P, 1); % number of frames;
bb = size(P, 2); % number of bones;

Prel = anim_world2rel(P, P0);       %lbs works on rest-to-deformed world space matrices
Prel2 = permute(Prel, [4 2 3 1]); % flatten this the way lbs_jacobian expects
Prel = reshape(squeeze(Prel2), [], ff);

J = lbs_jacobian(V0, W);

figure();
set(gcf, 'Position', [10 10 600 600])
hold on;
axis equal;
grid on;
t1 = tsurf(F, V0, 'EdgeAlpha', 0.1);
set(gcf,'color','w');

step = 1;
while (true)
     Preli = Prel(:, mod(step, ff)+1);

     p = Preli(:);
     V = reshape(J*p, [], 2);
    
     t1.Vertices = V;
     drawnow;
     step = step + 1;

end