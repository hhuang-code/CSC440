import csv
import re
import sys

def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+?')
    result = pattern.match(string)
    if result:
        return True
    else:
        return False

def groupby(filepath = 'iris.data', label = 'class'):

    # Load dataset
    with open(filepath, 'rb') as src_data:
        reader = csv.reader(src_data)
        imatrix = list(reader)
    src_data.close()

    # Dimensions
    sample_num = len(imatrix)
    feature_num = []
    if sample_num != 0:
        col = len(imatrix[0])
        for i in xrange(col):
            if is_number(imatrix[0][i]):
                feature_num.append(i)

    # Add Titles
    titles = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    
    # Find index of group column
    try:
        group_index = titles.index(label)
    except ValueError:
        print 'No such label in dataset.'
        return   
 
    # Group by
    dictionary = {}
    found = False
    for i in xrange(sample_num):
        found = False
        record = imatrix[i]
        label = record[group_index]
        for key in sorted(dictionary.keys()):
            if str(label) == key:
                found = True
                dictionary[key].append(record)
                break;
        if found == False:
            dictionary[str(label)] = []
            dictionary[str(label)].append(record)
 
    # Summary
    print
    print '=========GROUP BY=========='
    print titles[group_index], 'count'.rjust(20)
    for key in sorted(dictionary.keys()):
        print key.ljust(20), str(len(dictionary[key])).rjust(5)
    print

def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        in_label = ''
        if len(sys.argv) == 1:
            in_label = 'class'
        elif len(sys.argv) == 2:
            in_label = (sys.argv)[1]
        else:
            print 'Too many arguments! Please retry.'
        groupby(label = in_label)
    except:
        print >>sys.stderr
        return 1

if __name__ == '__main__':
    sys.exit(main())

