function [P] = read_rig_from_json(filepath, o)
%READ_RIG_FROM_JSON Summary of this function goes here
%   Input:
%       filepath - filepath to .json rig file outputted by riggrats
%   Ouptut
%       P -frames x b x 3 x 4 affine transformation matrices for each bone
arguments
    filepath;
    o.d=3; 
end
fid = fopen(filepath); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
json = jsondecode(str);
P = json.P;

if (numel(size(P)) == 3)
    P = reshape(P, size(P, 1), 1, size(P, 2), size(P, 3));
end 

if (o.d==2);
    % assumes from blender and that z is up!
    P2d = P( :, :, [1 2], [1 2 4])
    P = P2d;
end
end

