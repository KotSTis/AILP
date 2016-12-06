import caes
import Reader
import re
import sys


class RealTimeArg():

    def __init__(self, file_name):
        # since there are only two sides arguing we can encode the Burden of Proof
        # with a binary value, True indicating its on the proposition and False
        # that the burden of proof is on the defence
        bop = True
        self.file_name = file_name
        self.propositions, self.assumsumptions = self.extract_lines(file_name)
        self.PropLiterals, self.proofs = self.prop_process(self.propositions)

        #audience = audience_make(PropLiterals, arg_dict, assums_weights)
        # ArgSet.write_to_graphviz()
        #caes_object = caes.CAES(ArgSet, audience, proofs)

    def extract_lines(self, file_name):
        # regex to find the section start
        props = re.compile('PROPOSITIONS')
        assums = re.compile('ASSUMPTIONS')
        # lists with each line of their respective sections
        propositions = []
        assumsumptions = []
        # loop to get the section start lines
        # we use a with as loop to keep everything cleaner
        with open(file_name) as f:
            for i, line in enumerate(f):
                if props.match(line):
                    p = i
                if assums.match(line):
                    assu = i

            f.seek(0)
            propositions = f.readlines()[p + 1:assu - 1]
            f.seek(0)
            assums_weight = f.readlines()[assu + 1:]

        # stripping newlines and removing comment lines that start with '#'
        propositions = [i.strip('\n') for i in propositions if i[0] != '#']
        assums_weights = [i.strip('\n') for i in assums_weight if i[0] != '#']
        return propositions, assums_weights

    def prop_process(self, list_prop):
        propositions = {}
        proof_standards = []
        # regex for extracting any proof standards
        reg = r"\((.*?)\)"
        for i in list_prop:
            proof_std = re.findall(reg, i)
            if proof_std:
                # splitting the proposition and the proof standard if it exists
                words = i.split()
                key = words[0]
                value = words[0].strip('-')
            else:
                key = i
                value = i.strip('-')
            # checking if a proposition has negation
            if '-' in key:
                propositions[key] = caes.PropLiteral(value).negate()
            else:
                propositions[key] = caes.PropLiteral(value)
            if proof_std:
                proof_standards.append((propositions[key], proof_std[0]))
            # initializing proof standard
            ps = caes.ProofStandard(proof_standards)
        return propositions, ps

    def add_arg(self, argument, prop_dict, arg_set, argNum):
        # initializing argument dictionary
        arguments = {}
        prem = set()
        exc = set()
        # regex for separating and storing words
        words_pattern = re.compile(r'(-*[\w_]+)')
        # words that indicate the start of each respective section of an argument
        # they are indicated in the readme file
        conc_words = ['claims', 'says']
        premise_words = ['depends', 'requires']
        exception_words = ['voided', 'nullified']

        words = words_pattern.findall(arg)
        i = 0
        conc_idx = 0
        prem_idx = 0
        exc_idx = 0
        # we get the indices of each section of the argument
        # by checking against a list of words that user knows
        # they should use, as indicated in the README
        for word in words:
            # setting the index of each section by checking for the existence
            # of the key words
            if word in conc_words:
                conc_idx = i
            elif word in premise_words:
                prem_idx = i
            elif word in exception_words:
                exc_idx = i
            # increasing i so it goes to the next word
            i += 1
        # we are now checking inside these sections for the propositional
        # literals and adding them to the correct set
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
        if not exc_idx == 0:
            for prop in words[exc_idx + 1:]:
                if prop in prop_dict:
                    exc.add(prop_dict[prop])
        # adding the argument with its correct key to the argument dictionary
        arg = caes.Argument(conclusion=conc, premises=prem, exceptions=exc)
        arg_set.add_argument(arg, arg_id=argNum)

        return arg_set, arguments

    def get_continuous_input(self):
        debated_proposition = input("Which main proposition of the argument?")
        if debated_proposition not in self.propositions
        while True:
            if bop = True:
                print('Burden of proof about {} is on the proposition'.format(
                    debated_proposition))
            else:
                print('Burden of proof  about {} is on the defence'.format(
                    debated_proposition))
            argument = input('>>> ')
            self.ArgSet, self.arg_dict = self.add_arg(
                argument, self.PropLiterals)
            if argument == 'end':
                print("Goodbye :)")
                sys.exit()
            accepted_before = caes_obj.acceptable(debated_proposition)
            # stuff to update teh caes object
            accepted_after = caes_obj.acceptable(debated_proposition)

            if accepted_after == accepted_before:
                print("the burden of proof has switched")
