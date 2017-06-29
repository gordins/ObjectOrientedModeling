"""
Contains all the custom-defined exceptions that can occur in defined use-cases
"""
error_text_500 = '''There is a problem with the server flow.Please contact the developer at stefangordindev@gmail.com 
with the following error code: %(error_code)s
'''
error_text_412 = '''Your text is not processable. %s was not possible on your text.'''


class TokenizeException(Exception):
    ERROR_CODE = "10"
    ERROR_TEXT = error_text_412 % {"Tokenizing operation"}
    pass


class LemmatizeException(Exception):
    ERROR_CODE = "11"
    ERROR_TEXT = error_text_412 % {"Lemmatizing operation"}
    pass


class GrammarCanNotParseException(Exception):
    ERROR_CODE = "13"
    ERROR_TEXT = "Your text is not valid. It didn't pass the grammar-validation."
