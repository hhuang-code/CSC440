import csv
import re
import math
import sys
from numpy import *

# Check if a string is a number
def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+?')
    result = pattern.match(string)
    if result:
        return True
    else:
        return False

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
    
def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        cov_mat()
        cor_coeff()
    except:
        print >>sys.stderr
        return 1

if __name__ == '__main__':
    sys.exit(main())
