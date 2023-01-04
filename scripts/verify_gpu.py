import tensorflow as tf
from pprint import pprint
from tensorflow.python.client import device_lib

def run():
    print('TF Version: ', tf.__version__)
    print('------Devices------')
    pprint(device_lib.list_local_devices())
    print('--------------------------------')
    gpu_count = len(tf.config.experimental.list_physical_devices('GPU'))
    has_gpu = gpu_count > 0
    print("Num GPUs Available: ", gpu_count)
    print('Has gpu: ', has_gpu)
    pprint(tf.config.experimental.list_physical_devices('GPU'))
    return has_gpu
