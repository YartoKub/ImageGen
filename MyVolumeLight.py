# THIS PIECE OF CODE IS COPIED FROM VolumeLight
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image

def distance_point_to_line(A, B, C, x0, y0):
    distance = abs(A * x0 + B * y0 + C) / math.sqrt(A**2 + B**2)
    return distance
    
def vector_line(x0, y0, x1, y1):
    A = y1 - y0
    B = x0 - x1
    C = x1 * y0 - x0 * y1
    return A, B, C

def perpendicular_from_point_to_line(A, B, C, x0, y0):
    if A == 0: 
        x_perpendicular = x0
        y_perpendicular = -C / B
    elif B == 0: 
        x_perpendicular = -C / A
        y_perpendicular = y0
    else:
        m_perpendicular = B / A
        x_perpendicular = (-B * y0 + B * m_perpendicular * x0 - C) / (A + B * m_perpendicular)
        y_perpendicular = m_perpendicular * (x_perpendicular - x0) + y0
    return x_perpendicular, y_perpendicular

def clamp(n, my_min, my_max): 
    if n < my_min: 
        return my_min
    elif n > my_max: 
        return my_max
    else: 
        return n 

def ratio_perp(x0, y0, x1, y1, # line points
              a0, a1): # actual point
    A, B, C = vector_line(x0, y0, x1, y1)
    distance = distance_point_to_line(A, B, C, a0, a1)
    px, py = perpendicular_from_point_to_line(A, B, C, a0, a1)
    ratio = 10
    if abs((x1 - x0)) > 0.001:
        ratio = (px - x0) / (x1 - x0)
    elif abs((y1 - y0)) > 0.001:
        ratio = (py - y0) / (y1 - y0)
    return ratio, distance

def XYZ_to_world(x, y, z):
    return x / 64 - 0.5, y / 64 - 0.5, z - 0.5
def Light_to_grid(light_pos):
    x, y, z = light_pos # Z не нужен
    x = x + 0.5; y = y + 0.5;
    x = x * 64; y = y * 64
    x = round(x); y = round(y)
    return x, y

def try_paint(x, y):
    if x < 0 or y < 0: return False
    if x > 63 or y > 63: return False
    return True

# Хороший вариант честно спизженный отсюда:
# https://github.com/mitchcurtis/grid-line-intersection/blob/master/main.cpp
# Вариант очень хороший, я немного модифицировал его так чтобы он закрашивал клетки даже когда пересекается с углом.
# Но наверное это ролять не будет. Но все равно. 
# Его проблема в том что он принимает только integer значения
def rayCast(x0, y0, x1, y1, avoid_exorbants = False): 
    candidates = []

    dx = abs(x1 - x0);
    dy = abs(y1 - y0);
    x = x0;
    y = y0;
    n = 1 + dx + dy;
    x_inc = 1 if x1 > x0 else -1
    y_inc = 1 if y1 > y0 else -1
    error = dx - dy;
    dx *= 2;
    dy *= 2;
    while n > 0:
        n = n - 1
        if try_paint(x, y):
            candidates.append((x, y))
        if (error > 0):
            x += x_inc;
            error -= dy;
        elif (error < 0):
            y += y_inc;
            error += dx;
        elif (error == 0) :
            if avoid_exorbants == False:
                if try_paint(x + x_inc, y):
                    candidates.append((x, y))
                if try_paint(x, y + y_inc):
                    candidates.append((x, y))
            x += x_inc;
            y += y_inc;
            error -= dy;
            error += dx;
            n = n - 1;

    return candidates

def volume_shadow(depth_map, light_pos, treshhold, column_fat, column_sub_scat = 0.001):
    print("FRAME GEN BEGUN...")
    loc_depth_map = depth_map[:,:, 0]
    new_photo = np.zeros((64,64,3))
    new_light_pos = [-light_pos[1], light_pos[0], light_pos[2]]
    l_x, l_y = Light_to_grid(new_light_pos)
    l_z = new_light_pos[2]
    for x in range(0,64, 1): # ПОМЕНЯТЬ!
        for y in range(0, 64, 1):
            new_color = can_reach_pixel(loc_depth_map, (l_x, l_y, l_z), x, y, treshhold, column_fat, column_sub_scat)
            new_photo[x,y] = [new_color,new_color,new_color]
    print("FRAME GEN FINISHED!")
    return new_photo

def can_reach_pixel(depth_map, light_pos, x, y, treshhold, column_fat, column_sub_scat = 0.001):
    reverse_css = 1 / column_sub_scat
    new_x, new_y, z = light_pos[0], light_pos[1], light_pos[2]
    illumination = 1
    point_list = rayCast(new_x, new_y, x, y, False)
    debug_info = ""
    #print("=" * 10, "START " + str(z) + " END " + str(depth_map[x, y]), "=" * 10)
    for point in point_list:
        ratio, distance = ratio_perp(new_x, new_y, x, y, point[0], point[1])
        #print(new_x, new_y, x, y, point[0], point[1], "R&D:", ratio, distance)
        
        if try_paint(point[0], point[1]):
            light_height = z - (z - depth_map[x, y]) * ratio
            h_diff = depth_map[point[0], point[1]] - light_height
            #debug_info = (debug_info + "L:" + str(round(illumination, 2)) +  "LH" + str(round(light_height, 2)))
            if  h_diff > treshhold: 
                if illumination < 0.01:
                    illumination = 0
                    break
                neomod = clamp(column_sub_scat - h_diff, 0, column_sub_scat)  * reverse_css
                illumination = illumination * neomod
                #illumination = illumination * clamp(distance * 2 - column_fat, 0, 1)
                #print("LH", round(light_height, 4), "DM", round(depth_map[point[0], point[1]], 4), "HD", round(h_diff, 4), "NM", round(neomod,4))
                """
                debug_info +=(  "D: " + str(round(distance, 2)) + 
                                "H_diff" + str(round(h_diff, 4)) +
                                " neomod " + str(round(neomod, 4)) +
                                "Coord: " + str((round(point[0], 3), round(point[1], 3))) +  
                                "DM: " + str(round(depth_map[point[0], point[1]], 3)) + 
                                " LH: " + str(round(light_height, 3))
                             )  
                """
                
    #if illumination  < 0.8: print(debug_info)
    return illumination
    