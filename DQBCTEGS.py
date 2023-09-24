bl_info = {
    "name" : "DQ: Blender Collection To Empty Godot Saver",
    "author" : "Prof/Swat",
    "description" : "Exports scene to godot with collections",
    "blender" : (3, 5, 0),
    "location" : "View3D",
    "category" : "Import-Export"
}

import bpy
import os 
import shutil
import time
from bpy.app.handlers import persistent 

new_file_prefix = "godot_"
empties = []

# creates a new empty for each collection
def modify_collection(parent, depth=0):
    
    # recursively checks collections inside of current collection
    for collection in parent.children:
        modify_collection(collection, depth + 1)
    
    # creates new empty for this collection
    if(parent != bpy.context.scene.collection):
        new_empty = bpy.data.objects.new("empty", None)
        new_empty.name = parent.name
        new_empty.location = (0, 0, 0)
        
        # parents objects in this collection to new empty
        for obj in parent.objects:
            if obj.parent == None:
                obj.parent = new_empty
        
        bpy.data.collections[parent.name].objects.link(new_empty)        
        
        # parents child empties to current empty
        for obj in empties:
            if obj["empty"].parent == None and obj["depth"] == depth + 1:
                obj["empty"].parent = new_empty
        
        # adds new empty to the list
        empties.append({"empty": new_empty, "depth": depth})

# Goes through a parent array, renames parents and children.
def apply_imp_flag_to_hierarchy(parent):
    parentPaths = get_paths_of_flagged_children("-imp", parent)
        
    for parentPath in parentPaths:
        for parent in parentPath:
            if "-noimp" in parent.name:
                convert_directory_to_flag("-noimp", "-imp", parent)
                break;

# Gets all collections with the -col flag and applies col to all its subchildren.
def apply_col_flag_to_hierarchy(parent):
    collidable_collections = get_flagged_collections("-col", parent)

    for collection in collidable_collections:
        print(collection)
        convert_directory_to_flag("-col", "-nocol", collection)

# Take a directory and apply a flag to all subchildren.
def convert_directory_to_flag(flag, flagInverse, parent):
    if flag in parent.name:
        parent.name = parent.name.replace(flag, "");
    
    for child in parent.children:
        convert_directory_to_flag(flag, flagInverse, child)
    for object in parent.objects:
        print(object.name)
        print(flag not in object.name)
        if flagInverse in object.name:
            object.name = object.name.replace(flagInverse, "");
        elif flag not in object.name:
            object.name = object.name + flag
            print("renamed to " + object.name)

# Returns "paths" leading to a collection with a specified flag.
def get_flagged_collections(flag, parent):
    impPathArray = []
    
    # get discovered paths of the children.
    for child in parent.children:
        impPathArray = [*impPathArray, *get_flagged_collections(flag, child)]

    if flag in parent.name:
        impPathArray = [*impPathArray, parent]

    return impPathArray

# Returns "paths" leading to a child with a specified flag.
def get_paths_of_flagged_children(flag, parent, pathArray = []):
    pathArray = [*pathArray, parent]
    impPathArray = []
    
    # get discovered paths of the children
    for child in parent.children:
        impPathArray = [*impPathArray, *get_paths_of_flagged_children(flag, child, pathArray)]
    
    # as child, if theres -imp return path array.
    if parent is not bpy.context.scene.collection:        
        for object in parent.objects:
            if flag in object.name:
                impPathArray = [*impPathArray, pathArray]

    return impPathArray
    
# checks if the file is being saved
@persistent
def save_handler(scene):    
    blender_filepath = bpy.data.filepath
    godot_filepath = os.path.dirname(blender_filepath) + "\\" + new_file_prefix + bpy.path.display_name_from_filepath(blender_filepath) + ".blend"
    
    bpy.app.handlers.save_post.clear()
        
    bpy.ops.wm.save_as_mainfile(filepath=blender_filepath, copy=True)
    # modify this version and save it to godot
    scene_col = bpy.context.scene.collection
    apply_col_flag_to_hierarchy(scene_col)
    apply_imp_flag_to_hierarchy(scene_col)
    modify_collection(scene_col)
    

    bpy.ops.wm.save_as_mainfile(filepath=godot_filepath, copy=True)
    bpy.ops.wm.open_mainfile(filepath=blender_filepath)
    
    empties.clear()
    bpy.app.handlers.save_post.append(save_handler)

def register():
    bpy.app.handlers.save_post.clear()
    bpy.app.handlers.save_post.append(save_handler)

def unregister():
    bpy.app.handlers.save_post.clear()
    
if __name__ == "__main__":
    bpy.app.handlers.load_post.append(register)
