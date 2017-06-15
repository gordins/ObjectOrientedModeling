from oom_text_processor import tools, grammar

# lowered_text = "Stefan's car is a Dacia".lower()
lowered_text = "Stefan is abstract. Stefan has no heir. " \
               "Not everyone knows Stefan. " \
               "Stefan is a human. " \
               "Stefan has car. " \
               "Stefan has a car. " \
               "Stefan has many cars. " \
               "Only Stefan has car. " \
               "Only Stefan has a car. " \
               "Only Stefan has many cars. " \
               "Not everyone knows Stefan's car. " \
               "No one knows Stefan's car. " \
               "Stefan's car is a Dacia. " \
               "Stefan's car is unchangeable. " \
               "Stefan's car is shareable. " \
               "Stefan can swim. " \
               "Stefan can swim with a duck. " \
               "Only Stefan can run with Crocodile. " \
               "Only Stefan can study with a person and many birds. " \
               "There is only one Stefan.".lower()
sent_tokenized = tools.text_to_sent_tokenized(lowered_text)
# removing unnecessary punctuation from the text, of course, after the sentence splitting
no_punctuation = tools.sent_tokenized_to_no_punctuation(sent_tokenized)
word_tokenized = tools.no_punctuation_to_word_tokenized(no_punctuation)
# lemmatizing and part-of-speech recognition, combined together
# because part-of-speech is altered by lemmatizing
lemmatized_pos_terminals = tools.word_tokenized_to_lemmatized_pos_terminals(word_tokenized)
# finally, parsing the pre-processed text and converted into grammar-tagged json
processed_text = tools.lemmatized_pos_terminals_to_processed_text(lemmatized_pos_terminals)
print(processed_text)

# test = ['NNP', 'POS', 'NN', 'be', 'a', 'NN']
# for tree in grammar.grammar_parser.parse(test):
#     print(tree)
