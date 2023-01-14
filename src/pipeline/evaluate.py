from src.utils.arguments import setup_args

args = setup_args({
	'data_path' : 'Path of training data to load',
	'train_size' : 'Path of training data to load',
	'model_src' : 'Model\'s source code directory',
	'model_weight': 'Model weight to load',
	'model_config' : 'Model\'s configuration file',
	'evaluate_dir' : 'Save inference checkpoints, ...',
	'metric' : 'Output metrics file'
})

import sys
sys.path.append(args['model_src'])

from src.scripts.dataset import load_train_val
train_set, val_set = load_train_val({
	'path' : args['data_path'],
	'train_size' : int(args['train_size'])
})

from src.utils.config import load_config
from src.scripts.config import CustomConfig
config_dict = load_config(args['model_config'])
model_config = config_dict['train']['model-config']
model_config.update(config_dict['test']['override-model-configs'])
config = CustomConfig(model_config)
config.display()

from mrcnn.model import MaskRCNN
model = MaskRCNN(mode='inference', model_dir= args['evaluate_dir'], config= config)
model.load_weights(args['model_weight'], by_name=True)

from src.scripts.evaluate import evaluate_model
from src.utils.benchmark import bench

evaluation_result = {}
for name, test_set in [('train', train_set), ('validation', val_set)]:
	benchmark_result = bench(
		f'Inference on {name} set',
		evaluate_model,
		val_set, model, config
	)

	evaluation_result[f'{name}_set'] = {
			'inference_time' : benchmark_result['time'],
			'mAP' : benchmark_result['result']
	}

from src.utils.output import write_file
print(evaluation_result)
write_file(args['metric'], evaluation_result, 'json')
