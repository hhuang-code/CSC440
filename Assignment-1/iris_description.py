"""
- Data mining assignment 1
- @Author: Hao Huang
- @Date: Sept.12.2017
"""

import csv
import re
import math
import sys
import traceback
import pylab
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as mpt

from numpy import *
from pandas.plotting import scatter_matrix

# Check if a string is a number
def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+?')
    result = pattern.match(string)
    if result:
        return True
    else:
        return False

# Basic statistics indicators
def describe(filepath = 'iris.data'):
    
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
    print
    print '===========================BASIC DESCRIPTION============================'
    print 'sepal-length'.rjust(23), 'sepal-width'.rjust(15), 'petal-length'.rjust(15), 'petal-width'.rjust(15)
    print 'count'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(count[i]).rjust(15),
    print
    
    print 'mean'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(mean[i]).rjust(15),
    print
 
    print 'std'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(std[i]).rjust(15),
    print

    print 'min'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(minimum[i]).rjust(15),
    print

    print '25%'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(fquartile[i]).rjust(15),
    print

    print 'median'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(fquartile[i]).rjust(15),
    print
    
    print '75%'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(tquartile[i]).rjust(15),
    print
    
    print 'max'.ljust(6),
    for i in feature_num:
        print '{0:.6f}'.format(maximum[i]).rjust(15),
    print '\n'

# Group by
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
        print 'No such label (sepal-length\sepal-width\petal-length\petal-width\class) in dataset.'
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
    print titles[group_index].ljust(20), 'count'.rjust(5)
    for key in sorted(dictionary.keys()):
        print key.ljust(20), str(len(dictionary[key])).rjust(5)
    print

# Calculate covariance of each column
def cov_mat(filepath = 'iris.data', is_print = True):
  
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
    
    # Generate a matrix without the label column
    mat = []
    imatrix = array(imatrix)
    imatrix = imatrix[:, feature_num]
    for i in xrange(sample_num):
        mat.append(map(float, imatrix[i]))
    
    # Calculate mean of each column
    mean = []
    for i in feature_num:
        sum = 0.0
        for j in xrange(sample_num):
            sum += mat[j][i]
        mean.append(sum / sample_num)

    # Substract mean from each column
    mean = tile(mean, (sample_num, 1))   
    mat = mat - mean

    # Calculate covariance: trans(M) * M / (n - 1)
    cov = dot(mat.T, mat) / (sample_num - 1)
    
    # Display the covariance matrix
    if is_print:
        print
        print '=================================COVARIANCE MATRIX=============================='
        labels = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']
        row_num = len(cov)
        col_num = len(cov[0])
        print ''.rjust(15),
        for k in xrange(col_num):
            print labels[k].rjust(15),
        print
        for i in xrange(row_num):
            print labels[i].rjust(15),
            for j in xrange(col_num):
                print '{0:.6f}'.format(cov[i][j]).rjust(15),
            print
        print   

    # Return covariance
    return cov

# Calculate correlation coefficient of each column
def cor_coeff(filepath = 'iris.data'):
    
    # Get covariance
    cov = cov_mat(filepath, False)

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

    # Correlation coefficient: cov(X, Y) / (std(X) * std(Y))
    row_num = len(cov)
    col_num = len(cov[0])
    coeff = [[0 for i in xrange(col_num)] for i in xrange(row_num)]
    for i in xrange(row_num):
        for j in xrange(col_num):
            coeff[i][j] = cov[i][j] / (std[i] * std[j])

    # Display the covariance matrix
    print
    print '============================CORRELATION COEFFICIENT============================='
    labels = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width']
    row_num = len(cov)
    col_num = len(cov[0])
    print ''.rjust(15),
    for k in xrange(col_num):
        print labels[k].rjust(15),
    print
    for i in xrange(row_num):
        print labels[i].rjust(15),
        for j in xrange(col_num):
            print '{0:.6f}'.format(coeff[i][j]).rjust(15),
        print
    print
    
    # Return coefficient
    return coeff

# Load data for visualization
def loaddata(filename = 'iris.data'):
    feature_names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pd.read_csv(filename, names = feature_names)
    return dataset

# Line plot
def lineplot(filename = 'iris.data'):
    dataset = loaddata(filename)
    dataset.plot(kind = 'line', title = 'Line Plot', subplots = True, layout = (2, 2), sharex = False, sharey = False)
    mpt.show()

# Box plot
def boxplot(filename = 'iris.data'):
    dataset = loaddata(filename)
    dataset.plot(kind = 'box', title = 'Box Plot', subplots = True, layout = (2, 2), sharex = False, sharey = False)
    mpt.show()

# Quantile plot
def quantileplot(filename = 'iris.data'):
    dataset = loaddata(filename)
    df = pd.DataFrame({'mean': dataset.mean(), 'min': dataset.values.min(), '25%': dataset.quantile(0.25), 'median': dataset.median(), '75%': dataset.quantile(0.75)})
    df.plot()
    mpt.suptitle('Quantile Plot')
    mpt.show()

# Quantile-Quantile plot
def qqplot(filename = 'iris.data'):
    dataset = loaddata(filename)
    dataarray = array(dataset)
    # Iris-setosa
    fig1 = mpt.figure()
    ax11 = fig1.add_subplot(221)
    stats.probplot(map(float, dataarray[0: 50, 0]), dist = 'norm', plot = ax11)
    ax11.set_title('sepal-length')
    ax12 = fig1.add_subplot(222)
    stats.probplot(map(float, dataarray[0: 50, 1]), dist = 'norm', plot = ax12)
    ax12.set_title('sepal-width')
    ax13 = fig1.add_subplot(223)
    stats.probplot(map(float, dataarray[0: 50, 2]), dist = 'norm', plot = ax13)
    ax13.set_title('petal-length')
    ax14 = fig1.add_subplot(224)
    stats.probplot(map(float, dataarray[0: 50, 3]), dist = 'norm', plot = ax14)
    ax14.set_title('petal-width')
    mpt.suptitle('Quantile-Quantile Plot: Iris-setosa')
    # Iris-versicolor
    fig2 = mpt.figure()
    ax21 = fig2.add_subplot(221)
    stats.probplot(map(float, dataarray[50: 100, 0]), dist = 'norm', plot = ax21)
    ax21.set_title('sepal-length')
    ax22 = fig2.add_subplot(222)
    stats.probplot(map(float, dataarray[50: 100, 1]), dist = 'norm', plot = ax22)
    ax22.set_title('sepal-width')
    ax23 = fig2.add_subplot(223)
    stats.probplot(map(float, dataarray[50: 100, 2]), dist = 'norm', plot = ax23)
    ax23.set_title('petal-length')
    ax24 = fig2.add_subplot(224)
    stats.probplot(map(float, dataarray[50: 100, 3]), dist = 'norm', plot = ax24)
    ax24.set_title('petal-width')
    mpt.suptitle('Quantile-Quantile Plot: Iris-versicolor')
    # Iris-virginica
    fig3 = mpt.figure()
    ax31 = fig3.add_subplot(221)
    stats.probplot(map(float, dataarray[100: 150, 0]), dist = 'norm', plot = ax31)
    ax31.set_title('sepal-length')
    ax32 = fig3.add_subplot(222)
    stats.probplot(map(float, dataarray[100: 150, 1]), dist = 'norm', plot = ax32)
    ax32.set_title('sepal-width')
    ax33 = fig3.add_subplot(223)
    stats.probplot(map(float, dataarray[100: 150, 2]), dist = 'norm', plot = ax33)
    ax33.set_title('petal-length')
    ax34 = fig3.add_subplot(224)
    stats.probplot(map(float, dataarray[100: 150, 3]), dist = 'norm', plot = ax34)
    ax34.set_title('petal-width')
    mpt.suptitle('Quantile-Quantile Plot: Iris-virginica')
    mpt.show()

# Histogram
def histogram(filename = 'iris.data'):
    dataset = loaddata(filename)
    axarr = dataset.hist(bins = 20)
    for ax in axarr.flatten():
        ax.set_xlabel('unit: cm')
        ax.set_ylabel('cumulative num')
    mpt.suptitle('Histogram')
    mpt.show()

# Kernel Density Estimation
def kdeplot(filename = 'iris.data'):
    dataset = loaddata(filename)
    dataset.plot(kind = 'density', title = 'Kernel Density Estimation', subplots = True, layout = (2, 2), sharex = False, sharey = False)
    mpt.show()


# Scatter plot matrix
def scatter_mat(filename = 'iris.data'):
    dataset = loaddata(filename)
    scatter_matrix(dataset)
    mpt.suptitle('Scatter Matrix')
    mpt.show()

# Hexbin
def hexbin(filename = 'iris.data'):
    dataset = loaddata(filename)
    dataset.plot(kind = 'hexbin', title = 'Hexbin', x = 'sepal-length', y = 'sepal-width')
    dataset.plot(kind = 'hexbin', title = 'Hexbin', x = 'petal-length', y = 'petal-width')
    mpt.show()


# Main function
def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        print '\nWelcome to IRIS data set!'
        print 'Please choose which one to present:' 
        print 'A - Basic statistical indicators'
        print 'B - Group by a label'
        print 'C - Correlation analysis'
        print 'D - Visualization'
        print 'Z - Exit'
        while True:
            print 'Your choice(A\B\C\D\Z):'
            first_level = raw_input()
            if first_level.upper() == 'Z':
                return
            elif first_level.upper() == 'A':
                describe()
            elif first_level.upper() == 'B':
                print 'Please type a label (sepal-length\sepal-width\petal-length\petal-width\class) to group by:'
                group_label = raw_input()
                groupby(label = group_label)
            elif first_level.upper() == 'C':
                cov_mat()
                cor_coeff()
            elif first_level.upper() == 'D':
                print 'Please type a number to indicate which plot to be drawn:'
                print '1 - Line Plot\n2 - Box Plot\n3 - Quantile Plot\n4 - Quantile-Quantile Plot\n5 - Histogram'
                print '6 - Kernel Density Estimation\n7 - Scatter\n8 - Hexbin\n0 - Exit'
                while True:
                    print 'Input (0 to exit):'
                    second_level = raw_input()
                    if second_level == '0':
                        return
                    elif second_level == '1':
                        lineplot()
                    elif second_level == '2':
                        boxplot()
                    elif second_level == '3':
                        quantileplot()
                    elif second_level == '4':
                        qqplot()
                    elif second_level == '5':
                        histogram()
                    elif second_level == '6':
                        kdeplot()
                    elif second_level == '7':
                        scatter_mat()
                    elif second_level == '8':
                        hexbin()
                    else:
                        print 'Error! Please input again (1\2\3\4\5\6\7\8\0).'
            else:
                print 'Error! Please input again (A\B\C\D\Z).'
    except Exception, e:
        print traceback.format_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

