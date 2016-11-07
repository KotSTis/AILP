# README
 The reasoning behind the following syntax had in mind the triangular relation that the user should have an easy time inputing the data, another person who might want to read the original file and understand the argument that took place and the programmer so that he can parse everything correctly.


## Some points that apply for the all the sections:
 - Each different hing should be in ONE line
 - Follow the syntax, otherwise the reader won't work
 - If you make a problem, the program will output the line that you messed up
 - If a propositional literal with two words then you shold replace the space
    with an underscore.(e.g. medical expert->medical_expert)

### How to split the different sections
Each section should start with a line that only has the name of the section in all capitals.
e.g. PROPOSITIONS.(I'll have how you should start each section in brackets next to it)

### Propositions(PROPOSITIONS)
 - Write the name of the proposition and keep it that way for the entire file
 - If you want to give a negative proposition, put '-' in front of it
 - Each line should contain only one proposition
 - If a certain proposition requires a proof standard other than scintilla then
    you should indicate it by typing it like this when you declare the literal.
    i.e. murder - preponderance
 - Possible values for proof standards: "preponderance", "clear_and_convincing",
    "beyond_reasonable_doubt", and "dialectical_validity".

### Arguments(ARGUMENTS)

 - start each argument with '#.' where # is each respective argument's number
 - The actual argument should be structured in "so and so" claims/says that
    "this or that is true" because of "this or that", unless "this or that"
 i.e. The eye witness claims that there was intent because of "reasons" (the propLiteral that intent would depend on), but if h
 - if somebody in their argument claims that something is false, indicate that
    with saying claims not_propLiteral, the program automatically creates the
    negation


### Assumptions and weights(ASSUMPTIONS AND WEIGHTS)


### Example input

PROPOSITIONS
murder - beyond_reasonable_doubt
intent
defendant
medical expert
witness1
witness2

ARGUMENTS

1. the medical expert claims murder and it depends on the witness1 but can be voided if unreliable1
2. the wintess2 claims not_intent and it depends on unreliable1 but can be voided if witness1

ASSUMPTIONS AND WEIGHTS
