close all;
clear;

[V0, F, W, P0] = read_rig_from_json("./data/dolphin/fin_bone_rig.json", d=2);


CP = squeeze(P0(:, :, 3))

theta = pi/2;
CP = CP;
hold on;
tsurf(F, V0);
scatter(CP(:, 1), CP(:, 2), 'red', 'filled')
P = read_anim_from_json("./data/dolphin/anim.json", d=2)

W = W ./ sum(W, 2); % blender doesnt guarantee the sum to 1 property exactly
ff = size(P, 1); % number of frames;
bb = size(P, 2);
Prel = anim_world2rel(P, P0);
% Prel = P;
Prel2 = permute(Prel, [4 2 3 1]);
 size(squeeze(Prel2))
 Prel3 = reshape(squeeze(Prel2), [], ff);
Preli = Prel3(:, 15)
p = Preli(:);
PP = reshape(p, [], 3)


J = lbs_jacobian(V0, W);

figure();
set(gcf, 'Position', [10 10 1080 1080])
hold on;
axis equal;
grid on;
t1 = tsurf(F, V0, 'EdgeAlpha', 0.1);
set(gcf,'color','w');

step = 1;
while (true)
     Preli = Prel3(:, mod(step, ff)+1);

     p = Preli(:);
     V = reshape(J*p, [], 2);
    
%      C2 = PP(end, :);

     t1.Vertices = V;
     drawnow;
     step = step + 1;

end