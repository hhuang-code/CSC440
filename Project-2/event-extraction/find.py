from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import os.path
import subprocess
import pexpect
from subprocess import Popen, PIPE

"""
replace news file content with its title
"""

news_dir = '/home/aaron/Documents/Courses/440/smalldata'
titles_dir = '/home/aaron/Documents/Courses/440/smalltitles'

def gen_titles(news_dir):
    for dirpath, dirnames, filenames in os.walk(news_dir):
        for filename in [f for f in filenames if f.endswith('.txt')]:
            # change directory
            dest_dirpath = dirpath.replace('smalldata', 'smalltitles')
            if not os.path.exists(dest_dirpath):
                os.makedirs(dest_dirpath)
        
            # change file path
            src_filename = os.path.join(dirpath, filename)
            dest_filename = src_filename.replace('smalldata', 'smalltitles')

            # get title
            title = filename.split('.')[0].strip()
        
            # write title as content
            if not os.path.exists(dest_filename):
                with open(dest_filename, 'w') as f:
                    f.write(title + '\n')
                f.close()

# generate a list to store all news title files path
def gen_file_list(titles_dir):
    list_dir = '/home/aaron/Documents/Courses/440'
    list_filename = 'titlelist.txt'
    
    # traverse all title files
    with open(os.path.join(list_dir, list_filename), 'w') as lf:
        for dirpath, dirnames, filenames in os.walk(titles_dir):
            for filename in [f for f in filenames if f.endswith('.txt')]:
                abs_filename = os.path.join(dirpath, filename)
                lf.write(abs_filename + '\n')
    lf.close()

# call OpenIE command to extract event tuples
def extract_tuples(list_filename):
    # result file
    res_filename = '/home/aaron/Documents/Courses/440/result.txt'
    # src file
    src_filename = ''

    with Popen(['java', '-cp', '*', 'edu.stanford.nlp.naturalli.OpenIE', '-format', 'ollie'], 
                stdin = PIPE, stdout = PIPE, universal_newlines = True, bufsize = 1) as cat:
        for i in range(7):
            title = 'Obama was born in united states'
            with open(res_filename, 'a') as rf:
                    print(title, file = cat.stdin, flush = True)
                    rf.write(cat.stdout.readline())
            rf.close()
    cat.wait()

    """
    with open(res_filename, 'a') as rf:
        # tuple format: ollie
        tformat = 'ollie'
        #child = subprocess.Popen(['java', '-cp', '*', 'edu.stanford.nlp.naturalli.OpenIE', 
        #       '-format', tformat, '-filelist', list_filename], stdout = rf)
        child = subprocess.Popen(['java', '-cp', '*', 'edu.stanford.nlp.naturalli.OpenIE', 
                '-format', tformat], stdout = rf)
   
        for i in range(5):
            child.stdin.write(b'Obama was born in unites state')
        
        child.wait()
    """
    """
    while True:
        out = child.stdout.read(1)
        # child subprocess has terminated
        if out == '' and child.poll() != None:
            break
        if out != '':
            print(out)
    """

if __name__ == '__main__':
    #gen_titles(news_dir)
    #gen_file_list(titles_dir)
    list_filename = '/home/aaron/Documents/Courses/440/titlelist.txt'
    extract_tuples(list_filename)
