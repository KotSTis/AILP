import caes
import re
import argparse
import sys
import Reader
import copy

def main(file_name):
    propositions, prop_arguments, def_arguments, assums_weights = Reader.extract_lines(file_name)
    PropLiterals, proofs = Reader.prop_process(propositions)
    prop_arg_num, prop_arg_dict = Reader.args_process(prop_arguments, PropLiterals)
    def_arg_num, def_arg_dict = Reader.args_process(def_arguments, PropLiterals)
    main_argset = caes.ArgumentSet()
    main_argset.add_argument(prop_arg_dict['arg1'])
    del prop_arg_dict['arg1']
    z = prop_arg_dict.copy()
    z.update(def_arg_dict)
    assumptions, def_weights, prop_weights = Reader.audience_make(PropLiterals, z, assums_weights, prop_arg_num)
    BoP = False
    caes_object = caes.CAES(main_arget, main_audience, main_weights, proofs)
    BoP = caes_object.acceptable(tested_prop)
    i=0
    while True:
        if not BoP:
            print('Burden of proof is on the accusers')
            print('searching for appropriate argument...')
            for k, v in prop_arg_dict.items():
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                temp_argset.add_argument(v)
                temp_weights[k] = prop_weights[k]
                caes_object = caes.CAES(main_arget, main_audience, main_weights, proofs)
                if not caes_object.acceptable(tested_prop):
                    del prop_arg_dict[k]
                    del prop_weights[k]
                    BoP = not BoP
                    i+=1
                    break
            main_argset = copy.deepcopy(temp_argset)
            main_argset.write_to_graphviz('Insertion No:'+str(i))
            main_weights = copy.deepcopy(temp_weights)
        else:
            print('Burden of proof is on the defence')
            print('searching for appropriate argument...')
            for k, v in def_arg_dict.items():
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                temp_argset.add_argument(v)
                temp_weights[k] = def_weights[k]
                caes_object = caes.CAES(main_arget, main_audience, main_weights, proofs)
                if caes_object.acceptable(tested_prop):
                    del def_arg_dict[k]
                    del def_weights[k]
                    BoP = not BoP
                    i+=1
                    break
                main_argset = copy.deepcopy(temp_argset)
                main_argset.write_to_graphviz('Insertion No:'+str(i))
                main_weights = copy.deepcopy(temp_weights)
            print('selected')
    print("Could not find any arguments that would shift the burden of proof")
    if not BoP:
        print("The defence won")
    else:
        print("The accusers won")
