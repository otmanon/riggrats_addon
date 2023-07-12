import bpy
import json
import os
import numpy as np
import mathutils


bl_info = {
    "name": "rigrats",
    "blender": (3, 30, 0),
    "category": "Object",
}

    

def delete_unused_bones():
    bpy.ops.object.mode_set(mode='EDIT')
    scene = bpy.context.scene

    #Get mesh
    for scene_obj in scene.objects:
        if (scene_obj.type == "MESH"):
            mesh_name = scene_obj.name

    for scene_obj in scene.objects:
        if (scene_obj.type == "ARMATURE"):
            rig_name = scene_obj.name
            
    save_animation = True
    #assumes you have selected your armature

    armature = bpy.data.objects[rig_name]
     

    bones =  armature.data.bones
    edit_bones = armature.data.edit_bones


    #
    obj = bpy.data.objects[mesh_name]
    vertex_groups = obj.vertex_groups
    vertices = obj.data.vertices


    print("looping through bones")
    #save dict describing each bone in this list

    #save bone weights
    for bone in bones:
        
        if (bone.name in vertex_groups):
            bone_idx= vertex_groups[bone.name].index
        else:
            #bone ain't got no weights
            edit_bone_to_be_removed = edit_bones[bone.name]
            armature.data.edit_bones.remove(edit_bone_to_be_removed);
            continue
     
       
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
        print("consideriremoving bone : ", bone.name)
        print(len(weights_of_bone))
        if(len(vert_indeces_of_bone) == 0):
            print("removing bone : ", bone.name)
            edit_bone_to_be_removed = edit_bones[bone.name]
            armature.data.edit_bones.remove(edit_bone_to_be_removed);
          #  armature.data.bones.remove(bone);
            vertex_groups.remove(vertex_groups[bone.name]);
    bones.update()
            
    print("New vertex groups of length, " , len(vertex_groups))
        
    
    bpy.ops.object.mode_set(mode='OBJECT')

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

    #delete_unused_bones();

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
    Rx = mathutils.Matrix.Rotation(0, 4, 'X'); # the bone matrices all have z pointing up, y pointing forwards... want z pointing backwards, y pointing up
   
    bone_dict = {}
    i = 0
    # put all bones in dict
    for pose_bone in pose_bones:
        bone = bones[pose_bone.name]
        bone_dict[bone.name] = i
        i += 1
        
    for pose_bone in pose_bones:
       # print(pose_bone.name)
        bone = bones[pose_bone.name]
        #print(bone.name)
        bone_idx= vertex_groups[bone.name].index
     
        if bone.parent is None:
            parent_idx = -1;
        else:
            parent_idx = bone_dict[bone.parent.name]
    
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

    #delete_unused_bones();
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
    Rx = mathutils.Matrix.Rotation(0, 4, 'X'); # the bone matrices all have z pointing up, y pointing forwards... want z pointing backwards, y pointing up
   
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
    


class rigrats_save_rig(bpy.types.Operator):
    """Saves the Rig to A .json file"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.save_rig"        # Unique identifier for buttons and menu items to reference.
    bl_label = "rigrats: save to .json"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    # moved assignment from execute() to the body of the class...
    
#    total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)
#    name: bpy.props.StringProperty(name="name", default="my_rigged_mesh")
    save_rig : bpy.props.BoolProperty(name="Save Rig", default=False);
    rig_filepath: bpy.props.StringProperty(name="rig filepath", default="//rig.json")
    
    save_anim : bpy.props.BoolProperty(name="Save Rig Anim", default=False);
    anim_filepath: bpy.props.StringProperty(name="anim filepath", default="//anim.json")
    

    # and this is accessed on the class
    # instance within the execute() function as...
    def execute(self, context):        # execute() is called when running the operator.        
        if(self.save_rig):
            rig_filepath = bpy.path.abspath(self.rig_filepath);
            
            if not os.path.exists(os.path.dirname(rig_filepath)):
          # Create a new directory because it does not exist 
                os.makedirs(os.path.dirname(rig_filepath))
            save_rig(rig_filepath)
            
        if(self.save_anim):
            anim_filepath = bpy.path.abspath(self.anim_filepath);
            
            if not os.path.exists(os.path.dirname(anim_filepath)):
          # Create a new directory because it does not exist 
                os.makedirs(os.path.dirname(anim_filepath))
            save_animation(anim_filepath)
        return {'FINISHED'}
    
def menu_func(self, context):
    self.layout.operator(rigrats_save_rig.bl_idname)

def register():
    bpy.utils.register_class(rigrats_save_rig)
    bpy.types.VIEW3D_MT_object.append(menu_func)  # Adds the new operator to an existing menu.

def unregister():
    bpy.utils.unregister_class(rigrats_save_rig)
    
    
# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
#if not os.path.exists(os.path.dirname(anim_path)):
#    os.makedirs(os.path.dirname(anim_path))
#save_animation(anim_path)
       