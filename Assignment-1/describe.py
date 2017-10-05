import csv
import re
import math

def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+?')
    result = pattern.match(string)
    if result:
        return True
    else:
        return False

def describe(filepath = "iris.data"):
    
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
    
    # Count
    count = []
    for i in feature_num:
        cnt = 0
        for j in xrange(sample_num):
            if not imatrix[j][i] is None:
                cnt += 1
        count.append(cnt)

    # Mean
    mean = []
    for i in feature_num:
        sum = 0.0
        for j in xrange(sample_num):
            sum += float(imatrix[j][i])
        mean.append(sum / sample_num)

    # Standard deviation
    std = []
    for i in feature_num:
        sum = 0.0
        for j in xrange(sample_num):
            sum += pow(float(imatrix[j][i]) - mean[i], 2)
        std.append(math.sqrt(sum / (sample_num - 1)))

    # Minimum
    minimum = []
    for i in feature_num:
        min = float(imatrix[0][i])
        for j in xrange(sample_num):
            if min > float(imatrix[j][i]):
                min = float(imatrix[j][i])
        minimum.append(min)

    # First quartile
    fquartile = []
    for i in feature_num:
        tmp_list = []
        for j in xrange(sample_num):
            tmp_list.append(float(imatrix[j][i]))
        tmp_list = sorted(tmp_list)
        fquartile.append(tmp_list[int(math.ceil(sample_num / 4.0))])

    # Median
    median = []
    for i in feature_num:
        tmp_list = []
        for j in xrange(sample_num):
            tmp_list.append(float(imatrix[j][i]))
        tmp_list = sorted(tmp_list)
        median.append((tmp_list[int(math.ceil(sample_num / 2.0))] + tmp_list[int(math.ceil(sample_num / 2.0)) + 1]) / 2.0)

    # Third quartile
    tquartile = []
    for i in feature_num:
        tmp_list = []
        for j in xrange(sample_num):
            tmp_list.append(float(imatrix[j][i]))
        tmp_list = sorted(tmp_list)
        tquartile.append(tmp_list[int(math.ceil(3.0 * sample_num / 4.0))])

    # Maximum
    maximum = []
    for i in feature_num:
        max = float(imatrix[0][i])
        for j in xrange(sample_num):
            if max < float(imatrix[j][i]):
                max = float(imatrix[j][i])
        maximum.append(max)

    # Summary
    print "sepal-length".rjust(23), "sepal-width".rjust(15), "petal-length".rjust(15), "petal-width".rjust(15)
    print "count".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(count[i]).rjust(15),
    print
    
    print "mean".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(mean[i]).rjust(15),
    print
 
    print "std".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(std[i]).rjust(15),
    print

    print "min".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(minimum[i]).rjust(15),
    print

    print "25%".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(fquartile[i]).rjust(15),
    print

    print "median".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(fquartile[i]).rjust(15),
    print
    
    print "75%".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(tquartile[i]).rjust(15),
    print
    
    print "max".ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(maximum[i]).rjust(15),
    print

