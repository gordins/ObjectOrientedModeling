from nltk import pos_tag, Tree
from nltk.tokenize import sent_tokenize as sent_tokenizer, word_tokenize as word_tokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from string import punctuation
from oom_text_processor.grammar import grammar_parser, grammar_keywords
from oom_text_processor.schema_convertor.convertor import convert_processed_text

lemmatizer = WordNetLemmatizer()
punctuation_translator = str.maketrans('', '', punctuation.replace('\'', ''))
lemmatized = []

pos_list = ['C', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS',
            'PRP', 'PRPS', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT',
            'WP', 'WPS', 'WRB']

keywords = {"abstract", "as", "assert", "base", "bool", "boolean", "break", "byte", "case", "catch", "char", "checked",
            "class", "const", "continue", "decimal", "default", "delegate", "do", "double", "else", "enum", "event",
            "explicit", "extends", "extern", "false", "final", "finally", "fixed", "float", "for", "foreach", "goto",
            "if", "implements", "implicit", "import", "in", "instanceof", "int", "interface", "internal", "is", "lock",
            "long", "namespace", "native", "new", "null", "object", "operator", "out", "override", "package", "params",
            "private", "protected", "public", "readonly", "ref", "return", "sbyte", "sealed", "short", "sizeof",
            "stackalloc", "static", "strictfp", "string", "struct", "super", "switch", "synchronized", "this", "throw",
            "throws", "transient", "true", "try", "typeof", "uint", "ulong", "unchecked", "unsafe", "ushort", "using",
            "virtual", "void", "volatile", "while"}


def text_to_sent_tokenized(text):
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


def word_tokenized_to_word_tokenized_lower_cased(word_tokenized):
    word_tokenized_lower_cased = []
    original_words = []
    for sentence in word_tokenized:
        sentence_lower_cased = []
        for word in sentence:
            if word.lower() not in grammar_keywords:
                original_words.append(word)
            sentence_lower_cased.append(word.lower())

        word_tokenized_lower_cased.append(sentence_lower_cased)
    return word_tokenized_lower_cased, original_words


def pos_to_wordnet(pos):
    if pos.startswith('J'):
        return wordnet.ADJ
    if pos.startswith('V'):
        return wordnet.VERB
    if pos.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def word_tokenized_lower_cased_to_lemmatized_pos_terminals(word_tokenized_lower_cased):
    lemmatized_pos_terminals = []
    global lemmatized
    # the lemmatized are saved because the meaning of the word must be substituted back after grammar parsing
    lemmatized = []
    for word_tokenized_sent in word_tokenized_lower_cased:
        lemmatized_pos_terminals_sent = []
        lemmatized_sent = []
        pos_sent = pos_tag(word_tokenized_sent)
        for word_pos in pos_sent:
            lemmatized_word = lemmatizer.lemmatize(word_pos[0], pos_to_wordnet(word_pos[1]))
            lemmatized_sent.append(lemmatized_word)
            if lemmatized_word in grammar_keywords:
                lemmatized_pos_terminals_sent.append(lemmatized_word.lower())
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


def processed_text_to_schema(processed_text):
    entities = convert_processed_text(processed_text)
    valid_entities = []
    for entity in entities:
        if entity["name"] not in keywords:
            valid_entities.append(entity)
    return valid_entities


def trim_schema(schema, original_words):
    entity_counts = {}
    for i in range(0, len(schema)):
        schema[i]["name"] = find_actual_name(schema[i]["name"], original_words)
        entity_counts[schema[i]["name"]] = 0
    for i in range(0, len(schema)):
        if "inherits" in schema[i]:
            original_name = find_actual_name(schema[i]["inherits"], original_words)
            schema[i]["inherits"] = original_name
            entity_counts[original_name] += 1

        if "variables" in schema[i]:
            for j in range(0, len(schema[i]["variables"])):
                original_name = find_actual_name(schema[i]["variables"][j]["type"], original_words)
                if original_name in entity_counts:
                    schema[i]["variables"][j]["type"] = original_name
                    entity_counts[original_name] += 1
        if "methods" in schema[i]:
            for j in range(0, len(schema[i]["methods"])):
                if "returnType" in schema[i]["methods"][j]:
                    original_name = find_actual_name(schema[i]["methods"][j]["returnType"], original_words)
                    if original_name in entity_counts:
                        entity_counts[original_name] += 1
                        schema[i]["methods"][j]["returnType"] = original_name
                if "parameters" not in schema[i]["methods"][j]:
                    continue
                for k in range(0, len(schema[i]["methods"][j]["parameters"])):
                    original_name = find_actual_name(schema[i]["methods"][j]["parameters"][k]["type"], original_words)
                    if original_name in entity_counts:
                        entity_counts[original_name] += 1
                        schema[i]["methods"][j]["parameters"][k]["type"] = original_name
    trimmed_schema = []
    for entity in schema:
        if entity_counts[entity["name"]] == 0 and len(entity) <= 1:
            continue
        trimmed_schema.append(entity)
    return trimmed_schema


def find_actual_name(name, original_words):
    if name in keywords:
        return name
    for original_word in original_words:
        if original_word.lower() == name:
            return original_word[0].upper() + original_word[1:]
    return name.capitalize()
