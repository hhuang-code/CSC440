"""
Automatic generation of a concept hierarchy for numeric data based on the equal-frequency partitioning rule
"""

import math
import numpy as np

class SBin:
    def __init__(self):
        self.low_bound = 0
        self.high_bound = 0
        self.content = []

def attr_gen():
    print 'How many values you want to use for an attribute? Enter the number of values:'
    num_str = raw_input()
    num = int(num_str)
    line = ''
    while True:
        print 'Enter the min and max value, separated by single space, ended with carriage returns:'
        line = raw_input().strip('\n').split(' ')
        if len(line) == 2:
            break
    max = int(line[0]) if int(line[0]) > int(line[1]) else int(line[1])
    min = int(line[0]) if int(line[0]) < int(line[1]) else int(line[1])
    values = np.random.randint(min, max + 1, size = num)
    return values

def attr_display(values):
    print '-------------Values (generated randomly) for the attribute-------------'
    for i in range(len(values)):
        print values[i], ' ',
    print

def binning(values, bin_depth):
    values.sort()
    low_bound = min(values)
    bin_num = len(values) / bin_depth if len(values) % bin_depth == 0 else len(values) / bin_depth + 1
    bins = []
    for i in range(bin_num):
        bin = SBin()
        bins.append(bin)
    j = 0
    cnt = 0
    for v in values:
        if cnt < bin_depth:
            cnt = cnt + 1
        else:
            bins[j].high_bound = v - 1
            cnt = 0
            j = j + 1
        bins[j].content.append(v)
        bins[j].low_bound = v

    #for i in range(bin_num):
        #print bins[i].low_bound, ' ', bins[i].high_bound, ' ', bins[i].content
    return bins
 
def hrchy_gen(values):
    print 'Enter how many levels of hirerachy you want? (Not samller than 1 and not larger than %d)' % (math.log(len(values), 2) + 1)
    level_num = int(raw_input())
    hrchy = {}
    hrchy[0] = [binning(values, len(values))]
    cnt = 1
    while cnt < level_num:
        hrchy[cnt] = []
        for bins in hrchy[cnt - 1]:
            for bin in bins:
                hrchy[cnt].append(binning(bin.content, len(bin.content) / 2))
        cnt = cnt + 1
    return hrchy, level_num

def hrchy_display(hrchy, level_num):
    cnt = 0
    while cnt < level_num:
        print '--------------------------- level %d ---------------------------' % cnt
        for bins in hrchy[cnt]:
            for bin in bins:
                print 'low_bound:', bin.low_bound, ' high_bound:'.ljust(10), bin.high_bound, ' '.ljust(10), bin.content
        print
        cnt = cnt + 1

if __name__ == '__main__':
    values = attr_gen()
    attr_display(values)
    hrchy, level_num = hrchy_gen(values)
    hrchy_display(hrchy, level_num)
