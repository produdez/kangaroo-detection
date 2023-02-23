import imgaug.augmenters as iaa


def load_augmenter(aug_config):
	if not aug_config['use']: 
		print(f"Not using augmenter: {aug_config['name']}")
		return None

	constructor = getattr(iaa, aug_config['name'])
	if aug_config.get('nested', False):
		if not aug_config.get('augmenters', False) or not aug_config.get('nested-arg', False):
			raise Exception("Nested augmentation config must include 'augmenters: <list>'")

		augmenters = []
		for config in aug_config['augmenters'].values():
			child_aug = load_augmenter(config)
			if child_aug: augmenters.append(child_aug)

		if not augmenters: return None

		aug_config['params'][aug_config['nested-arg']] = augmenters
	return constructor(**aug_config['params'])
