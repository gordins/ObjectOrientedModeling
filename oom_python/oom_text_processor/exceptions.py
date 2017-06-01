"""
Contains all the custom-defined exceptions that can occur in defined use-cases
"""
error_text_500 = '''There is a problem with the server flow.Please contact the developer at stefangordindev@gmail.com 
with the following error code: %(error_code)s
'''


class BadGrammarException(Exception):
    ERROR_CODE = "10"
    pass
