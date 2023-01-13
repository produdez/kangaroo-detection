
import os
from src.utils.arguments import setup_args

args = setup_args({
	'env_name' : 'Name of python virtual environment',
	'output' : 'Output file'
})

env_name = args.get('env_name')
if env_name != os.environ.get('CONDA_DEFAULT_ENV'):
	raise RuntimeError(f'Environment not activated! (use `conda activate {env_name}`)')

from src.scripts import verify_gpu

from src.utils.output import write_file
verify_dict = verify_gpu.run()
write_file(args['output'], verify_dict, 'json')

if not verify_dict['has_gpu']:
	raise RuntimeError("No GPU Available! Please recheck environment configuration/setup.")
