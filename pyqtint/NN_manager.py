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


    def modelUpdate(self, model_map, status = False, reason_str = "провал"):
        self.main_window.modelUpdate(model_map, status, reason_str)
    
    def makeimage(self, result):
        result = (result[0] * 255).astype(np.uint8)
        image = Image.fromarray(result)
        image.save('output_image.png')
