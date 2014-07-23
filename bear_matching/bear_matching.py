import re
from itertools import product

def matching_bears(filename):
	try:
		file_text = open(filename, 'r')
	except:
		print "File does not exist."
		exit()

	bears_dict = {}
	parents_dict = {}
	grandparents_dict = {}
	fam_dict = {}
	male_bears = []
	female_bears = []

	for line in file_text:
		line = line.rstrip()
		words = line.split(':')
		words_stripped = []
		for word in words:
			word = re.sub(r'\s+',' ', word)
			words_stripped.append((word.strip()).lower())
		name = words_stripped[0].lower()
		words_stripped[4] = float(words_stripped[4])
		words_stripped[4] = int(10 * words_stripped[4])
		if name not in bears_dict.keys():
			bears_dict[name] = words_stripped[1:]
		if name not in parents_dict.keys():
			parents_dict[name] = words_stripped[2:4]

	for bear in bears_dict:
		mother = parents_dict[bear][0]
		father = parents_dict[bear][1]
		
		if bears_dict[bear][0] == 'm':
			male_bears.append(bear)
		elif bears_dict[bear][0] == 'f':
			female_bears.append(bear)

		try:
			grandparents_dict[bear] = [parents_dict[mother][0], parents_dict[mother][1], parents_dict[father][0], parents_dict[father][1]]
		except:
			if father not in parents_dict.keys() and mother not in parents_dict.keys():
				grandparents_dict[bear] = ['nil','nil','nil','nil']
			elif mother not in parents_dict.keys():
				grandparents_dict[bear] = ['nil','nil',parents_dict[father][0],parents_dict[father][1]]
			elif father not in parents_dict.keys():
				grandparents_dict[bear] = [parents_dict[mother][0],parents_dict[mother][1],'nil','nil']

	file_text.close()

	for bear in parents_dict:
		fam_dict[bear] = parents_dict[bear] + grandparents_dict[bear]

	gender_combinations = list(product(female_bears, male_bears))

	for pair in gender_combinations[:]:
		if abs(bears_dict[pair[0]][3] - bears_dict[pair[1]][3]) > 10 or (bears_dict[pair[0]][3] > 60 or bears_dict[pair[1]][3] > 60) or (bears_dict[pair[0]][3] < 20 or bears_dict[pair[1]][3] < 20):
			gender_combinations.remove(pair)

	for bear in bears_dict:
		for pair in gender_combinations[:]:
			if pair[0] in bears_dict[bear] or pair[1] in bears_dict[bear]:
				gender_combinations.remove(pair)

	for pair in gender_combinations[:]:
		if parents_dict[pair[0]] != ['nil','nil'] or parents_dict[pair[1]] != ['nil','nil']:
			if (parents_dict[pair[0]][1] == parents_dict[pair[1]][1]) or parents_dict[pair[0]][1] == parents_dict[pair[1]][1]:
				gender_combinations.remove(pair)

	for i in range(6):
		for pair in gender_combinations[:]:
			if fam_dict[pair[0]] != 6*['nil']:
				if fam_dict[pair[0]][i] in fam_dict[pair[1]]:
					gender_combinations.remove(pair)
						
	return gender_combinations
    