function [V, F, W, P0, pI, l, rig_type] = read_rig_from_json(filepath)
%READ_RIG_FROM_JSON Summary of this function goes here
%   Input:
%       filepath - filepath to .json rig file outputted by riggrats
%   Ouptut
%       V - n x 2 (or 3)mesh geometry
%       F - f x 3 (or 4) triangle (or tet) mesh indices
%       W - n x b bone weights
%       P0 -b x 3 x 4 affine transformation matrices for each bone
%       pI - b x 1 parent bone indices
%       l  - bone lengths
%       rig_type - string ("surface" or "volume")
fid = fopen(filepath); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
json = jsondecode(str);

V = json.V;
F = json.F + 1; % cpp/python indexes at 0
W = json.W;
l = json.lengths;
P0 = json.p0;
pI = json.pI + 1;
rig_type = json.rig_type;
end

