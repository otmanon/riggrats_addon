close all;
clear;

[V0, F, W, P0] = read_rig_from_json("./data/michelle/rig.json");
P = read_anim_from_json("./data/michelle/walk.json");

W = W ./ sum(W, 2);
ff = size(P, 1); % number of frames;
bb = size(P, 2);
Prel = anim_world2rel(P, P0);
% Prel = P;
Prel2 = permute(Prel, [4 2 3 1]);
 size(squeeze(Prel2))
 Prel3 = reshape(squeeze(Prel2), [], ff);
Preli = Prel3(:, 40)
p = Preli(:);
PP = reshape(p, [], 3)


J = lbs_jacobian(V0, W);

figure();
set(gcf, 'Position', [10 10 1080 1080])
hold on;
axis equal;
axis([-0.5 0.5 0.0 1.5]*200)
grid on;
t1 = tsurf(F, V0, 'EdgeAlpha', 0.1);
set(gcf,'color','w');

step = 1;
while (true)
     Preli = Prel3(:, mod(step, ff)+1);

     p = Preli(:);
     V = reshape(J*p, [], 3);
    
%      C2 = PP(end, :);

     t1.Vertices = V;
     drawnow;
     step = step + 1;

end