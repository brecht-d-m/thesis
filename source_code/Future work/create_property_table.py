from tqdm import tqdm
import csv
import copy

input_filename = "watdiv.500k.csv"
output_filename = "watdiv.500k.out.csv"

predicates = set(["subject"])
triples = {}

test_triple = ""

print()
print("Reading triples:")
print("----------------")
with open(input_filename, "rt") as csvfile:
	triples_reader = csv.reader(csvfile, delimiter=",")
	for row in tqdm(triples_reader):
		# Check if predicate is uri
		if row[1][0] == "<" and row[1][-1] == ">": 
			predicates.add(row[1])
		
		if row[0] in triples:
			if row[1] in triples[row[0]]:
				triples[row[0]][row[1]].append(row[2])
			else:
				triples[row[0]][row[1]] = [row[2]]
		else:	
			triples[row[0]]={}
			triples[row[0]][row[1]] = [row[2]]
		
		test_triple = row[0]

temp_triple_table = []

# Backtracking algo to expand triple
def expand_triple(subject, triple):
	temp_triple_table = [] # Re-initialize
	
	temp_triple = {}
	temp_triple["subject"]=subject
	
	_expand_triple(triple, copy.deepcopy(triple), temp_triple)
	return temp_triple_table

def _expand_triple(triple, predicate_list, temp_triple):
	if len(predicate_list) is not 0:
		pred, val = predicate_list.popitem()
		for predicate_subject in val:
			temp_triple[pred]=predicate_subject
			_expand_triple(triple, predicate_list, temp_triple)
	else:
		temp_triple_table.append(temp_triple)
		return

# Expand triples table
print()
print("Parsing tables:")
print("---------------")
for triple in tqdm(triples):
	print(triple)
	temp_triple_table += expand_triple(triple, triples[triple])

print()
print("Predicates:")
print("-----------")
print(predicates)

print()
print("Parsed triple:")
print("--------------")
print(triples[test_triple])

print()
print("Wrting to csv:")
print("--------------")

with open(output_filename, 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=predicates)
	writer.writeheader()

	for triple in tqdm(temp_triple_table):
    		writer.writerow(triple)
