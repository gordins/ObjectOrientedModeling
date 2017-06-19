entities = []


def convert_processed_text(processed_text):
    global entities
    entities = []
    for sentence in processed_text:
        convert_sentence(sentence)
    return entities


def convert_sentence(sentence):
    if "descriptive" in sentence:
        convert_desc_sentence(sentence["descriptive"])
    elif "possessive" in sentence:
        convert_pos_sentence(sentence["possessive"])
    elif "behavioral" in sentence:
        convert_behav_sentence(sentence["behavioral"])
    elif "singleton" in sentence:
        convert_singleton_sentence(sentence["singleton"])


def convert_desc_sentence(desc_sentence):
    index_entity = add_entity(desc_sentence["entity"])
    if "abstract" in desc_sentence:
        entities[index_entity]["isAbstract"] = True
    elif "sealed" in desc_sentence:
        entities[index_entity]["isSealed"] = True
    elif "protected" in desc_sentence:
        entities[index_entity]["accessModifier"] = "protected"
    elif "inherited_entity" in desc_sentence:
        add_entity(desc_sentence["inherited_entity"]["entity"])
        entities[index_entity]["inherits"] = desc_sentence["inherited_entity"]["entity"]


def convert_pos_sentence(pos_sentence):
    if "defining_possessed" in pos_sentence:
        convert_defining_possessed_sentence(pos_sentence["defining_possessed"])
    elif "possessed_limitation" in pos_sentence:
        convert_possessed_limitation_sentence(pos_sentence["possessed_limitation"])
    elif "possessed_description" in pos_sentence:
        convert_possessed_description_sentence(pos_sentence["possessed_description"])


def convert_defining_possessed_sentence(defining_possessed_sentence):
    entity_index = add_entity(defining_possessed_sentence["entity"])
    variable_index = add_variable(entity_index, defining_possessed_sentence["possessed"]["pos_object"])
    if "private_indicator" in defining_possessed_sentence:
        entities[entity_index]["variables"][variable_index]["accessModifier"] = "private"
    if "numeral_indicator" in defining_possessed_sentence["possessed"]:
        if defining_possessed_sentence["possessed"]["numeral_indicator"] == "many":
            entities[entity_index]["variables"][variable_index]["isCollection"] = True


def convert_possessed_limitation_sentence(possessed_limitation_sentence):
    entity_index = add_entity(possessed_limitation_sentence["entity"])
    variable_index = add_variable(entity_index, possessed_limitation_sentence["possessed"]["pos_object"])
    if "protected" in possessed_limitation_sentence["limited_indicator"]:
        entities[entity_index]["variables"][variable_index]["accessModifier"] = "protected"
    if "private" in possessed_limitation_sentence["limited_indicator"]:
        entities[entity_index]["variables"][variable_index]["accessModifier"] = "private"


def convert_possessed_description_sentence(possessed_description_sentence):
    entity_index = add_entity(possessed_description_sentence["entity"])
    variable_index = add_variable(entity_index, possessed_description_sentence["possessed"]["pos_object"])
    if "constant" in possessed_description_sentence["description_type"]:
        entities[entity_index]["variables"][variable_index]["isConst"] = True
    if "static" in possessed_description_sentence["description_type"]:
        entities[entity_index]["variables"][variable_index]["isStatic"] = True
    if "entity" in possessed_description_sentence["description_type"]:
        add_entity(possessed_description_sentence["description_type"]["entity"])
        entities[entity_index]["variables"][variable_index]["type"] = \
            possessed_description_sentence["description_type"]["entity"]
        if "numeral_indicator" in possessed_description_sentence["description_type"]:
            entities[entity_index]["variables"][variable_index]["isCollection"] = \
                possessed_description_sentence["description_type"]["numeral_indicator"] != "a"


def convert_behav_sentence(behav_sentence):
    entity_index = add_entity(behav_sentence["entity"])
    method_index = add_method(entity_index, behav_sentence["behavior"]["behav_object"])
    if behav_sentence["behav_verb"] == "do" or behav_sentence["behav_verb"] == "can":
        entities[entity_index]["methods"][method_index]["accessModifier"] = "public"
    elif behav_sentence["behav_verb"] == "should" or behav_sentence["behav_verb"] == "may":
        entities[entity_index]["methods"][method_index]["accessModifier"] = "protected"
    if "private_indicator" in behav_sentence:
        entities[entity_index]["methods"][method_index]["accessModifier"] = "private"
    if "parameter_enumeration" in behav_sentence["behavior"]:
        convert_parameter_enumeration(behav_sentence["behavior"]["parameter_enumeration"],
                                      entity_index, method_index)


def convert_parameter_enumeration(parameter_enumeration, entity_index, method_index):
    parameter_index = add_parameter(entity_index, method_index, parameter_enumeration["parameter"]["entity"])
    add_entity(parameter_enumeration["parameter"]["entity"])
    if "numeral_indicator" in parameter_enumeration["parameter"]:
        entities[entity_index]["methods"][method_index]["parameters"][parameter_index]["isCollection"] = \
            parameter_enumeration["parameter"]["numeral_indicator"] != "a"
    if "parameter_enumeration" in parameter_enumeration:
        convert_parameter_enumeration(parameter_enumeration["parameter_enumeration"], entity_index, method_index)


def convert_singleton_sentence(singleton_sentence):
    entity_index = add_entity(singleton_sentence["entity"])
    variable_index = add_variable(entity_index, singleton_sentence["entity"])
    entities[entity_index]["variables"][variable_index]["name"] = "instance"
    entities[entity_index]["variables"][variable_index]["isStatic"] = True
    entities[entity_index]["variables"][variable_index]["accessModifier"] = "private"
    entities[entity_index]["constructors"] = []
    entities[entity_index]["constructors"].append({"accessModifier": "private"})
    method_index = add_method(entity_index, "getInstance")
    entities[entity_index]["methods"][method_index]["returnType"] = singleton_sentence["entity"]
    entities[entity_index]["methods"][method_index]["isStatic"] = True
    entities[entity_index]["methods"][method_index]["accessModifier"] = "public"


def does_element_exist(element_name, elements):
    for i in range(0, len(elements)):
        if elements[i]["name"] == element_name:
            return i
    return -1


def add_entity(entity_name):
    entity_index = does_element_exist(entity_name, entities)
    if entity_index == -1:
        entities.append({"name": entity_name})
        return len(entities) - 1
    return entity_index


def add_variable(entity_index, variable_name):
    if "variables" in entities[entity_index]:
        variable_index = does_element_exist(variable_name, entities[entity_index]["variables"])
    else:
        variable_index = -1
        entities[entity_index]["variables"] = []

    if variable_index == -1:
        entities[entity_index]["variables"].append({"name": variable_name, "type": variable_name})
        add_entity(variable_name)
        return len(entities[entity_index]["variables"]) - 1
    return variable_index


def add_method(entity_index, method_name):
    if "methods" in entities[entity_index]:
        method_index = does_element_exist(method_name, entities[entity_index]["methods"])
    else:
        method_index = -1
        entities[entity_index]["methods"] = []

    if method_index == -1:
        entities[entity_index]["methods"].append({"name": method_name})
        return len(entities[entity_index]["methods"]) - 1
    return method_index


def add_parameter(entity_index, method_index, parameter_name):
    if "parameters" in entities[entity_index]["methods"][method_index]:
        parameter_index = does_element_exist(parameter_name,
                                             entities[entity_index]["methods"][method_index]["parameters"])
    else:
        parameter_index = -1
        entities[entity_index]["methods"][method_index]["parameters"] = []

    if parameter_index == -1:
        entities[entity_index]["methods"][method_index]["parameters"].append(
            {"name": parameter_name, "type": parameter_name})
        add_entity(parameter_name)
        return len(entities[entity_index]["methods"][method_index]["parameters"]) - 1
    return parameter_index
