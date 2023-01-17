
import os
from src.utils.file import read_dvc_params

dvc_params = read_dvc_params(__file__)
pipeline_params = dvc_params['environment-check']

env_name = pipeline_params['environment-name']
if env_name != os.environ.get('CONDA_DEFAULT_ENV'):
	raise RuntimeError(f'Environment not activated! (use `conda activate {env_name}`)')

from src.scripts import verify_gpu

from src.utils.output import write_file
verify_dict = verify_gpu.run()
write_file(pipeline_params['output'], verify_dict, 'json')

if not verify_dict['has_gpu']:
	raise RuntimeError("No GPU Available! Please recheck environment configuration/setup.")
