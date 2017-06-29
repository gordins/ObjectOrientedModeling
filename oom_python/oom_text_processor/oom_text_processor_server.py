from bottle import run, route, request, response
from oom_text_processor.processor import process
from oom_text_processor import exceptions
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
        return {"entities": processed_text}
    except exceptions.TokenizeException as e:
        response.status = 412
        return e.ERROR_TEXT
    except exceptions.GrammarCanNotParseException as e:
        response.status = 412
        return e.ERROR_TEXT
    except exceptions.LemmatizeException as e:
        response.status = 412
        return e.ERROR_TEXT
    except Exception as exception:
        print(exception)
        response.status = 500
        return 'There was a unhandled exception during the processor flow.'


if __name__ == '__main__':
    run(host='0.0.0.0', port='3000')
