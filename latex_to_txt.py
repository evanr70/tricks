def get_file(fn):
	try:
		with open(fn, 'r') as f:
			data = f.read()
	except FileNotFoundError:
		print('File "{}" was not found'.format(fn))
	return data

def get_input(text):
	start = text.find('\\input{')
	end = start + text[start:].find('}')
	return start, end

main = get_file('main.tex')

while main.find('\\input{') > -1:
	s, e = get_input(main)
	next_file = get_file(main[s+7:e])
	main = main.replace(main[s:e+1], next_file)

print("file name for output:")
output_name = input('> ')
with open(output_name, "w") as f:
	f.write(main)

