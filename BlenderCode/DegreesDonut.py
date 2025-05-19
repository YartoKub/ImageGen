import bpy
from math import radians
from mathutils import Vector
import numpy as np
import os

def x_rotation(vector,theta):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    return np.dot(R,vector)

def y_rotation(vector,theta):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R,vector)

def z_rotation(vector,theta):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])
    return np.dot(R,vector)

#bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0,0,0), scale=(1, 1, 1))
#empty = bpy.context.active_object
#empty.name = "center"

bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0,0,0), scale=(1, 1, 1))
light = bpy.context.active_object
light.name = "Plight"

#light.parent = empty

light.data.energy = 100
# DEGREES
y_donut_degrees = 360 # CONSTANT
x_thicc_degrees_start = -30 
x_thicc_degrees_end =    30 
# STEPS
y_donut_step_number = 60
x_thicc_step_number = 10
# DEGREE CHANGE
y_donut_degree_change = round(y_donut_degrees / y_donut_step_number)
x_thicc_degree_change = round((x_thicc_degrees_end - x_thicc_degrees_start) / (x_thicc_step_number - 1))
# FRAMES
total_frames = y_donut_step_number * x_thicc_step_number
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = total_frames
# DATA
rotationNames = ""
for y in range(0, y_donut_step_number):
    for x in range(0, x_thicc_step_number):
        #empty.rotation_euler = ( radians(x_thicc_degrees_start + x_thicc_degree_change * x),  radians(y_donut_degree_change * y),   0.0) 
        default_vector = np.array([0,0,1])
        default_vector = x_rotation(default_vector, radians(x_thicc_degrees_start + x_thicc_degree_change * x))
        default_vector = y_rotation(default_vector, radians(y_donut_degree_change * y))
        
        light.location = default_vector #* 0.4
        light.keyframe_insert(data_path="location", frame=y * x_thicc_step_number + x)
        default_vector = default_vector.round(3)
        cx = default_vector[0]
        cy = default_vector[1]
        cz = default_vector[2]
        #print(y * x_thicc_step_number + x)
        rotationNames += ("ImageNum" + str(y * x_thicc_step_number + x) + "VectorXYZ" + str(cx) + "_" + str(cy) + "_" + str(cz))

        #rotationNames.append("x" + (str)(degree_change * y) + "z" + (str)( degree_change * x))
        #
        #default_vector = np.array([0,1,0])
        #default_vector = x_rotation(default_vector, radians(x_thicc_degrees_start + x_thicc_degree_change * x))
        #default_vector = y_rotation(default_vector, radians(y_donut_degree_change * y))
        #rotationNames.append(default_vector)
# danger zone
#import time
#print(os.path.dirname(os.path.abspath(__file__)))

with open("D:\MyBlender\ImageGenFinished\copy.txt", "w") as file:
    file.write(rotationNames)
print(rotationNames)


"""
scene = bpy.context.scene
for frame in range(scene.frame_start, scene.frame_end + 1):
    scene.render.filepath = 'D:/MyBlender/imageGenFinished/' + str(frame).zfill(4) + rotationNames[frame - 1]
    scene.frame_set(frame)
    bpy.ops.render.render(write_still=True)
    time.sleep(0.1)

"""
#bpy.ops.mesh.primitive_uv_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(-0.326196, 0.0291865, 1.29371), scale=(1, 1, 1))
