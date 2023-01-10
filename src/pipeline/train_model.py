from src.utils.arguments import setup_args
from pprint import pprint
args = setup_args({
	'data_path' : 'Path of training data to load',
	'model_src' : 'Model\'s source code directory',
	'model_config' : 'Model\'s configuration file'
})
pprint(args)

import sys
sys.path.append(args.get('model_src'))
from src.scripts.dataset import KangarooDataset

data_path = args.get('data_path')
train_set = KangarooDataset()
train_set.load_data(data_path)
train_set.prepare()
val_set = KangarooDataset()
val_set.load_data(data_path, is_train=False)
val_set.prepare()
print(f'train-size: ', len(train_set.image_ids))
print(f'val-size: ', len(val_set.image_ids))


# import dvc.api as api

# params = api.params_show()
# print('PARAMS: ', params)
import yaml

# Function to load yaml configuration file
def load_config():
    with open(args.get('model_config')) as file:
        config = yaml.safe_load(file)

    return config
config = load_config()
print('Model config: ', config)
