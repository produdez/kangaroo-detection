from src.utils.file import read_dvc_params
dvc_params = read_dvc_params(__file__)
pipeline_params = dvc_params['evaluate']

from src.scripts.dataset import load_train_val
train_set, val_set = load_train_val(pipeline_params['data'])

inference_params = dvc_params['inference']

from src.scripts.config import CustomConfig
config = CustomConfig(inference_params['configs'])
config.display()

from mrcnn.model import MaskRCNN
model = MaskRCNN(
	mode='inference', 
	model_dir= pipeline_params['evaluate_dir'], 
	config= config
)
model.load_weights(pipeline_params['model-weight'], by_name=True)

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

output_params = pipeline_params['output']
from src.utils.output import write_file
print(evaluation_result)
write_file(output_params['metric'], evaluation_result, 'json')
