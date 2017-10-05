import csv
import sys
import pandas as pd
import matplotlib.pyplot as mpt

from numpy import * 
from pandas.plotting import scatter_matrix

# Load data
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

def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        print 'Please input a number to indicate which plot to be drawn:'
        print '1 - Line Plot'
        print '2 - Box Plot'
        print '3 - Histogram'
        print '4 - Kernel Density Estimation'
        print '5 - Scatter'
        print '6 - Hexbin'
        print '0 - Exit'
        while True:
            print 'Input (0 to exit):'
            user_input = raw_input()
            if user_input == '0':
                return
            elif user_input == '1':
                lineplot()
            elif user_input == '2':
                boxplot()
            elif user_input == '3':
                histogram()
            elif user_input == '4':
                kdeplot()
            elif user_input == '5':
                scatter_mat()
            elif user_input == '6':
                hexbin()
            else:
                print 'Error! Please input again'
    except:
        print >>sys.stderr
        return 1

if __name__ == '__main__':
    sys.exit(main())
 
