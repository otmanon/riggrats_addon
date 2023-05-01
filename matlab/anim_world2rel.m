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
P2 = zeros(size(P));
for fi=1:f
    for bi=1:b
        Pi = [squeeze(P(fi, bi, :, :)); 0 0 0 1];
        P0i = [squeeze(P0(bi, :, :)); 0 0 0 1];
        PPi =  (Pi * inv(P0i ));
        P2(fi, bi, :, :) = PPi(1:3, :);
    end
end

end

