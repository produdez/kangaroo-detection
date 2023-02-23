from src.utils.file import read_dvc_params
dvc_params = read_dvc_params(__file__)
pipeline_params = dvc_params['train-pipeline']

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

from src.utils.output import write_file, check_create
general_metrics = {
	'train_time': training_benchmark['time']
}

metric_output_folder = output_params['metric']['folder']
check_create(metric_output_folder)
write_file(output_params['metric']['general'], general_metrics, formatter='json', folder=metric_output_folder)

# Get other training metrics wrote in the log folder (TensorBoard)
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
event_acc = EventAccumulator(model.log_dir)
event_acc.Reload()

keys = ['timestamp', 'iteration', 'value']
# ! we actually only care about bounding box loss for this project
other_metrics = output_params['metric']['others']
for metric_name in other_metrics:
	metric = {
		metric_name: [
			dict(zip(keys ,values))
			for values in event_acc.Scalars(metric_name)
		]
	}
	write_file(metric_name + '.json', metric, 'json', metric_output_folder)




