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
	parents = []

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
		if name not in bears_dict:
			bears_dict[name] = words_stripped[1:]
		if name not in parents_dict:
			parents_dict[name] = words_stripped[2:4]

	file_text.close()

	for bear in bears_dict:
		mother = parents_dict[bear][0]
		father = parents_dict[bear][1]

		try:
			grandparents_dict[bear] = [parents_dict[mother][0], parents_dict[mother][1], parents_dict[father][0], parents_dict[father][1]]
		except:
			if father not in parents_dict and mother not in parents_dict:
				grandparents_dict[bear] = []
			elif mother not in parents_dict:
				grandparents_dict[bear] = [parents_dict[father][0],parents_dict[father][1]]
			elif father not in parents_dict:
				grandparents_dict[bear] = [parents_dict[mother][0],parents_dict[mother][1]]

		fam_dict[bear] = parents_dict[bear] + grandparents_dict[bear]

	for bear in bears_dict:
		if (bears_dict[bear][3] > 60 or bears_dict[bear][3] < 20):
			continue
		elif bears_dict[bear][0] == 'm':
			male_bears.append(bear)
		elif bears_dict[bear][0] == 'f':
			female_bears.append(bear)

	pairs = list(product(female_bears, male_bears))

	[parents.append(parent[0]) for parent in parents_dict.values()]
	[parents.append(parent[1]) for parent in parents_dict.values()]

	for i in range(6):
		for pair in pairs[:]:
			if pair[0] in parents or pair[1] in parents:
				pairs.remove(pair)
			elif abs(bears_dict[pair[0]][3] - bears_dict[pair[1]][3]) > 10:
				pairs.remove(pair)
			elif len(fam_dict[pair[0]]) >= 4 and len(fam_dict[pair[1]]) >= 4:
				if fam_dict[pair[0]][i] in fam_dict[pair[1]]:
					pairs.remove(pair)

	return pairs



