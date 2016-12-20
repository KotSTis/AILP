import caes
import re
import argparse
import sys
import Reader
import copy


def main(file_name, debated_prop):
    propositions, prop_arguments, def_arguments, assums_weights = Reader.extract_lines(
        file_name)
    PropLiterals, proofs = Reader.prop_process(propositions)
    prop_arg_num, prop_arg_dict = Reader.args_process(
        prop_arguments, PropLiterals)
    def_arg_num, def_arg_dict = Reader.args_process(
        def_arguments, PropLiterals)
    main_argset = caes.ArgumentSet()
    main_argset.add_argument(prop_arg_dict['arg1'])
    tested_prop = PropLiterals[debated_prop]
    del prop_arg_dict['arg1']
    z = prop_arg_dict.copy()
    z.update(def_arg_dict)
    assumptions, def_weights, prop_weights = Reader.audience_make(
        PropLiterals, z, assums_weights, prop_arg_num)
    BoP = False
    caes_object = caes.CAES(main_arget, main_audience, main_weights, proofs)
    BoP = caes_object.acceptable(tested_prop)
    turn = 0
    while True:
        if BoP:
            for i in range(len(prop_arg_dict)):
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                arg_keys = itertools.combinations(prop_arg_dict, i + 1)
                for key in range(i):
                    temp_argset.add_argument(
                        prop_arg_dict[arg_keys[i][key]], arg_id=arg_keys[i][key])
                    temp_weights[arg_keys[i][key]] = prop_weights[arg_keys[i][key]]
                temp_audience = caes.Audience(assumptions, temp_weights)
                caes_object = caes.CAES(temp_argset, temp_audience, proofs)
                if not caes_object.acceptable(tested_prop):
                    for key in range(i):
                        del prop_arg_dict[arg_keys[i][key]]
                        del prop_weights[arg_keys[i][key]]
                    BoP = not BoP
                    turn += 1
                    break
            main_argset = copy.deepcopy(temp_argset)
            main_argset.write_to_graphviz('Insertion No:' + str(turn))
            main_weights = copy.deepcopy(temp_weights)
        else:
            print('Burden of proof is on the defence')
            print('searching for appropriate argument...')
            for i in range(len(def_arg_dict)):
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                arg_keys = itertools.combinations(prop_arg_dict, i + 1)
                for key in range(i):
                    temp_argset.add_argument(
                        def_arg_dict[arg_keys[i][key]], arg_id=arg_keys[i][key])
                    temp_weights[arg_keys[i][key]] = def_weights[
                        arg_keys[i][key]]
                temp_audience = caes.Audience(assumptions, temp_weights)
                caes_object = caes.CAES(temp_argset, temp_audience, proofs)
                if not caes_object.acceptable(tested_prop):
                    for key in range(i):
                        del def_arg_dict[arg_keys[i][key]]
                        del def_weights[arg_keys[i][key]]
                    BoP = not BoP
                    turn += 1
                    break
            main_argset = copy.deepcopy(temp_argset)
            main_argset.write_to_graphviz('Insertion No:' + str(turn))
            main_weights = copy.deepcopy(temp_weights)
        print('Arguments on the table: ', caes_object.get_all_arguments())
    print("Could not find any combinations of arguments that would shift the burden of proof")
    if not BoP:
        print("The defence won")
    else:
        print("The accusers won")
