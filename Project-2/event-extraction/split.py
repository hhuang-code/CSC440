import pdb
import operator

"""
ollie format: conf: (subject; relation; object)
"""

filename = 'result.txt'
# key is relation tuple, value is confidence
rel_dict = {}
with open(filename, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        
        # get confidence and relation tuple
        conf, rel = line.split(':')

        # convert confidence from string to float
        conf = float(conf.strip())

        # split subject, relation, and object
        rel = rel.strip()[1 : -1].split(';')

        # trim leading and tailing whitespace
        rel = [elem.strip() for elem in rel]

        # add to dict
        rel_dict[tuple(rel)] = conf
f.close

# sort dict by value (conf) and return a list
rel_sorted = sorted(rel_dict.items(), key = operator.itemgetter(1))

print(rel_sorted)


