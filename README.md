# README

First and foremost, to be able to run this file, you need the CAES system python implementation, obviously. You also need to put the Reader.py file inside the 'carneades/src/carneades' folder.

This is a how you run the code. you don't need to pass an open file to the program, just the string containing the file's relative directory

```
>>> import Reader
>>> file_name = 'filename.txt'
>>> caes_obj = Reader.make_caes(file_name)
```

This will produce a graph.dot file, which you can turn into a viewable picture using the "$ dot -Tps graph.dot -o outfile.ps" command. That's it from a technical aspect. If you follow the following syntax instructions, you should be good to go! Any questions, can be directed at konstantinaras+caes@gmail.com.

The reasoning behind the following syntax had in mind the triangular relation that the user should have an easy time inputing the data, another person who might want to read the original file and understand the argument that took place and the programmer so that he can parse everything correctly.

## Some points that apply for the all the sections:

- Each different hing should be in ONE line
- Follow the syntax, otherwise the reader won't work
- If you make a problem, the program will output the line that you messed up
- If a propositional literal with two words then you shold replace the space with an underscore.(e.g. medical expert->medical_expert)

## How to split the different sections

Each section should start with a line that only has the name of the section in all capitals. e.g. PROPOSITIONS.(I'll have how you should start each section in brackets next to it)

## Propositions(PROPOSITIONS)

- Write the name of the proposition and keep it that way for the entire file
- If you want to give a negative proposition, put '-' in front of it
- Each line should contain only one proposition
- If a certain proposition requires a proof standard other than scintilla then you should indicate it by enclosing it in brackets next to the literal when you declare the literal. i.e. murder (preponderance)
- Possible values for proof standards: "preponderance", "clear_and_convincing", "beyond_reasonable_doubt", and "dialectical_validity".

## Arguments(('ARGUMENTS PROSECUTION' and 'ARGUMENTS DEFENCE'))


- start each argument with '#.' where # is each respective argument's number
- The actual argument should be structured in "so and so" claims/says that "this or that is true" because of "this or that", unless "this or that" i.e. The eye witness claims that there was intent because of "reasons" (the propLiteral that intent would depend on), but if
- if somebody in their argument claims that something is false, make sure to have the negation of the propLiteral as another Proposition on the top. i.e. if somebody claims intent is false you should write that in the arguments section as: x claims -intent.... and in the propositions you should have -intent as well as intent if somebody claims that intent is true
- Some arguments don't have somebody that makes the claim, i.e. the fact that murder depends on kill and intent. These can be expressed in the following way: "murder depends on intent and kill" that is, there is no need for somebody to claim or say it.

  - conclusion words: claims, says
  - premise words: depends, requires
  - exception words: voided, nullified

- Please have the argument written in this format: conclusion words "conclusion" premise words "premise" exception words "exceptions"

- the arguments for must come first and the arugments against second. They are two separate sections but share numbering, for example if there are 10 arguments for, then the first argument against will be number 11. This is because the weights are all in the same section continuously so as to not confuse the system

  ## Assumptions Weights

- This section should be 2 lines long, (assumptions, weights and the proposition we are trying to determine if true)

- If the audience(jury) has no assumptions, write "no assumptions"

- list the propositions that the audience assumes to be true, comma separated

- for the weights have the weights comma separated.

- The first value of the weights will correspond to the first argument and so on and so forth
- The value of each weight should be [0,1]. The decimal point should be a dot and not a comma.

### Example input

#### PROPOSITIONS

murder (beyond_reasonable_doubt)
intent
-intent
defendant
medical_expert
witness1
witness2
unreliable1
evidence
kill
lawyer1

#### ARGUMENTS PROSECUTION
1. the medical expert claims murder and it depends on the witness2 but can be voided if unreliable1  
2. lawyer1 claims murder depends on intent and kill  
3. witness1 claims intent and it depends on evidence  

#### ARGUMENTS DEFENCE  
4. the wintess2 claims -intent and it depends on unreliable1 but can be voided if witness1  
5. defendant claims -intent and it depends on wintess2  

#### ASSUMPTIONS AND WEIGHTS

evidence, kill 0.6, 0.5, 0.8 , 0.5, 0.5
