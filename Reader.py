import caes
import re
import argparse
import sys


class Reader():
    file_name = sys.argv[1]
    out_file = open('docstring.py','w')


    propositions, arguments, assums_weights = extract_lines(file_name)
    PropLiterals = prop_process(propositions)
    ArgSet = args_process(arguments, PropLiterals)
    AssumsWeights = assums_process(ArgSet, PropLiterals, assums_weights)



    def extract_lines(file_name):
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
            propositions = [i.strip('\n') for i in propositions if i[0]!='#']
            arguments = [i.strip('\n') for i in arguments if i[0]!='#']
            assums_weights = [i.strip('\n') for i in assums_weight if i[0]!='#']


            return propositions, arguments, assums_weights

    def get_set_props(words, prop_dict):
        props = set()
            for word in words:
                if word in prop_dict.keys():
                    props.add(prop_dict[word])

        return props

    def prop_process(list):
        propositions = {}
        for i in list:
            if !i.isalpha():
                i = i.replace (" ", "_")
            if (i[0]!='-'):
                propositions['i'] = caes.PropLiteral(i)
            else:
                propositions['i'] = caes.PropLiteral(i).negate()

        return propositions

    def args_process(list, prop_dict):
        arguments = {}
        conclusion = set()
        premises = set()
        exceptions = set()
        words_pattern = re.compile(r'\b([a-zA-Z_]+)')
        for arg in list:
            argNum = re.match('[1-9]+\.', arg)
            if len(argNum):
                words = words_pattern.findall(arg)
                i=0
                for word in words.groups:
                    #we get the indices of each section of the argument
                    #by checking against a list of words that user knows
                    #they should use, as indicated in the README
                    if word in conc_words:
                        conc_idx = i
                    elif word in premise_words:
                        prem_idx = i
                    elif word in exception_words:
                        exc_idx = i
                    i+=1
                #get a list of the propLiterals for each part of the argument
                #we do this by calling the get_set_props which return the
                #propLiterals found in a list of words
                conclusion = get_set_props(words[conc_idx,prem_idx-1], prop_dict)
                premises = get_set_props(words[prem_idx,exc_idx-1], prop_dict)
                exceptions = get_set_props(words[exc_idx, len(words)-1], prop_dict)

                arguments[arg + str(argNum)] = caes.Argument(conclusion, premises, exceptions)
            else:
                print("you forgot to number your arguments!")

        return arguments

    def assums_process(prop_dict, args_dict, l  ist):
