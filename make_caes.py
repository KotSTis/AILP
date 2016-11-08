def make_caes(file_name):
    import Reader
    propositions, arguments, assums_weights = Reader.extract_lines(file_name)
    PropLiterals, proofs = Reader.prop_process(propositions)
    ArgSet, arg_dict =  Reader.args_process(arguments, PropLiterals)
    audience =  Reader.audience(PropLiterals, arg_dict, assums_weights)
    ArgSet.write_to_graphviz()
    caes_object =  Reader.caes.CAES(ArgSet, audience, proofs)
    return caes_object
