from bottle import run, route, request, response
from oom_text_processor.processor import process
import json

# the uri where the processed text can get converted into a json-schema
# json-schema is modelled in oom_csharp
schema_generator_uri = 'http://localhost:4000/schemaGenerator'


# defining the handler
@route('/textProcessor', method='POST')
def text_preprocessor_handler():
    # there are several exceptions that can occur during the flow, more details on the Except field
    processed_text = ""
    try:
        text = request.body.read().decode('UTF-8')
        processed_text = process(text)
    except Exception as exception:
        print(exception)
        response.status = 400
        return 'The text to process can not be processed (Tokenizer).'
    return {"entities": processed_text}

if __name__ == '__main__':
    run(host='localhost', port='3000')
