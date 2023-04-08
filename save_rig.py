import bpy
import json
import os
import numpy as np
import mathutils
mesh_name = "cd_fish"
rig_name = "skeleton_rig"
anim = "swim"
root_dir = "C:\\Users\\otmanbench\OneDrive - University of Toronto\\fastCD\\aquarium\\"

rig_dir = root_dir + "\\data\\" +mesh_name +"\\rigs\\" + rig_name + "\\";
rig_path = rig_dir  + rig_name + ".json"
anim_path =  rig_dir + "\\anim\\" +  anim+".json"


    #run delete_unused_bones
if ("delete_unused_bones.py" not in bpy.data.texts):
    text = bpy.data.texts.load(root_dir + "fast_cd_blender\\delete_unused_bones.py")


def matrix_world(armature_ob, bone_name):
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis

    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name)  @ (parent_local.inverted() @ local) @ basis

def save_rig(output_path, scale_mod=1):

    mod = bpy.data.texts["delete_unused_bones.py"].as_module()
    mod.delete_unused_bones();

    #assumes you have selected your armature
    scene = bpy.context.scene

    #Get mesh
    for scene_obj in scene.objects:
        if (scene_obj.type == "MESH"):
            mesh_name = scene_obj.name

    for scene_obj in scene.objects:
        if (scene_obj.type == "ARMATURE"):
            rig_name = scene_obj.name
            


    armature = bpy.data.objects[rig_name]
    root_transform = armature.matrix_world
     

    bones =  armature.data.bones
    pose_bones =  armature.pose.bones
    
    first_bone_transform = bones[0].matrix_local
    #to get world matrix do:
    world_bone_matrix = root_transform  @ first_bone_transform;


    obj = bpy.data.objects[mesh_name]
    n = len(obj.data.vertices);
    #print(n, "vertices");
    vertex_groups = obj.vertex_groups
    vertices = obj.data.vertices


    V = [[vert.co.x, vert.co.y, vert.co.z] for vert in obj.data.vertices]
     
    F = [[vert for vert in polygon.vertices] for polygon in obj.data.polygons]
    print("saving rig")
    #save dict describing each bone in this list
    json_bone_entries = []
    
    lengths = [];
    T0 = [];
    pI = [];
    W = [];
    #save bone weights
    Rx = mathutils.Matrix.Rotation(-np.pi/2, 4, 'X'); # the bone matrices all have z pointing up, y pointing forwards... want z pointing backwards, y pointing up
   
    for pose_bone in pose_bones:
       # print(pose_bone.name)
        bone = bones[pose_bone.name]
        #print(bone.name)
        bone_idx= vertex_groups[bone.name].index
     
        if bone.parent is None:
            parent_idx = -1;
     
        else:
            parent_idx = vertex_groups[bone.parent.name].index 
        
        pI.append(parent_idx)
        bone_transform = scale_mod * Rx @ root_transform  @ bone.matrix_local
        bone_transform = [list(vector[:]) for vector in list(bone_transform[:-1])]
        #print(bone_transform);
        T0.append(bone_transform);
        
        bone_length = bone.length   
        lengths.append(bone_length);
        #vertex indices of bxone
        vert_indeces_of_bone = []
        #weights associated with each vertex in bone\
        #following https://blender.stackexchange.com/questions/74461/exporting-weight-and-bone-elements-to-a-text-file
        weights_of_bone = []
        for count, v in enumerate(vertices):
            v_groups = [g.group for g in v.groups]
            if bone_idx in v_groups:
                vert_indeces_of_bone.append(count)
                w = vertex_groups[bone_idx].weight(count)
                weights_of_bone.append(w)
    
      #  print(weights_of_bone);
        w = np.zeros((n));
        w[vert_indeces_of_bone] = weights_of_bone;
    #    print(w.shape);
        W.append(w.T.tolist())
        #print(W);
        #print(weights_of_bone);
        #print(vert_indeces_of_bone);
       # a * 0
      #  json_bone = {'bone_idx' : bone_idx, 'parent_idx' : parent_idx, 'bone_transform' : bone_transform, 
    #    'bone_length' : bone_length, 'vert_indeces_of_bone' : vert_indeces_of_bone, 'weights_of_bone' : weights_of_bone}
        #json_bone_entries.append(json_bone)

    #save rest state rig data
    data = {"rig_type" : "surface", "pI" : pI,  "p0" :T0, "W": np.array(W).T.tolist(), "lengths" : lengths, "V" : V, "F": F};
 #   data = {'format': 
#        'surface','rig_type': 'lbs_rig','bones' : json_bone_entries, 'vertices': V, 'faces': F}
    with open(output_path, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    print("Done!")


def save_animation(output_path, scale_mod=1.0):
     #should abstrac tthis away 
     #run delete_unused_bones
    if ("delete_unused_bones.py" not in bpy.data.texts):
        text = bpy.data.texts.load("C:\\Users\\otman\\OneDrive\\Desktop\\fastComplementaryDynamicsCpp\\blender\\delete_unused_bones.py")

    mod = bpy.data.texts["delete_unused_bones.py"].as_module()
    mod.delete_unused_bones();
    #assumes you have selected your armature
    scene = bpy.context.scene
    
    #Get mesh
    for scene_obj in scene.objects:
        if (scene_obj.type == "MESH"):
            mesh_name = scene_obj.name

    for scene_obj in scene.objects:
        if (scene_obj.type == "ARMATURE"):
            rig_name = scene_obj.name
            


    armature = bpy.data.objects[rig_name]
    root_transform = armature.matrix_world
     

    bones =  armature.data.bones
    pose_bones =  armature.pose.bones
    first_bone_transform = bones[0].matrix_local
    Rx = mathutils.Matrix.Rotation(-np.pi/2, 4, 'X'); # the bone matrices all have z pointing up, y pointing forwards... want z pointing backwards, y pointing up
   
    #to get world matrix do:
    world_bone_matrix = Rx @ root_transform  @ first_bone_transform;


    obj = bpy.data.objects[mesh_name]
    vertex_groups = obj.vertex_groups
    vertices = obj.data.vertices


    print("saving_animation")
    world_space_matrix_animation = [];
    
    scene.frame_set(1) 
    bone_rest_matrices = []; 
    for pose_bone in armature.pose.bones:
        T0 = scale_mod * Rx @ root_transform  @ matrix_world(armature, pose_bone.name)
    #    print("T0 ", T0);
        bone_rest_matrices.append(T0.inverted());
    
 
    for frame in range(scene.frame_end + 1):
        bone_matrices_at_frame = [] ;
        scene.frame_set(frame)
        i = 0
        for pose_bone in armature.pose.bones:
            T =  scale_mod * Rx @ root_transform  @ matrix_world(armature, pose_bone.name)
            T =  T;
            pose_bone_world = [list(vector[:]) for vector in list(T[:-1])]
        
            bone_matrices_at_frame.append(pose_bone_world);
            i += 1
        world_space_matrix_animation.append(bone_matrices_at_frame)

   # print(world_space_matrix_animation)
    anim = {'P' : world_space_matrix_animation}
    with open(output_path, 'w') as outfile:
        json.dump(anim, outfile,indent=2)

    print("Done!")
    

if not os.path.exists(os.path.dirname(rig_path)):
  # Create a new directory because it does not exist 
  os.makedirs(os.path.dirname(rig_path))
if not os.path.exists(os.path.dirname(anim_path)):
    os.makedirs(os.path.dirname(anim_path))

save_rig(rig_path)
save_animation(anim_path)
        #print("parent index of  bone "  + str(bone_idx) + " is " +  str(parent_idx))             
                #print(True)
       # print("num weight associated with bone " + str(bone_idx) + " : " + str(len(weights_of_bone)));
        
       # print("num vertices associated with bone " + str(bone_idx) + " : " + str(len(vert_indeces_of_bone))); 
        
       # groups_of_vertex = list(v.groups)
       # print( vertex_groups[bone.name] in groups_of_vertex)
     #   print(groups_of_vertex)
       # if vertex_groups[bone.name] in groups_of_vertex:
       #     vert_indeces_of_bone.append(count)
    
   # print("vert indices associated with bone " + str(bone_idx) + " : " + str(vert_indeces_of_bone)); 
    
    #bone index children of bone
    #bone_dict = {'bone_index': gidx, 'vertex_ind' : vert_indeces_of_bone}
         
    #bone_verts = [v for v in mesh.vertices if gidx in [g.group for g in v.groups]]
    #print(bone_verts)
    #w = mesh.vertices.groups[gidx]
    #print(vg[bone.name].index)

#print([list(tri.vertices[:]) for tri in mesh.loop_triangles])
#mesh.calc_loop_triangles()
#for tri in mesh.loop_triangles:
#    print(list[tri.vertices[:]])
