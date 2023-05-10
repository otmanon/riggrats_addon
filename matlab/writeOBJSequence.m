function   writeOBJSequence(output_dir, Vs, F,o)
%WRITEOBJSEQUENCE Summary of this function goes here
%   Detailed explanation goes here
arguments;
output_dir; Vs; F;
o.d = 3;
o.UV = zeros(0, 2 );
o.UVF = zeros(0, 3 );
o.N = zeros(0, 3);
o.NF = zeros(0, 3);
end
mkdir(output_dir)
for i = 1:size(Vs,1)
    V = reshape(Vs(i, :), [], o.d);
    output = strcat(output_dir, "./", num2str(i, '%04.f'), ".obj");
    writeOBJ(output, V, F, o.UV, o.UVF, o.N, o.NF);
end

end

