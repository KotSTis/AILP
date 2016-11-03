    kill = PropLiteral('kill')
    intent = PropLiteral('intent')
    neg_intent = intent.negate()
    murder = PropLiteral('murder')
    witness1 = PropLiteral('witness1')
    unreliable1 = PropLiteral('unreliable1')
    witness2 = PropLiteral('witness2')
    unreliable2 = PropLiteral('unreliable2')

    ps = ProofStandard([(intent, "beyond_reasonable_doubt")])

    arg1 = Argument(murder, premises={kill, intent})
    arg2 = Argument(intent, premises={witness1}, exceptions={unreliable1})
    arg3 = Argument(neg_intent, premises={witness2}, exceptions={unreliable2})

    argset = ArgumentSet()
    argset.add_argument(arg1)
    argset.add_argument(arg2)
    argset.add_argument(arg3)
    argset.draw()
    argset.write_to_graphviz()

    assumptions = {kill, witness1, witness2, unreliable2}
    weights = {'arg1': 0.8, 'arg2': 0.3, 'arg3': 0.8}
    audience = Audience(assumptions, weights)
    caes = CAES(argset, audience, ps)
    caes.acceptable(murder)
    caes.acceptable(murder.negate())
