from src.utils.arguments import setup_args
args = setup_args({
	'data_path' : 'Path of training data to load',
	'model_src' : 'Model\'s source code directory',
	'model_config' : 'Model\'s configuration file',
	'training_dir' : 'Training directory to save training checkpoints/logs !',
	'summary' : 'Summary file path',
	'model_output' : 'Where to save finished training weights',
	'metric' : 'Training time saved in json'
})

import sys
sys.path.append(args['model_src'])

from src.scripts.dataset import load_train_val
train_set, val_set = load_train_val(args['data_path'])


from src.scripts.config import CustomConfig
from src.utils.config import load_config
config_dict = load_config(args['model_config'])['train']
config = CustomConfig(config_dict['model-config'])
config.display()


from mrcnn.model import MaskRCNN
model = MaskRCNN(mode='training', model_dir=args['training_dir'], config=config)
weight_config = config_dict['weights']
model.load_weights(
	weight_config['init'], 
	by_name=True,
	exclude=weight_config['exclude']
)

with open(args['summary'], 'w+') as f:
	model.keras_model.summary(print_fn=lambda x: f.write(x + '\n'))

from src.utils.benchmark import bench

training_benchmark = bench(
	'Training', model.train,
	train_set, val_set, 
	learning_rate = config.LEARNING_RATE, 
	epochs=config_dict['epochs'], 
	layers = config_dict['layers']
)

model.keras_model.save_weights(args['model_output'])

from src.utils.output import write_file
metrics = {
	'train_time': training_benchmark['time']
}
write_file(args['metric'], metrics, 'json')

