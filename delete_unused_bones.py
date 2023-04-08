import bpy

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