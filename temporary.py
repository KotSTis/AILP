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
