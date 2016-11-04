import caes
import re
import argparse
import sys


class Reader():
    file_name = sys.argv[1]
    out_file = open('docstring.py','w')

    #regex to find the section start
    props = re.compile('PROPOSITIONS')
    args = re.compile('ASSUMPTIONS AND WEIGHTS')
    assums = re.compile('ASSUMPTIONS AND WEIGHTS')
    #lists with each line of their respective sections
    propositions = []
    arguments = []
    assums_weight = []
    #loop to get the section start lines
    #we use a with as loop to keep everything cleaner
    with open(file_name) as f:
        for i, line in enumerate(f):
            if props.match(line):
                p = i;
            if args.match(line):
                ar = i;
            if assums.match(line):
                assu = i;

        f.seek(0)
        propositions = f.readlines()[p+1:ar-1]
        arguments = f.readlines()[ar+1:assu-1]
        assums_weight = f.readlines()[assu+1:]


    #stripping newlines and removing comment lines that start with '#'
    arguments = [i.strip('\n') for i in arguments if i[0]!='#']
    assums_weights = [i.strip('\n') for i in assums_weight if i[0]!='#']
    propositions = [i.strip('\n') for i in propositions if i[0]!='#']




    def prop_process(list):
        propositions = {}
        for i in list:
            if not i.isalpha():
                i = i.replace (" ", "_")
            if (i[0]!='-'):
                propositions['i'] = caes.PropLiteral(i)
            else:
                propositions['i'] = caes.PropLiteral(i).negate()

        return propositions



    def args_process(list):
        delimiters = ['\n', ' ', ',', '.', '?']
        argumens = {}
        for arg in list:
            if re.match('[1-9]+\.', arg):


            else:
                print("you need to mark the number of each argument said as mentioned in the README")




    #def assums_process(list):
