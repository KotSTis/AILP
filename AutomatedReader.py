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
    failure = False
    #this is the main loop of the program
    while True:
        #checks where the Burden of Proof lies and decides which side's turn
        #it is to speak
        if BoP:
            #the comments for this part of the if else control flow are the same
            #for the both parts with the exception of whether we select arguments
            #from the defence or the prosecution. For this reason we won't comments
            #the second part of the if else
            print('Burden of proof is on the prosecutionm')
            print('searching for appropriate argument(s)...')
            #this loop incrememnts the number of arguments can be used in one round
            for i in range(len(prop_arg_dict)):
                #copying the main argset and weights so we can test each set of arguments and weights
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                #getting all the possible combinations of arguments of length i
                arg_keys = list(itertools.combinations(prop_arg_dict, i + 1))
                for  setno in range(len(arg_keys)):
                    for key in range(i):
                        temp_argset.add_argument(prop_arg_dict[arg_keys[setno][key]], arg_id=arg_keys[setno][key])
                        temp_weights[arg_keys[setno][key]] = prop_weights[arg_keys[setno][key]]

                    temp_audience = caes.Audience(assumptions, temp_weights)
                    caes_object = caes.CAES(temp_argset, temp_audience, proofs)
                    if not caes_object.acceptable(tested_prop):
                        #loop that removes the arguments and weights that were used
                        #from the bank of availability if the BoP changes
                        for key in range(i):
                            del prop_arg_dict[arg_keys[i][key]]
                            del prop_weights[arg_keys[i][key]]
                        #changing the BoP
                        BoP = not BoP
                        #inceremnting the number of the turn since the BoP changed
                        turn += 1

                        #copying the temporary argset and weights that worked to the main ones
                        main_argset = copy.deepcopy(temp_argset)
                        main_weights = copy.deepcopy(temp_weights)
                        main_argset.write_to_graphviz('Insertion No:' + str(turn))
                        break
                #if the program goes through on this if it means that we have explored all using
                #all available arguments but we couldnt change the BoP therefore the session
                #comes to an end
                if i == len(prop_arg_dict)-1:
                    failure = True
        else:
            print('Burden of proof is on the defence')
            print('searching for appropriate argument(s)...')
            for i in range(len(def_arg_dict)):
                temp_argset = copy.deepcopy(main_arget)
                temp_weights = copy.deepcopy(main_weights)
                arg_keys = itertools.combinations(prop_arg_dict, i + 1)
                for  setno in range(len(arg_keys)):
                    for key in range(i):
                        temp_argset.add_argument(
                            def_arg_dict[arg_keys[setno][key]], arg_id=arg_keys[setno][key])
                        temp_weights[arg_keys[setno][key]] = def_weights[arg_keys[setno][key]]
                    temp_audience = caes.Audience(assumptions, temp_weights)
                    caes_object = caes.CAES(temp_argset, temp_audience, proofs)
                    if caes_object.acceptable(tested_prop):
                        for key in range(i):
                            del def_arg_dict[arg_keys[i][key]]
                            del def_weights[arg_keys[i][key]]
                        BoP = not BoP
                        turn += 1

                        main_argset = copy.deepcopy(temp_argset)
                        main_argset.write_to_graphviz('Insertion No:' + str(turn))
                        main_weights = copy.deepcopy(temp_weights)
                        break
                if i == len(prop_arg_dict)-1:
                    failure = True
        #printing the arguments that are currently used
        print('Arguments on the table: ', caes_object.get_all_arguments())
        if failure:
            print("Could not find any combinations of arguments that would shift the burden of proof")
            break
    if not BoP:
        print("The defence won")
    else:
        print("The accusers won")
