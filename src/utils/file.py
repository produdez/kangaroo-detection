import os
from pprint import pprint
def get_pipeline_name(file, replace_underscore=True):
	module_name = os.path.splitext(os.path.basename(file))[0]
	return module_name if not replace_underscore else module_name.replace('_', '-')

from dvc.api import params_show
from src.utils.file import get_pipeline_name

def read_dvc_params(file, verbose=True):
	pipeline_name = get_pipeline_name(file)
	dvc_params = params_show(stages=pipeline_name)

	if verbose:
		print('Pipeline parameters: ')
		pprint(dvc_params)
	return dvc_params
