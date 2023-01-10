
import os
from src.utils.arguments import setup_args

args = setup_args({
	'env_name' : 'Name of python virtual environment'
})

env_name = args.get('env_name')
if env_name != os.environ.get('CONDA_DEFAULT_ENV'):
	raise RuntimeError(f'Environment not activated! (use `conda activate {env_name}`)')

from src.scripts import verify_gpu
if not verify_gpu.run():
	raise RuntimeError("No GPU Available! Please recheck environment configuration/setup.")
