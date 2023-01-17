from src.utils.file import read_dvc_params
dvc_params = read_dvc_params(__file__)
pipeline_params = dvc_params['train-pipeline']

import sys
model_src = dvc_params['src']['current-model']
sys.path.append(model_src)

from src.scripts.dataset import load_train_val
train_set, val_set = load_train_val(pipeline_params['data'])


training_params = dvc_params['train']

from src.scripts.config import CustomConfig
config = CustomConfig(training_params['configs'])
config.display()


from mrcnn.model import MaskRCNN
model = MaskRCNN(
	mode='training', 
	model_dir=pipeline_params['train_dir'], 
	config=config
)
weight_config = training_params['weights']
model.load_weights(
	weight_config['init'], 
	by_name=True,
	exclude=weight_config['exclude']
)

with open(pipeline_params['summary'], 'w+') as f:
	model.keras_model.summary(print_fn=lambda x: f.write(x + '\n'))

from src.utils.benchmark import bench

training_benchmark = bench(
	'Training', model.train,
	train_set, val_set, 
	learning_rate = config.LEARNING_RATE, 
	epochs = training_params['epochs'], 
	layers = training_params['layers']
)


output_params = pipeline_params['output']
model.keras_model.save_weights(output_params['model'])

from src.utils.output import write_file
metrics = {
	'train_time': training_benchmark['time']
}
write_file(output_params['metric'], metrics, 'json')

