import json
from os import path, mkdir

def check_create(folder):
	if path.exists(folder): 
		print(f'Folder {folder} already exists.')
	else:
		mkdir(folder)
		print(f'Folder {folder} created!')

def format(content, formatter):
	if not formatter: return content
	if 'json': return json.dumps(content, indent=2)

def write_file(filename, content, formatter=None, folder=None):
	if folder: filename = folder + ('/' if folder[-1] != '/' else '') + filename
	with open(filename, 'w+') as f:
		content = format(content, formatter)
		f.write(content)
