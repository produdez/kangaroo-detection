import argparse
from pprint import pprint
def setup_args(dictionary):
	parser=argparse.ArgumentParser()
	for name, description in dictionary.items():
		parser.add_argument('--'+name, help=description)

	arguments = vars(parser.parse_args())
	print('File arguments:')
	pprint(arguments)
	return arguments
