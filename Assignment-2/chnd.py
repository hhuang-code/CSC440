"""
Automatic generation of a concept hierarchy for nominal data based on the number of distinct values of attributes
"""

import operator

def attr_gen():
    print 'How many attributes you want to use? Enter the number of attributes:'
    num_str = raw_input()
    num = int(num_str)
    attr_dict = {}   # Key is attribute name, value is a list storing attribute values
    for i in range(num):
        print 'Enter the name of attribute %d:' % (i + 1)
        attr_name = raw_input()
        attr_dict[attr_name] = []
        print 'Enter values of attribue %d, separated by single space, ended with carriage returns:' % (i + 1)
        line = raw_input().strip('\n').split(' ')
        for j in range(len(line)):
            if line[j].strip() != '':
                attr_dict[attr_name].append(line[j])
    return attr_dict

def attr_display(attr_dict):
    print '---------------Attributes and their values---------------'
    for key, value in attr_dict.items():
        print key , ' : ' , value

def hrchy_gen(attr_dict):
    hrchy = {}
    for key, value in attr_dict.items():
        hrchy[key] = len(list(set(attr_dict[key])))
    hrchy_sorted = sorted(hrchy.items(), key = operator.itemgetter(1))
    return hrchy_sorted

def hrchy_draw(hrchy):
    print '-----Concept hierarchy (from high level to low level)-----'
    for elem in hrchy[:-1]:
        print elem[0], '(', elem[1], ') ---> ',
    else:
        print hrchy[-1][0], '(', elem[-1], ')'

if __name__ == '__main__':
    attr_dict = attr_gen()
    attr_display(attr_dict)
    hrchy_sorted = hrchy_gen(attr_dict)
    hrchy_draw(hrchy_sorted)
