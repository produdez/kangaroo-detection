import tensorflow as tf
from pprint import pprint
from tensorflow.python.client import device_lib

def run():
    print('TF Version: ', tf.__version__)
    print('------Devices------')
    devices_detail = device_lib.list_local_devices()
    print(devices_detail)
    print('--------------------------------')
    device_list = tf.config.experimental.list_physical_devices('GPU')
    gpu_count = len(device_list)
    has_gpu = gpu_count > 0
    print("Num GPUs Available: ", gpu_count)
    print('Has gpu: ', has_gpu)
    pprint(device_list)
    return {
        'has_gpu' : has_gpu,
        'gpu_count' : gpu_count,
        'devices' : [{
            'name' : device.name,
            'device_type' : device.device_type,
            'physical_device_desc' : device.physical_device_desc
        } for device in devices_detail],
    }

if __name__ == "__main__":
    run()
