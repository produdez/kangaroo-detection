import json

def format(content, formatter):
	if not formatter: return content
	if 'json': return json.dumps(content, indent=2)

def write_file(filename, content, formatter=None):
	with open(filename, 'w+') as f:
		content = format(content, formatter)
		f.write(content)
