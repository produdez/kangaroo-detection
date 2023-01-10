import argparse

def setup_args(dictionary):
	parser=argparse.ArgumentParser()
	for name, description in dictionary.items():
		parser.add_argument('--'+name, help=description)

	return vars(parser.parse_args())
