import re
import math
import sys
import matplotlib
import matplotlib.pyplot as mpt

from random import uniform
from collections import defaultdict
from numpy import *

# Check if a string is a number
def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+?')
    result = pattern.match(string)
    if result:
        return True
    else:
        return False

# Calculate the distance between two vectors
def calc_dist(v1, v2):
    dims1 = len(v1)
    dims2 = len(v2)
    if dims1 != dims2:
        print 'Error in calc_dist()!'
        return
    else:
        dist = 0
        for i in xrange(dims1):
            dist += math.pow(v1[i] - v2[i], 2)
    return math.sqrt(dist)

# Calculate the average vector of a group of vectors
def avg_vector(vectors):
    dims = len(vectors[0])
    avg = []
    for i in xrange(dims):
        sum = 0
        for v in vectors:
            sum += v[i]
        avg.append(float('%.1f'%(sum / float(len(vectors)))))
    return avg

# Load data
def read_data(filename = 'iris.data'):
    dataset = []
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                continue
            line = line.split(',')
            sample = []
            for d in line:
                if is_number(d):
                    sample.append(float(d))
            dataset.append(sample)
        file.close()
    return dataset

# Generate k centers
def generate_centers(dataset, k):
    centers = []
    dims = len(dataset[0])
    min_arr = [sys.float_info.max, sys.float_info.max, sys.float_info.max, sys.float_info.max]
    max_arr = [sys.float_info.min, sys.float_info.min, sys.float_info.min, sys.float_info.min]
    for sample in dataset:
        for i in xrange(dims):
            value = sample[i]
            if value < min_arr[i]:
                min_arr[i] = value
            if value > max_arr[i]:
                max_arr[i] = value
    for i in xrange(k):
        random = []
        for j in xrange(dims):
            min_val = min_arr[j]
            max_val = max_arr[j]
            select = float('%.1f'%(uniform(min_val, max_val)))
            random.append(select)
        centers.append(random)
    return centers

# Group each sample into a certain certer
def group_sample(dataset, centers):
    group = []
    for sample in dataset:
        shortest_dist = sys.float_info.max
        index = 0
        center_num = len(centers)
        for i in xrange(center_num):
            dist = calc_dist(centers[i], sample)
            if dist < shortest_dist:
                shortest_dist = dist
                index = i
        group.append(index)
    if len(set(group)) < len(centers):
        print 'Error: a center has been assigned zero sample!'
        print 'Please re-run the program.'
        exit()
    return group

# Update centers
def refresh_centers(dataset, group, k):
    new_centers = []
    dict = defaultdict(list)
    for kind, sample in zip(group, dataset):
        dict[kind].append(sample)
    for i in xrange(k):
        vectors = dict[i]
        new_centers.append(avg_vector(vectors))
    return new_centers

# K-means
def k_means(dataset, k):
    init_centers = generate_centers(dataset, k)
    cur_group = group_sample(dataset, init_centers)
    pre_group = None
    while pre_group != cur_group:
        new_centers = refresh_centers(dataset, cur_group, k)
        pre_group = cur_group
        cur_group = group_sample(dataset, new_centers)
    result = list(zip(cur_group, dataset))
    return result

def comp_kmeans():
    
    fig = mpt.subplots(nrows = 2, ncols = 2)
    
    dataset = read_data("iris.data")
    
    # Ground truth label
    label = list(zeros(50)) + list(ones(50)) + list(2 * ones(50))
    result = list(zip(label, dataset))

    class0 = []
    class1 = []
    class2 = []
    for r in result:
        if r[0] == 0:
            class0.append(r[1])
        if r[0] == 1:
            class1.append(r[1])
        if r[0] == 2:
            class2.append(r[1])
    class0 = array(class0)
    class1 = array(class1)
    class2 = array(class2)

    # Group by sepal - ground truth
    mpt.subplot(2, 2, 1)
    mpt.title('Sepal Cluster - Ground Truth')
    mpt.xlabel('sepal-length')
    mpt.ylabel('sepal-width')
    p0 = mpt.scatter(class0[:,0], class0[:, 1], marker = 'x', color = 'm', label = 'setosa', s = 30)
    p1 = mpt.scatter(class1[:,0], class1[:, 1], marker = '+', color = 'c', label = 'versicolor', s = 30)
    p2 = mpt.scatter(class2[:,0], class2[:, 1], marker = 'x', color = 'r', label = 'virginica', s = 30)
    mpt.legend(loc = 'upper right')
    
    # Group by petal - ground truth
    mpt.subplot(2, 2, 3)
    mpt.title('Petal Cluster - Ground Truth')
    mpt.xlabel('petal-length')
    mpt.ylabel('petal-width')
    p0 = mpt.scatter(class0[:,2], class0[:, 3], marker = 'x', color = 'm', label = 'setosa', s = 30)
    p1 = mpt.scatter(class1[:,2], class1[:, 3], marker = '+', color = 'c', label = 'versicolor', s = 30)
    p2 = mpt.scatter(class2[:,2], class2[:, 3], marker = 'x', color = 'r', label = 'virginica', s = 30)
    mpt.legend(loc = 'upper right')

    # Test result
    result = k_means(dataset, 3)

    class0 = []
    class1 = []
    class2 = []
    for r in result:
        if r[0] == 0:
            class0.append(r[1])
        if r[0] == 1:
            class1.append(r[1])
        if r[0] == 2:
            class2.append(r[1])
    class0 = array(class0)
    class1 = array(class1)
    class2 = array(class2)

    # Group by sepal - test
    mpt.subplot(2, 2, 2)
    mpt.title('Sepal Cluster - Test')
    mpt.xlabel('sepal-length')
    mpt.ylabel('sepal-width')
    p0 = mpt.scatter(class0[:,0], class0[:, 1], marker = 'x', color = 'm', label = 'type1', s = 30)
    p1 = mpt.scatter(class1[:,0], class1[:, 1], marker = '+', color = 'c', label = 'type2', s = 30)
    p2 = mpt.scatter(class2[:,0], class2[:, 1], marker = 'x', color = 'r', label = 'type3', s = 30)
    mpt.legend(loc = 'upper right')

    # Group by petal - test
    mpt.subplot(2, 2, 4)
    mpt.title('Petal Cluster - Test')
    mpt.xlabel('petal-length')
    mpt.ylabel('petal-width')
    p0 = mpt.scatter(class0[:,2], class0[:, 3], marker = 'x', color = 'm', label = 'type1', s = 30)
    p1 = mpt.scatter(class1[:,2], class1[:, 3], marker = '+', color = 'c', label = 'type2', s = 30)
    p2 = mpt.scatter(class2[:,2], class2[:, 3], marker = 'x', color = 'r', label = 'type3', s = 30)
    mpt.legend(loc = 'upper right')

    mpt.suptitle('K-means Cluster')
    mpt.show()

def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        comp_kmeans()
    except:
        print >>sys.stderr
        return 1

if __name__ == '__main__':
    sys.exit(main())

