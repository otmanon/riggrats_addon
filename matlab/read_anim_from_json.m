function [P] = read_rig_from_json(filepath)
%READ_RIG_FROM_JSON Summary of this function goes here
%   Input:
%       filepath - filepath to .json rig file outputted by riggrats
%   Ouptut
%       P -frames x b x 3 x 4 affine transformation matrices for each bone
fid = fopen(filepath); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
json = jsondecode(str);
P = json.P;
end

