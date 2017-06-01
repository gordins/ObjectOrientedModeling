import requests
from bottle import run, route, request, response

text_processor_uri = 'http://localhost:3000/textProcessor'
code_generator_uri = 'http://localhost:4000/codeGenerator/'


@route('/moo', method='POST')
def modeling_handler():
    try:
        input_text = request.json['text']
        if request.json['language'] == 'java' or request.json['language'] == 'csharp' \
                or request.json['language'] == 'json':
            input_language = request.json['language']
        elif request.json['language'] == 'c#' or request.json['language'] == 'dotnet' \
                or request.json['language'] == '.net':
            input_language = 'csharp'
        else:
            response.status = 400
            return 'Language %s is not supported.' % (request.json['language'])
    except Exception as exception:
        print(exception)
        response.status = 400
        return 'Any request must contain "text" and "language" fields.'

    try:
        processor_response = requests.post(text_processor_uri, data=input_text)
    except Exception as exception:
        print(exception)
        response.status = 500
        return 'Unhandled exception.[Processing text]'
    else:
        if processor_response.status_code != 200:
            response.status = processor_response.status_code
            return processor_response.text
    try:
        # return processor_response.json()
        generator_response = requests.post(code_generator_uri + input_language,
                                           json=processor_response.json())
    except Exception as exception:
        print(exception)
        response.status = 500
        return 'Unhandled exception.[Generating code]'

    else:
        if generator_response.status_code != 200:
            response.status = generator_response.status_code
            return generator_response.text
    return generator_response.json()


if __name__ == '__main__':
    run(host='localhost', port='2000')
