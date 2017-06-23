import string, itertools, sys, random

filename = sys.argv[1]
order = list(itertools.repeat(list(string.ascii_lowercase), 10))
flattened_order = [y for x in order for y in x]
file = open(filename, 'w')
random.shuffle(flattened_order)
shuffled = ",".join(flattened_order)
file.write(shuffled)
sys.stdout.write(shuffled)