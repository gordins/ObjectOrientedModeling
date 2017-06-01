from nltk import pos_tag, Tree
from nltk.tokenize import sent_tokenize as sent_tokenizer, word_tokenize as word_tokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from string import punctuation
from oom_text_processor.grammar import grammar_parser, grammar_keywords

lemmatizer = WordNetLemmatizer()
punctuation_translator = str.maketrans('', '', punctuation)
lemmatized = []

pos_list = ['C', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS',
            'PRP', 'PRPS', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT',
            'WP', 'WPS', 'WRB']


def text_to_sent_tokenized(text):
    text.replace(' the ', ' ')
    return sent_tokenizer(text)


def sent_tokenized_to_no_punctuation(sent_tokenized):
    no_punctuation = []
    for sentence in sent_tokenized:
        no_punctuation.append(sentence.translate(punctuation_translator))
    return no_punctuation


def no_punctuation_to_word_tokenized(no_punctuation):
    word_tokenized = []
    for no_punctuation_sent in no_punctuation:
        word_tokenized.append(word_tokenizer(no_punctuation_sent))
    return word_tokenized


def pos_to_wordnet(pos):
    if pos.startswith('J'):
        return wordnet.ADJ
    if pos.startswith('V'):
        return wordnet.VERB
    if pos.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def word_tokenized_to_lemmatized_pos_terminals(word_tokenized):
    lemmatized_pos_terminals = []
    global lemmatized
    # the lemmatized are saved because the meaning of the word must be substituted back after grammar parsing
    lemmatized = []
    for word_tokenized_sent in word_tokenized:
        lemmatized_pos_terminals_sent = []
        lemmatized_sent = []
        pos_sent = pos_tag(word_tokenized_sent)
        for word_pos in pos_sent:
            lemmatized_word = lemmatizer.lemmatize(word_pos[0], pos_to_wordnet(word_pos[1]))
            lemmatized_sent.append(lemmatized_word)
            if lemmatized_word in grammar_keywords:
                lemmatized_pos_terminals_sent.append(lemmatized_word)
            else:
                lemmatized_pos_terminals_sent.append(word_pos[1])
        lemmatized.append(lemmatized_sent)
        lemmatized_pos_terminals.append(lemmatized_pos_terminals_sent)
    return lemmatized_pos_terminals


def tree_to_dict(tree, current_sentence_index, current_position_in_sentence=0):
    tree_dict = dict()
    for t in tree:
        if isinstance(t, Tree) and isinstance(t[0], Tree):
            tree_dict[t.label()], current_position_in_sentence = tree_to_dict(t, current_sentence_index,
                                                                              current_position_in_sentence)
        elif isinstance(t, Tree):
            if str(t[0]) in pos_list:
                tree_dict[t.label()] = lemmatized[current_sentence_index][current_position_in_sentence]
            else:
                tree_dict[t.label()] = str(t[0])
            current_position_in_sentence = current_position_in_sentence + 1
    return tree_dict, current_position_in_sentence


def lemmatized_pos_terminals_to_processed_text(lemmatized_pos_terminals):
    processed_text = []
    for i in range(0, len(lemmatized_pos_terminals)):
        processed_sentence_tree = grammar_parser.parse(lemmatized_pos_terminals[i])
        processed, last_index = tree_to_dict(processed_sentence_tree, i)
        processed_text.append(processed['sentence'])
    return processed_text
