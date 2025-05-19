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

bpy.ops.object.light_add(type='POINT', align='WORLD', location=(0,0,0), scale=(1, 1, 1))
light = bpy.context.active_object
light.name = "Plight"

# EDIT HERE TO PICK AN OBJECT
object_name = 'donut'
dude = bpy.data.objects[object_name]
dude_name = object_name

light_distance = 0.9
light.data.energy = 50
def LightArch(x_start_end_steps, y_start_end_steps):
    if x_start_end_steps[2] == 0 or y_start_end_steps[2] == 0: return
    # X DEGREES
    x_degrees_beg = x_start_end_steps[0] 
    x_degrees_end = x_start_end_steps[1]
    x_step_number = x_start_end_steps[2]
    x_degree_change = round((x_degrees_end - x_degrees_beg) / (x_step_number - 1))
    # Y DEGREES
    y_degrees_beg = y_start_end_steps[0] 
    y_degrees_end = y_start_end_steps[1]
    y_step_number = y_start_end_steps[2]
    y_degree_change = round(abs((y_degrees_end - y_degrees_beg)) / (y_step_number - 1))
    
    archVectors = list()
    for y in range(0, y_step_number):
        for x in range(0, x_step_number):
            default_vector = np.array([0,0,1])
            default_vector = x_rotation(default_vector, radians(x_degrees_beg + x_degree_change * x))
            default_vector = y_rotation(default_vector, radians(y_degrees_beg + y_degree_change * y)) 
            archVectors.append(default_vector)
    
    return archVectors

def GetNames(positionList):
    namesList=list()
    for num in range(0, len(positionList)):
        #light.location = positionList[num] #* 0.4
        #light.keyframe_insert(data_path="location", frame=num)
        
        default_vector = positionList[num].round(3)
        cx = default_vector[0]
        cy = default_vector[1]
        cz = default_vector[2]
        namesList.append(("VectorXYZ" + str(cx) + "_" + str(cy) + "_" + str(cz)))
    return namesList
            

arch1 = LightArch((-80, 80, 7), (-80,  80, 7)) # 7, 21
arch2 = LightArch((-30, 30, 2), ( 95,  175, 2))
#arch3 = LightArch((-30, 30, 2), ( 160,  175, 2))
arch4 = LightArch((-30, 30, 2), (-175, -95, 2))
#arch5 = LightArch((-30, 30, 3), (-150, -105, 4))

# + arch3 + arch5
allPoints = arch1 + arch2  + arch4   # THE IMPORTANT THING_1
rotationNames = GetNames(allPoints) # THE IMPORTANT THING_2


head_r_beg = -80
head_r_end = 80
head_r_steps = 10 # 13
head_degree_change = round((head_r_end - head_r_beg) / (head_r_steps - 1))

nod_r_beg = -65
nod_r_end = 65
nod_r_steps = 10 # 7
nod_degree_change = round((nod_r_end - nod_r_beg) / (nod_r_steps - 1))

all_obj_rots = list()
OutPut_ImageNames = "NumberOfLightJumps" + str(len(allPoints))
OutPut_ImageAnswers = ""
for h in range(0, head_r_steps): 
    for n in range(0, nod_r_steps):
        n_radians = nod_r_beg + nod_degree_change * n
        h_radians = head_r_beg + head_degree_change * h
        obj_vector = (radians( n_radians), radians( h_radians), 0.0)
        all_obj_rots.append(obj_vector)
        OutPut_ImageAnswers += dude_name + str(h_radians) + "_" + str(n_radians)
# GET LIGHED IMAGES WITH DIFFERENT ANGLES
for hn in range(0, len(all_obj_rots)): # 25 steps
    vect = all_obj_rots[hn]
    dude.rotation_euler = (vect[0], vect[1], vect[2])
    dude.keyframe_insert(data_path="rotation_euler", frame=hn * len(allPoints))
    for num in range(0, len(allPoints)):
        light.location = allPoints[num] * light_distance
        light.keyframe_insert(data_path="location", frame=num + hn * len(allPoints))
        OutPut_ImageNames += (rotationNames[num])

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = len(allPoints) * len(all_obj_rots)

# ЭТА ШТУКА ДЛЯ NORMAL MAP и MASK и ALBEDO

for hn in range(0, len(all_obj_rots)):
    vect = all_obj_rots[hn]
    dude.rotation_euler = (vect[0], vect[1], vect[2])
    dude.keyframe_insert(data_path="rotation_euler", frame=len(allPoints) * len(all_obj_rots) + hn)

fcurves = dude.animation_data.action.fcurves
for fcurve in fcurves:
    for kf in fcurve.keyframe_points:
        kf.interpolation = 'CONSTANT'



with open("D:\MyBlender\ImageGenFinished\ImageData.txt", "w") as file:
    file.write(OutPut_ImageNames)
with open("D:\MyBlender\ImageGenFinished\ImageAnswers.txt", "w") as file:
    file.write(OutPut_ImageAnswers)
