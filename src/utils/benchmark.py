import time

import time

def bench(name, function, *args, **kwargs):
	start = time.time()
	result = function(*args, **kwargs)
	end = time.time()
	minutes = round((end - start) / 60, 2)
	print(f'{name} took {minutes} minutes')
	return {
		'time' : minutes,
		'unit' : 'minute',
		'result' : result,
	}
