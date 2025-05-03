import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image
import MyVolumeLight
import MyNormalLight

def single_frame_pipe(myNormal, myAlbedo, myDepth, myMask, one_light_direction, 
                        specular_color = 0.3, ambient_color = 0, 
                        reflection_factor = 5, light_strength = 4,
                        threshhold = 0.00001, column_fat = 0.05, sss = 0.25,
                        volume_normal_ratio = 0.2, mask_prominence = 1,
                        return_combined = True
                     ):
    my_volume = MyVolumeLight.volume_shadow(myDepth, one_light_direction, threshhold, column_fat, sss)
    my_normal_light = MyNormalLight.linear3DLight(  myNormal, myAlbedo, myDepth, one_light_direction, 
                                                    specular_color, ambient_color , 
                                                    reflection_factor, light_strength)
    if return_combined:
        my_normal_light = my_normal_light * (1 - mask_prominence) + my_normal_light * myMask * mask_prominence
        return my_normal_light * volume_normal_ratio + (myAlbedo * my_volume) * (1 - volume_normal_ratio)
    else:
        return my_volume, my_normal_light