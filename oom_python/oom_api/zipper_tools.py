import os
import time
import hashlib
import shutil


class BadInputForZipper(Exception):
    pass


language_extensions = {
    "java": ".java",
    "c#": ".cs",
    "cs": ".cs",
    ".net": ".cs",
    "csharp": ".cs"
}


def validate(input_dictionary):
    print(input_dictionary)
    required_properties = ["entities", "language", "text"]
    for required_property in required_properties:
        if required_property not in input_dictionary:
            raise BadInputForZipper("The input does not contain the key " + required_property + ".")
    entities = input_dictionary["entities"]
    language = input_dictionary["language"]
    text = input_dictionary["text"]
    if type(entities) != dict:
        raise BadInputForZipper("The entities key doesn't have a dictionary as value.")
    if type(language) != str:
        raise BadInputForZipper("The language key doesn't have a string as value.")
    if language not in language_extensions:
        raise BadInputForZipper("The language " + language + " is not supported.")
    if type(text) != str:
        raise BadInputForZipper("The text key doesn't have a string as value.")
    if len(entities) < 1:
        raise BadInputForZipper("There is not entity in the entities dictionary.")

    for entity_name in entities:
        if type(entity_name) != str:
            raise BadInputForZipper("Entities does not contain just string keys.")
        if type(entities[entity_name]) != str:
            raise BadInputForZipper("Entities does not contain just string keys.")


def return_zip(input_dictionary):
    entities = input_dictionary["entities"]
    language = input_dictionary["language"]
    text = input_dictionary["text"]
    os.chdir("zips")

    directory_name = "GeneratedCode_" + hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()[:7]

    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)
    os.makedirs(directory_name)
    os.chdir(directory_name)

    original_text = open("originalText.txt", "w")
    original_text.write(text)
    original_text.close()

    for file_name in entities:
        current_file = open(file_name + language_extensions[language], "w")
        current_file.write(entities[file_name])
        current_file.close()

    os.chdir("..")

    shutil.make_archive(directory_name, 'zip', directory_name)

    shutil.rmtree(directory_name)

    os.chdir("..")

    return "http://localhost:2000/downloading/" + directory_name + ".zip"
