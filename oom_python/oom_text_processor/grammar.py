"""In this file the parser is created from a grammar. Currently available two grammars"""
import nltk
import re

# here is defined the default grammar
V1_GRAMMAR_PATH = 'grammars/grammar_v1.txt'
# the more detailed/expressive grammar
V2_GRAMMAR_PATH = 'grammars/grammar_v2.txt'

# selecting the file
grammar_picker = 2
if grammar_picker == 1:
    GRAMMAR_PATH = V1_GRAMMAR_PATH
else:
    GRAMMAR_PATH = V2_GRAMMAR_PATH

# getting the grammar in string form
grammar_string = open(GRAMMAR_PATH, 'r').read()

# creating the grammar
grammar_in_use = nltk.CFG.fromstring(grammar_string)

# creating the parser
grammar_parser = nltk.BottomUpChartParser(
    grammar_in_use)  # the bottom up chart parser provides better performances than the simple chart parser

# collecting the keywords from the grammar
grammar_keywords = set(re.findall(r'"(.*?)"', grammar_string))  # collecting the keywords from the grammar
