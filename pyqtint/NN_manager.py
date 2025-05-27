import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
gpus = tf.config.experimental.list_physical_devices("GPU")
print(gpus)
import numpy as np
import math
import pandas
from matplotlib import pyplot as plt
from PIL import Image
import os
from RGBHSL import image_coverter,  pixel_hsl_to_rgb, pixel_rgb_to_hsl

# ===== ACCEPTABLE_SIZES =====
DEFAULT_INPUT_SIZE = (None, 64, 64, 3)
NORMAL_OUTPUT_SIZE = (None, 64, 64, 3)
DEPTH_OUTPUT_SIZE = (None, 64, 64)
COLOR_OUTPUT_HSL_SIZE = (None, 64, 64, 2) # Использует HSL, поэтомув сего два канала. Ииу также нужно преобразование перед загрузкой и после загрузки
COLOR_OUTPUT_RGB_SIZE = (None, 64, 64, 3) # Использует нормальный RGB

LIGHT_INPUT_SIZE = [(None, 64, 64, 3), (3,)]
LIGHT_OUTPUT_SIZE = (None, 64, 64, 3)

RGB_FORMAT = "RGB"
HSL_FORMAT = "HSL"

class NN_Manager():
    def __init__(self, parent):
        self.main_window = parent
        self.NORMAL_MODEL = None #tf.keras.models.load_model("ImageGen\TrainedModels\CubeConvTransDropoutMSENormals001.keras")
        self.COLOR_MODEL_FORMAT = "RGB"
        self.COLOR_MODEL = None
        self.DEPTH_MODEL = None
        self.LIGHT_MODEL = None

    def changeModel(self, map_name, model_adress):
        print("начинаю грузить модель в NN manager")
        if  map_name == "NORMAL":
            self.changeNormal(model_adress)
            return
        if  map_name == "COLOR" :
            self.changeColor (model_adress)
            return
        if  map_name == "DEPTH" :
            self.changeDepth (model_adress)
            return
        if  map_name == "LIGHT" :
            self.changeLight (model_adress)
            return
    
    def changeNormal(self, model_adress):
        loaded_model = tf.keras.models.load_model(model_adress)
        
        inputs = loaded_model.inputs  ; act_inputs = []; 
        for i, inp in enumerate(inputs):
            act_inputs .append(tuple(inp.shape))

        outputs = loaded_model.outputs; act_outputs = []
        for i, out in enumerate(outputs):
            act_outputs.append(tuple(out.shape))

        if len(act_inputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("NORMAL", False, f"Количество входных матриц равно {len(act_inputs)}, должна быть одна матрица")
            return 
        if act_inputs[0] != DEFAULT_INPUT_SIZE:
            self.modelUpdate("NORMAL", False, f"Не тот размер входной матрицы {act_inputs[0]}, правильно {DEFAULT_INPUT_SIZE}")
            return
        
        if len(act_outputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("NORMAL", False, f"Количество ВЫходных матриц равно {len(act_outputs)}, должна быть одна матрица")
            return 
        if act_outputs[0] != NORMAL_OUTPUT_SIZE: # если не 1, значит входных матриц две
            self.modelUpdate("NORMAL", False, f"Не тот размер ВЫходной матрицы {act_outputs[0]}, правильно {NORMAL_OUTPUT_SIZE}")
            return 
        self.NORMAL_MODEL = loaded_model
        self.modelUpdate("NORMAL", True, f"Успешная загрузка модели карты нормалей! ")
        return

    def changeDepth(self, model_adress):
        loaded_model = tf.keras.models.load_model(model_adress)    
        inputs = loaded_model.inputs  ; act_inputs = []; 
        for i, inp in enumerate(inputs):
            act_inputs .append(tuple(inp.shape))

        outputs = loaded_model.outputs; act_outputs = []
        for i, out in enumerate(outputs):
            act_outputs.append(tuple(out.shape))

        if len(act_inputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("DEPTH", False, f"Количество входных матриц равно {len(act_inputs)}, должна быть одна матрица")
            return 
        if act_inputs[0] != DEFAULT_INPUT_SIZE:
            self.modelUpdate("DEPTH", False, f"Не тот размер входной матрицы {act_inputs[0]}, правильно {DEFAULT_INPUT_SIZE}")
            return
        
        if len(act_outputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("DEPTH", False, f"Количество ВЫходных матриц равно {len(act_outputs)}, должна быть одна матрица")
            return 
        if act_outputs[0] != DEPTH_OUTPUT_SIZE: # если не 1, значит входных матриц две
            self.modelUpdate("DEPTH", False, f"Не тот размер ВЫходной матрицы {act_outputs[0]}, правильно {DEPTH_OUTPUT_SIZE}")
            return 
    
        self.DEPTH_MODEL = loaded_model
        self.modelUpdate("DEPTH", True, f"Успешная загрузка глубинной модели! ")
        return
        
    def changeColor(self, model_adress):
        loaded_model = tf.keras.models.load_model(model_adress)    
        inputs = loaded_model.inputs  ; act_inputs = []; 
        for i, inp in enumerate(inputs):
            act_inputs .append(tuple(inp.shape))

        outputs = loaded_model.outputs; act_outputs = []
        for i, out in enumerate(outputs):
            act_outputs.append(tuple(out.shape))

        if len(act_inputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("COLOR", False, f"Количество входных матриц равно {len(act_inputs)}, должна быть одна матрица")
            return 
        if act_inputs[0] != DEFAULT_INPUT_SIZE:
            self.modelUpdate("COLOR", False, f"Не тот размер входной матрицы {act_inputs[0]}, правильно {DEFAULT_INPUT_SIZE}")
            return
        
        if len(act_outputs) != 1: # если не 1, значит ВЫвходных матриц две
            self.modelUpdate("COLOR", False, f"Количество ВЫходных матриц равно {len(act_outputs)}, должна быть одна матрица")
            return 
        
        if act_outputs[0] == COLOR_OUTPUT_HSL_SIZE: # если не 1, значит входных матриц две
            self.COLOR_MODEL = loaded_model
            self.COLOR_MODEL_FORMAT = HSL_FORMAT
            self.modelUpdate("COLOR", True, f"Успешная загрузка модели! Режим: HSL")
            return 
        elif act_outputs[0] == COLOR_OUTPUT_RGB_SIZE: # если не 1, значит входных матриц две
            self.COLOR_MODEL = loaded_model
            self.COLOR_MODEL_FORMAT = RGB_FORMAT
            self.modelUpdate("COLOR", True, f"Успешная загрузка модели! Режим: RGB")
            return 
        else:
            self.modelUpdate("COLOR", False, f"Не тот размер ВЫходной матрицы {act_inputs[0]}, правильно {COLOR_OUTPUT_HSL_SIZE} или {COLOR_OUTPUT_RGB_SIZE}")
            return
        
    def changeLight(self, model_adress):
        loaded_model = tf.keras.models.load_model(model_adress)    
        inputs  = loaded_model.inputs ; act_inputs  = []; 
        for i, inp in enumerate(inputs):
            act_inputs .append(tuple(inp.shape))

        outputs = loaded_model.outputs; act_outputs = [];
        for i, out in enumerate(outputs):
            act_outputs.append(tuple(out.shape))

        if len(act_inputs) != 2: # На вход подается матрица с изображением и матрица с вектором
            self.modelUpdate("LIGHT", False, f"Количество входных матриц равно {len(act_inputs)}, должно быть две входных матрицы")
            return
        if act_inputs[0] != LIGHT_INPUT_SIZE[0]: 
            self.modelUpdate("LIGHT", False, f"Неправильный размер первой входной матрицы: {str(act_inputs[0])}, должно быть: {LIGHT_INPUT_SIZE[0]}")
            return
        if act_inputs[1] == LIGHT_INPUT_SIZE[1]:
            self.modelUpdate("LIGHT", False, f"Неправильный размер второй входной матрицы: {str(act_inputs[1])}, должно быть: {LIGHT_INPUT_SIZE[1]}")
            return
        if len(act_outputs) != 1: # если не 1, значит входных матриц две
            self.modelUpdate("LIGHT", False, f"Количество ВЫходных матриц равно {len(act_outputs)}")
            return 
        if act_outputs[0] != LIGHT_OUTPUT_SIZE: # если не 1, значит входных матриц две
            self.modelUpdate("LIGHT", False, f"Неправильный размер ВЫходной матрицы:  {str(act_outputs[0])}, должно быть: {LIGHT_OUTPUT_SIZE}")
            return 
        
        self.LIGHT_MODEL = loaded_model
        self.modelUpdate("LIGHT", True, f"Успешная загрузка световой модели! ")
        return
# ============================= SINGLE IMAGE PROCESSING ====================================
    def RenderSingleImage(self, map_name, input_image, input_vector = None):
        if  map_name == "NORMAL":
            if self.NORMAL_MODEL == None: return self.fillerImage(input_image)
            result = self.NORMAL_MODEL.predict(input_image.reshape((1, 64, 64, 3)))[0]
            return np.clip(result, 0, 1)
        
        if  map_name == "COLOR" :
            if self.COLOR_MODEL == None: return self.fillerImage(input_image)
            if self.COLOR_MODEL_FORMAT == RGB_FORMAT:
                result = input_image - self.COLOR_MODEL.predict(input_image.reshape((1, 64, 64, 3)))[0]
            if self.COLOR_MODEL_FORMAT == HSL_FORMAT:
                temp_hsl = image_coverter(input_image, pixel_rgb_to_hsl, True, True)
                result = self.COLOR_MODEL.predict(temp_hsl.reshape((1, 64, 64, 3))) 
                result = result[0] # тут только два своя: S и L
                result = np.stack([temp_hsl[:,:,0], temp_hsl[:,:,1] - result[:,:,0], temp_hsl[:,:,2] - result[:,:,1]], axis = 2)
                result = image_coverter(result, pixel_hsl_to_rgb, True, True)
            return np.clip(result, 0, 1)
        
        if  map_name == "DEPTH" :
            if self.DEPTH_MODEL == None: return self.fillerImage(input_image)
            result = self.DEPTH_MODEL.predict(input_image.reshape((1, 64, 64, 3)))[0]
            result = np.stack([result, result, result], axis=2)
            return np.clip(result, 0, 1)
        
        if  map_name == "LIGHT" and input_vector != None:
            if self.LIGHT_MODEL == None: return self.fillerImage(input_image)
            result = self.LIGHT_MODEL.predict(input_image.reshape((1, 64, 64, 3)), input_vector)[0]
            return result # Здесь нет clip т.к. свет может быть выше 1. Ограничение должно накладыватсья позднее
# ================ MULTIPLE IMAGE PROCESSING ======================================================
    def RenderMultipleImages(self, map_name, input_image_list, input_vector_list = None):
        if  map_name == "NORMAL":
            if self.NORMAL_MODEL == None: return self.fillerImage(input_image_list)
            result = self.NORMAL_MODEL.predict(input_image_list)
            return np.clip(result, 0, 1)
        
        if  map_name == "COLOR" :
            if self.COLOR_MODEL == None: return self.fillerImage(input_image_list)
            if self.COLOR_MODEL_FORMAT == RGB_FORMAT:
                result = input_image_list - self.COLOR_MODEL.predict(input_image_list)
                return np.clip(result, 0, 1)
            if self.COLOR_MODEL_FORMAT == HSL_FORMAT:
                #print("Inside HSL")
                new_array = np.zeros(input_image_list.shape)
                for i in range(input_image_list.shape[0]):
                    #print(f"image convering RGB -> HSL {i}")
                    new_array[i] = image_coverter(input_image_list[i], pixel_rgb_to_hsl, True, True)

                result = self.COLOR_MODEL.predict(new_array) 
                result = np.stack([new_array[:,:,:,0], new_array[:,:,:,1] - result[:,:,:,0], new_array[:,:,:,2] - result[:,:,:,1]], axis = 3)

                to_return = np.zeros(input_image_list.shape)
                for i in range(new_array.shape[0]):
                    #print(f"image convering HSL -> RGB {i}")
                    to_return[i] = image_coverter(result[i], pixel_hsl_to_rgb, True, True)

                result = to_return



                return np.clip(result, 0, 1)
        
        if map_name == "DEPTH" :
            if self.DEPTH_MODEL == None: return self.fillerImage(input_image_list)
            result = self.DEPTH_MODEL.predict(input_image_list)
            result = np.stack([result, result, result], axis=3)
            return np.clip(result, 0, 1)
        
        if  map_name == "LIGHT" and input_vector_list != None:
            if self.LIGHT_MODEL == None: return self.fillerImage(input_image_list)
            result = self.LIGHT_MODEL.predict(input_image_list, input_vector_list)
            return result # Здесь нет clip т.к. свет может быть выше 1. Ограничение должно накладыватсья позднее
    

    def fillerImage(self, map_name, input_image):
        return np.random.random(input_image.shape)


    def modelUpdate(self, model_map, status = False, reason_str = "провал"):
        self.main_window.modelUpdate(model_map, status, reason_str)
    
    def makeimage(self, result):
        result = (result[0] * 255).astype(np.uint8)
        image = Image.fromarray(result)
        image.save('output_image.png')

    
