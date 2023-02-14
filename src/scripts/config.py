from mrcnn.config import Config
from pprint import pprint

class CustomConfig(Config):
	def get_config(self):
			return self.to_dict()
	
	def __init__(self, model_cfg, verbose=True):
		if verbose:
			print('Model config: ')
			pprint(model_cfg)
		for key,v in model_cfg.items():
			self.__setattr__(key, v)
		super().__init__()
