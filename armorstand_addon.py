
bl_info = {
    "name": "Armorstand Extension",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import WorkSpaceTool

def export_animation(context,start,end,filepath,loop):
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    f = open(filepath, 'w', encoding='utf-8')
    f.write("scoreboard objectives add armorstand_animation dummy\n")
    
    armature = bpy.context.view_layer.objects.active
    
    bpy.ops.object.mode_set(mode='POSE', toggle=False)
    
    rememberFrame = bpy.context.scene.frame_current
    
    pi = 3.14
    
    for i in range(start,end+1):
        context.scene.frame_set(i)
        context.view_layer.update()
        
        body = armature.pose.bones["Main"].rotation_euler
        ll = armature.pose.bones["LeftLeg"].rotation_euler
        rl = armature.pose.bones["RightLeg"].rotation_euler
        la = armature.pose.bones["LeftArm"].rotation_euler
        ra = armature.pose.bones["RightArm"].rotation_euler
        he = armature.pose.bones["Head"].rotation_euler
        print(he[0]*180/pi)
        f.write("execute if score @s armorstand_animation matches "+str(i)+" run data merge entity @s {Pose:{"+
            "LeftLeg:["+str(ll[0]* 180/pi)+"f,"+str(ll[1]* 180/pi)+"f,"+str(ll[2]* 180/pi)+"f],"+
            "RightLeg:["+str(rl[0]* 180/pi)+"f,"+str(rl[1]* 180/pi)+"f,"+str(rl[2]* 180/pi)+"f],"+
            "LeftArm:["+str(la[0]* 180/pi)+"f,"+str(la[1]* 180/pi)+"f,"+str(la[2]* 180/pi)+"f],"+
            "RightArm:["+str(ra[0]* 180/pi)+"f,"+str(ra[1]* 180/pi)+"f,"+str(ra[2]* 180/pi)+"f],"+
            "Head:["+str(he[0]* 180/pi)+"f,"+str(he[1]* 180/pi)+"f,"+str(he[2]* 180/pi)+"f]"+
            "},Rotation:["+str(body[1]* 180/pi)+"f,0.0f]}\n")
            
    if(loop):
        f.write("execute if score @s armorstand_animation matches "+str(end)+".. run scoreboard players set @s armorstand_animation 0\n")
            
    f.write("scoreboard players add @s armorstand_animation 1\n")
    
    f.close()
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    context.scene.frame_set(rememberFrame)
        
    return {'FINISHED'}
    

class CreateArmorStand(bpy.types.Operator):
    """Creates a new Armorstand"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.armorstand"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Create Armorstand"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    
    def execute(self, context):        # execute() is called when running the operator.

        bone_positions = [
            [[0,0,1.375],[0,0,0.75]],
            [[-0.125,0,0.0625],[-0.125,0,0.75]],
            [[0.125,0,0.0625],[0.125,0,0.75]],
            [[-0.3125,0,0.75],[-0.3125,0,1.375]],
            [[0.3125,0,0.75],[0.3125,0,1.375]],
            [[0,0,1.875],[0,0,1.4375]]
        ]
        
        bone_names = [
            "Main",
            "RightLeg",
            "LeftLeg",
            "RightArm",
            "LeftArm",
            "Head"
        ]
        
        
        bone_locks = [
            [True,False,True],
            [False,False,True],
            [False,False,True],
            [False,False,True],
            [False,False,True],
            [False,False,True]    
        ]
    
        #create armature
        bpy.ops.object.armature_add()
        armature = context.object
        context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        
        edit_bones = armature.data.edit_bones
        
        for i in range(1,len(bone_positions)):
            b = edit_bones.new('bone')
            
        for i,b in enumerate(edit_bones):
            #bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        
            b.name = bone_names[i]
            b.head.x = bone_positions[i][1][0]
            b.head.y = bone_positions[i][1][1]
            b.head.z = bone_positions[i][1][2]
            b.tail.x = bone_positions[i][0][0]
            b.tail.y = bone_positions[i][0][1]
            b.tail.z = bone_positions[i][0][2]
            
            
            if(i > 0): 
                 b.parent = edit_bones[0]
            
            
        bpy.ops.object.mode_set(mode="POSE")
        
        for i,b in enumerate(bone_locks):
            #cst = armature.pose.bones[i].constraints.new(type='LIMIT_ROTATION')
            armature.pose.bones[i].rotation_mode = "XYZ"
            armature.pose.bones[i].lock_rotation[0] = b[0]
            armature.pose.bones[i].lock_rotation[1] = b[1]
            armature.pose.bones[i].lock_rotation[2] = b[2]
        
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            
        armature.name = "Armorstand"
        
        bpy.ops.mesh.primitive_cube_add(location=(0.0, -0.15, 0))
        bpy.ops.transform.resize(value=(0.025, 0.2, .001))
        
        marker = bpy.context.object
        marker.parent = armature
        marker.name = "forward"

        context.view_layer.objects.active = armature
        
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
            
        return {'FINISHED'}
    
class ExportMcFunction(bpy.types.Operator,ExportHelper):
    """Exports the animationas an mcfunction"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "ops.mcexport"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Export Animation (.mcfunction)"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # ExportHelper mixin class uses this
    filename_ext = ".mcfunction"

    filter_glob: StringProperty(
        default="*.mcfunction",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )
    
    start_frame : bpy.props.IntProperty(
        name = "Start Frame",
        description="Begin of export timeframe",
        step = 1,
        default = 0,
        min=0
    )
    end_frame : bpy.props.IntProperty(
        name = "End Frame",
        description="End of export timeframe",
        step = 1,
        default = 250,
        min=1
    )
    
    
    loop_animation : bpy.props.BoolProperty(
        name = "Loop Animation",
        description="If the animation should start again after finishing",
    )
    
    def execute(self, context):        # execute() is called when running the operator.
        return export_animation(context,self.start_frame,self.end_frame,self.filepath,self.loop_animation)

class ArmorstandSetup(bpy.types.Operator):
    bl_idname = "wm.armorstand_setup"
    bl_label = "Setup Armorstand Scene"

        
    def execute(self, context):
        scn = bpy.context.scene
        scn.frame_current = 0
        scn.render.fps = 20
        

        for obj in bpy.data.objects:
            if (obj.type == "CAMERA" or obj.type == "LIGHT"):
                bpy.data.objects.remove(obj, do_unlink=True)
                
        try:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        except:
            pass
        
        bpy.ops.object.armorstand()
            
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
    
        return {'FINISHED'}
    
### Info.
class VIEW3D_PT_armorstand(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Armorstand"
    bl_label = "Minecraft Armorstand"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.armorstand_setup", text="Setup Scene", icon='NONE')
        
def menu_func(self, context):
    self.layout.operator(CreateArmorStand.bl_idname)
    
def menu_func1(self, context):
    self.layout.operator(ExportMcFunction.bl_idname)

def register():
    bpy.utils.register_class(ArmorstandSetup)
    bpy.utils.register_class(CreateArmorStand)
    bpy.utils.register_class(VIEW3D_PT_armorstand)
    bpy.utils.register_class(ExportMcFunction)
    bpy.types.VIEW3D_MT_add.append(menu_func)  # Adds the new operator to an existing menu.
    bpy.types.TOPBAR_MT_file_export.append(menu_func1)

def unregister():
    bpy.utils.unregister_class(ArmorstandSetup)
    bpy.utils.unregister_class(CreateArmorStand)
    bpy.utils.unregister_class(VIEW3D_PT_armorstand)
    bpy.utils.unregister_class(ExportMcFunction)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()