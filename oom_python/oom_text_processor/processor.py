"""In this file the flow is embedded via the process function"""

from oom_text_processor.tools import \
    text_to_sent_tokenized, sent_tokenized_to_no_punctuation, no_punctuation_to_word_tokenized, \
    word_tokenized_to_lemmatized_pos_terminals, lemmatized_pos_terminals_to_processed_text, \
    processed_text_to_schema, trim_schema


def process(text):
    """
    :param plain natural text:
    :return processed text:

    In here the whole flow is embedded, every processing operation
    In oom_text_processor/tools.py all the processing operations are defined and explained
    """
    # the grammar keywords are processed case sensitive so the text must be lowercase
    lowered_text = text.lower()
    # splitting the whole text in sentences, since
    # the idea of the grammar is to be able to process sentences by themselves
    sent_tokenized = text_to_sent_tokenized(lowered_text)
    # removing unnecessary punctuation from the text, of course, after the sentence splitting
    no_punctuation = sent_tokenized_to_no_punctuation(sent_tokenized)
    # splitting the sentences into words, preparing for part-of-speech recognition
    word_tokenized = no_punctuation_to_word_tokenized(no_punctuation)
    # lemmatizing and part-of-speech recognition, combined together
    # because part-of-speech is altered by lemmatizing
    lemmatized_pos_terminals = word_tokenized_to_lemmatized_pos_terminals(word_tokenized)
    # parsing the pre-processed text and converted into grammar-tagged json
    processed_text = lemmatized_pos_terminals_to_processed_text(lemmatized_pos_terminals)
    # converting into grammar-tagged json
    schema = processed_text_to_schema(processed_text)
    # trim the schema of unused entities and capitalize the first letters of a entity
    trimmed_schema = trim_schema(schema)
    # return schema
    return trimmed_schema
