import caes
import re
import argparse
import sys

def extract_lines(file_name):
        #regex to find the section start
        props = re.compile('PROPOSITIONS')
        args_for = re.compile('ARGUMENTS PROSECUTION')
        args_against = re.compile('ARGUMENTS DEFENCE')
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
                if args_for.match(line):
                    arf = i;
                if args_against.match(line):
                    ara = i
                if assums.match(line):
                    assu = i;

            f.seek(0)
            propositions = f.readlines()[p+1:arf-1]
            f.seek(0)
            arguments_for = f.readlines()[arf+1:ara-1]
            f.seek(0)
            arguments_against = f.readlines()[ara+1:arf-1]
            f.seek(0)
            assums_weight = f.readlines()[assu+1:]


        #stripping newlines and removing comment lines that start with '#'
        propositions = [i.strip('\n') for i in propositions if i[0]!='#']
        arguments_for = [i.strip('\n') for i in arguments_for if i[0]!='#']
        arguments_against = [i.strip('\n') for i in arguments_against if i[0]!='#']
        assums_weights = [i.strip('\n') for i in assums_weight if i[0]!='#']


        return propositions, arguments_for, arguments_against, assums_weights

def prop_process(list_prop):
    propositions = {}
    proof_standards = []
    #regex for extracting any proof standards
    reg = r"\((.*?)\)"
    for i in list_prop:
        proof_std = re.findall(reg, i)
        if proof_std:
            #splitting the proposition and the proof standard if it exists
            words = i.split()
            key = words[0]
            value = words[0].strip('-')
        else:
            key = i
            value = i.strip('-')
        #checking if a proposition has negation
        if '-' in key:
            propositions[key] = caes.PropLiteral(value).negate()
        else:
            propositions[key] = caes.PropLiteral(value)
        if proof_std:
            proof_standards.append((propositions[key], proof_std[0]))
        #initializing proof standard
        ps = caes.ProofStandard(proof_standards)
    return propositions, ps

def prop_args_process(list_args, prop_dict):
    #filtering any empty lines
    list_args = list(filter(None, list_args))
    #initializing argument dictionary
    arguments = {}
    prem = set()
    exc = set()
    #regex for separating and storing words
    words_pattern = re.compile(r'(-*[\w_]+)')
    #words that indicate the start of each respective section of an argument
    #they are indicated in the readme file
    conc_words = ['claims', 'says']
    premise_words = ['depends', 'requires']
    exception_words = ['voided', 'nullified']
    #initializing the argument set
    arg_set = caes.ArgumentSet()
    #iterating over arguments
    for arg in list_args:
        #finding argument number to make sure everything is formatted correctly
        argNum = re.findall('([1-9]+)\.', arg)
        if len(argNum)>0:
            words = words_pattern.findall(arg)
            i = 0
            conc_idx = 0
            prem_idx = 0
            exc_idx = 0
            #we get the indices of each section of the argument
            #by checking against a list of words that user knows
            #they should use, as indicated in the README
            for word in words:
                #setting the index of each section by checking for the existence of the key words
                if word in conc_words:
                    conc_idx = i
                elif word in premise_words:
                    prem_idx = i
                elif word in exception_words:
                    exc_idx = i
                #increasing i so it goes to the next word
                i+=1
            #we are now checking inside these sections for the propositional
            #literals and adding them to the correct set
            for prop in words[:conc_idx]:
                if prop in prop_dict:
                    prem.add(prop_dict[prop])

            for prop in words[conc_idx:prem_idx]:
                if prop in prop_dict:
                    conc = prop_dict[prop]

            if not prem_idx == 0:
                for prop in words[prem_idx:exc_idx]:
                    if prop in prop_dict:
                        prem.add(prop_dict[prop])

            if  not exc_idx == 0:
                for prop in words[exc_idx+1:]:
                    if prop in prop_dict:
                        exc.add(prop_dict[prop])
            #adding the argument with its correct key to the argument dictionary
            arguments['arg' + str(argNum[0])] = caes.Argument(conclusion=conc, premises=prem, exceptions=exc)
        else:
            print("you need to mark the number of each argument said as mentioned in the README")
            exit
    return arguments

def audience_make(prop_dict, args_dict, list_aud, cutoffpoint):
    assumptions = set()
    if not list_aud[0] == 'no assumptions':
        assumptions_raw = [line.strip() for line in list_aud[0].split(',')]
        for value in assumptions_raw:
            if value in prop_dict:
                assumptions.add(prop_dict[value])
        if len(assumptions) == 0 and len(assumptions_raw) >0:
            print("you seem to have something for a assumption but none of that is a propLiteral")

    weights_raw = [line.strip() for line in list_aud[1].split(',')]
    weights = {}
    i=1
    if not len(weights_raw) == len(args_dict):
        print("you seem to not have weights for every argument, please do that.")
    else:
        for weight in weights_raw[:cutoffpoint]:
            prop_weights[args_dict['arg'+str(i)]] = weight
            i+=1;
        for weight in weights_raw[cutoffpoint+1:]:
            def_weights[args_dict['arg'+str(i)]] = weight
            i+=1
    return assumptions,def_weights, prop_weights
