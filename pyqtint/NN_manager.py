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

NORMAL_MODEL = tf.keras.models.load_model("ImageGen\TrainedModels\CubeConvTransDropoutMSENormals001.keras")

NORMAL_MODEL.summary()

my_dataset = np.random.random((1, 64,64,3))

result = NORMAL_MODEL.predict(my_dataset)
print(result.shape)
