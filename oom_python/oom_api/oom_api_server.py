import requests
import json
from bottle import run, route, request, response

server_utilities = {}
error_texts = {}


# defining the handler
@route('/oom', method='POST')
def modeling_handler():
    try:
        received = request.json
    except Exception as e:
        print(e)
        response.status = 401
        return error_texts['wrong_input_format']

    for required_field in server_utilities['required_fields']:
        if required_field not in received:
            response.status = 401
            return error_texts['required_field_missing'] % required_field

    received_text = received['text']
    received_language = received['language']

    if type(received_text) is not str or type(received_language) is not str:
        response.status = 401
        return error_texts['wrong_input_format']
    if received_language not in server_utilities['languages']:
        response.status = 401
        return error_texts['language_not_supported'] % received_language

    try:
        processor_response = requests.post(server_utilities['text_processor_uri'], data=received_text)
    except Exception as exception:
        print(exception)
        response.status = 500
        return error_texts['unhandled exception'] % "Text processor"
    else:
        if processor_response.status_code != 200:
            response.status = processor_response.status_code
            return processor_response.text

    try:
        generator_response = requests.post(server_utilities['languages'][received_language],
                                           json=processor_response.json())
    except Exception as exception:
        print(exception)
        response.status = 500
        return error_texts['unhandled exception'] % "Code generator"
    else:
        if generator_response.status_code != 200:
            response.status = generator_response.status_code
            return generator_response.text
    return generator_response.json()


def main():
    global server_utilities
    global error_texts
    with open('server_utilities.json') as server_utilities_json:
        server_utilities = json.load(server_utilities_json)
    error_texts = {
        'wrong_input_format': 'The format of the request is not processable',
        'required_field_missing': 'The %s field was not find in your request.',
        'language_not_supported': 'The language %s is not supported',
        'unhandled exception': 'Unhandled exception.[%s]'
    }
    if 'languages' not in server_utilities \
            or 'text_processor_uri' not in server_utilities \
            or 'required_fields' not in server_utilities:
        print('The server can not start with a invalid server_utilities.json')
    run(host='localhost', port='2000')


if __name__ == '__main__':
    main()
