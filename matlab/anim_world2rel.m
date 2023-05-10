function [P2] = anim_world2rel(P, P0)
%READ_RIG_FROM_JSON Summary of this function goes here
%   Input:
%       P - #frames x b x 3 x 4 world space rig animation
%       P0 - b x 3 x 4  world space matrix at rest.
%   Ouptut
%       P2 -frames x b x 3 x 4 affine transformation matrices relative to
%       rest

f = size(P, 1);
b = size(P, 2);
d = size(P, 3); 

P2 = zeros(size(P));

homog = [zeros(1, d) 1];
for fi=1:f
    for bi=1:b
        Pi = [squeeze(P(fi, bi, :, :)); homog];
        P0i = [squeeze(P0(bi, :, :)); homog];
        PPi =  (Pi * inv(P0i ));
        P2(fi, bi, :, :) = PPi(1:d, :);
    end
end


end

