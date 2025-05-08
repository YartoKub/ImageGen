import numpy as np
import math
def pixel_rgb_to_hsl(my_pixel, normalized_input = False, normalize_output = False):
    if normalized_input == False:
        my_pixel = my_pixel / 255
    
    minval = np.min(my_pixel)
    brightest_channel = np.argmax(my_pixel)
    maxval = my_pixel[brightest_channel]
    delta = maxval - minval
    luminance = (minval + maxval) / 2
    
    bottom_saturation = (maxval + minval) if luminance <= 0.5 else (2.0 - delta)
    
    if delta == 0:
        return 0, 0, luminance 
        
    saturation = (delta) / bottom_saturation
    hue = 0
    if brightest_channel == 0:
        hue = (my_pixel[1] - my_pixel[2]) / delta
    elif brightest_channel == 1:
        hue = 2.0 + (my_pixel[2] - my_pixel[0]) / delta
    else: 
        hue =  4.0 + (my_pixel[0] - my_pixel[1]) / delta
    hue = hue * 60 + 360 if hue < 0 else hue * 60
    if normalize_output: hue = hue / 360
    return hue, saturation, luminance 
# Hue Saturation Luminance
def pixel_hsl_to_rgb(my_pixel, normalized_input = False, normalize_output = False):
    if  normalized_input == True:
        my_pixel = np.array([my_pixel[0] * 360, my_pixel[1], my_pixel[2]])
    hue        = my_pixel[0] #if my_pixel[0] != 360 else 0
    saturation = my_pixel[1]
    luminance  = my_pixel[2]

    H = hue / 60
    C = (1 - abs(luminance * 2 - 1)) * saturation
    X = C * (1 -   abs(H % 2 - 1)    )
    m = luminance - C / 2

    rgb = None
    if hue >= 0   and hue < 60 : rgb = (C, X, 0)
    if hue >= 60  and hue < 120: rgb = (X, C, 0)
    if hue >= 120 and hue < 180: rgb = (0, C, X)
    if hue >= 180 and hue < 240: rgb = (0, X, C)
    if hue >= 240 and hue < 300: rgb = (X, 0, C)
    if hue >= 300 and hue <= 360: rgb = (C, 0, X)

    to_return = np.array([rgb[0] + m, rgb[1] + m, rgb[2] + m])
    if normalize_output == False:
        to_return = np.round( to_return * 255, 0)
    
    return to_return

def image_coverter(myPicture, funcfunc,  normalized_input = False, normalize_output = False):
    bigx, bigy, z = myPicture.shape
    if z != 3: return False
    to_return = np.zeros((bigx,bigy,z))
    for x in range(bigx):
        for y in range (bigy):
            to_return[x, y] = funcfunc(myPicture[x,y], normalized_input, normalize_output)
    return to_return