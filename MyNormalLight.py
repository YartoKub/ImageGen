import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image

def light3Dsingular(normal_px, albedo_px, light_point, x, y, depth, 
                    specular_color = 0,      ambient_color = 0, 
                    reflection_factor = 4,   light_strength = 1,):
    axis_center = np.array([0.5,0.5,0.5]); # Центр объекта в blender находится на 0,0,0, но здесь координаты от 0 до 1, поэтому я смещаю.
    camera_pos = np.array([0.5,0.5,2]);
    camera_pos = camera_pos - axis_center
    #axis_center = np.array([0,0,0]);
    x = x / 64; y = y / 64; depth; # Все должнры нормализоваться до 0-1
    specular_color = np.array([specular_color,specular_color,specular_color]); 
    ambient_color = np.array([ambient_color,ambient_color, ambient_color]);
    pixel_pos = np.array([x,y,depth[0]]) - axis_center # смещение относительно axis_center. Также вокруг центра вращается источник освещения
    
    l_d = light_point - pixel_pos
    v_len = np.linalg.norm(l_d)
    lightdir_norm  = np.array([l_d[0] / v_len, l_d[1] / v_len, l_d[2] / v_len])
    #color = ambient + strength * diffuse * max([0,0,0], dot(normal, light_dir))
    #print(l_d, lightdir_norm, v_len)
    v_len = v_len if v_len > 0.001 else 0.001
    diffuse_light = max(0,  np.dot(normal_px, lightdir_norm)) / v_len

    cemera_vector = camera_pos - pixel_pos
    camvec_norm  = (cemera_vector / np.linalg.norm(cemera_vector))
    reflection_vector = (2 * (np.dot(normal_px, lightdir_norm))) * normal_px - lightdir_norm
    specular_light = max(0,  np.dot(reflection_vector, camvec_norm)) ** reflection_factor
    
    #print(diffuse_light)
    #color = ambient_light + diffuse_light + spceular_light
    color =(ambient_color * albedo_px  
            + albedo_px * light_strength * diffuse_light
            + specular_color * specular_light
           )
    color = (min(1, color[0]), min(1, color[1]), min(1, color[2]))
    
    return color

def linear3DLight(normal, albedo, depth, vector, specular_color = 0.4, ambient_color = 0, reflection_factor = 5, light_strength = 1):
    neo_vector = np.array([vector[0], vector[1], vector[2]])
    local_normal = (normal - 0.5) * 2
    new_photo = np.zeros((64,64,3))
    for x in range(64):
        for y in range(64):
            new_color =  light3Dsingular(local_normal[x,y], albedo[x,y], 
                   neo_vector, 
                    x, y, depth[x, y],
                    specular_color = specular_color,
                    ambient_color = ambient_color,
                    reflection_factor = reflection_factor,
                    light_strength = light_strength
                   )
    
            new_photo[x,y] = new_color
    return new_photo

def light3Dspecular(normal_px, light_point, x, y, depth, 
                    light_strength = 1, 
                    specular_color = 0, reflection_factor = 4  ):
    axis_center = np.array([0.5,0.5,0.5]); # Центр объекта в blender находится на 0,0,0, но здесь координаты от 0 до 1, поэтому я смещаю.
    camera_pos = np.array([0.5,0.5,2]);
    camera_pos = camera_pos - axis_center
    #axis_center = np.array([0,0,0]);
    x = x / 64; y = y / 64; depth; # Все должнры нормализоваться до 0-1
    specular_color = np.array([specular_color,specular_color,specular_color]); 

    pixel_pos = np.array([x,y,depth[0]]) - axis_center # смещение относительно axis_center. Также вокруг центра вращается источник освещения

    l_d = light_point - pixel_pos
    v_len = np.linalg.norm(l_d)
    v_len = v_len if v_len > 0.001 else 0.001
    lightdir_norm  = np.array([l_d[0] / v_len, l_d[1] / v_len, l_d[2] / v_len])

    
    is_visible = np.dot(normal_px, lightdir_norm)
    specular_light = 0
    
    if is_visible > 0:
        cemera_vector = camera_pos - pixel_pos
        camvec_norm  = (cemera_vector / np.linalg.norm(cemera_vector))
        reflection_vector = (2 * (np.dot(normal_px, lightdir_norm))) * normal_px - lightdir_norm
        specular_light = max(0,  np.dot(reflection_vector, camvec_norm)) ** reflection_factor / v_len 
    

    color = specular_color * specular_light
    color = (min(1, color[0]), min(1, color[1]), min(1, color[2]))
    
    return color

def light3Ddiffuse(normal_px, light_point, 
                       x, y, depth, 
                       light_strength = 1, value1 =0, value2=0, value3=0):
    axis_center = np.array([0.5,0.5,0.5]); # Центр объекта в blender находится на 0,0,0, но здесь координаты от 0 до 1, поэтому я смещаю.
    x = x / 64; y = y / 64; depth; # Все должнры нормализоваться до 0-1
    pixel_pos = np.array([x,y,depth[0]]) - axis_center # смещение относительно axis_center. Также вокруг центра вращается источник освещения

    l_d = light_point - pixel_pos
    v_len = np.linalg.norm(l_d)
    lightdir_norm  = np.array([l_d[0] / v_len, l_d[1] / v_len, l_d[2] / v_len])
    #color = ambient + strength * diffuse * max([0,0,0], dot(normal, light_dir))
    #print(l_d, lightdir_norm, v_len)
    v_len = v_len if v_len > 0.001 else 0.001
    color = max(0,  np.dot(normal_px, lightdir_norm) * light_strength) / v_len 

    color = (min(1, color), min(1, color), min(1, color))
    
    return color

def soloDiffuse(normal, depth, light_point, light_strength):
    newNorm = normal * 2 - 1
    bigx, bigy, z = normal.shape
    light_point = np.array([-light_point[1], light_point[0], light_point[2]])
    if z != 3: return False
    to_return = np.zeros((bigx,bigy,z))
    for x in range(bigx):
        for y in range (bigy):
            to_return[x, y] = light3Ddiffuse(newNorm[x, y], light_point, x, y, depth[x, y],  light_strength)
    return to_return

def soloSpecular(normal, depth, light_point, light_strength, specular_color = 0.3, reflection_factor = 4):
    newNorm = normal * 2 - 1
    bigx, bigy, z = normal.shape
    light_point = np.array([-light_point[1], light_point[0], light_point[2]])
    if z != 3: return False
    to_return = np.zeros((bigx,bigy,z))
    for x in range(bigx):
        for y in range (bigy):
            to_return[x, y] = light3Dspecular(newNorm[x, y], light_point, x, y, depth[x, y],  light_strength, specular_color, reflection_factor)
    return to_return