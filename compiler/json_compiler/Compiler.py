import json
import os
import pprint
import copy
from utils.searcher import search_json
from utils.CustomLogging import CustomLogging

MODELS_FIELD = "models"
SPECIAL_FIELD_FLAG = "__"
EXTENDS_FIELD = SPECIAL_FIELD_FLAG+"extends"

def set_type(object, to_type):
    # TODO: implement type serialization
    return object
def load_json_as_dict(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
def extends(json_dict, *, base_folder=None, base_dict={}, object_route=""):
    extends_from = json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"from"].split(".")
    attr_build = {}
    if len(extends_from) == 1:
        new_route = ".".join(object_route.split(".")+[extends_from[0]])
        if extends_from[0] in base_dict:
            attr_build = special_flags_processing(base_dict[extends_from[0]], base_dict=base_dict, object_route = new_route)
        else:
            CustomLogging.error(f"Attribute {extends_from[0]} not found \n{base_dict}")
    else:
        attr_file_name = search_json(json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"from"], base_folder=base_folder)
        if not attr_file_name:
            CustomLogging.error(f"{json_dict[SPECIAL_FIELD_FLAG+'extends'][SPECIAL_FIELD_FLAG+'from']} path does not exists in")
        attr_json = load_json_as_dict(attr_file_name)
        attr_build = json_global_compile(
            attr_json,
            args = json_dict[SPECIAL_FIELD_FLAG+"extends"],
            base_folder = os.path.dirname(attr_file_name),
            object_route=json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"from"]
        )
    is_excluding = SPECIAL_FIELD_FLAG+"excludes" in json_dict[SPECIAL_FIELD_FLAG+"extends"]
    is_including = SPECIAL_FIELD_FLAG+"includes" in json_dict[SPECIAL_FIELD_FLAG+"extends"]
    if is_including and is_excluding:
        CustomLogging.error("can not use excludes and includes in a same block")
    if is_including:
        new_attr_build = {}
        for include in json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"includes"]:
            if include not in attr_build:
                CustomLogging.error(f"{object_route} include error: attribute {include} not in {json_dict[SPECIAL_FIELD_FLAG+'extends'][SPECIAL_FIELD_FLAG+'from']}")
            new_attr_build[include] = attr_build[include]
        attr_build = new_attr_build
    if is_excluding:
        for exclude in json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"excludes"]:
            if exclude in attr_build:
                attr_build.pop(exclude)
            else:
                CustomLogging.warning(f"exclude error: attribute {exclude} not in {json_dict[SPECIAL_FIELD_FLAG+'extends'][SPECIAL_FIELD_FLAG+'from']}")
    json_dict.update(attr_build)
    json_dict.pop(SPECIAL_FIELD_FLAG+"extends")
    return json_dict
def cosntruct_replace(main_object, arg_replace, value):
    if type(main_object) == str:
        return main_object.replace(arg_replace, value)
    response_json = {}
    for attribute in main_object:
        attribute_new_name = attribute.replace(arg_replace, value)
        attribute_new_value = main_object[attribute]
        if type(attribute_new_value) == dict:
            attribute_new_value = cosntruct_replace(attribute_new_value, arg_replace, value)
        elif type(attribute_new_value) == list:
            attribute_new_value = [ cosntruct_replace(element, arg_replace, value) for element in attribute_new_value ]
        response_json[attribute_new_name] = attribute_new_value
    return response_json
def cosntructor(json_dict, *, args = {}, object_route=""):
    constructor_dict = json_dict.pop(SPECIAL_FIELD_FLAG+"constructor")
    response_json = copy.deepcopy(json_dict)
    args_to_check = copy.deepcopy(args)
    args_to_check.pop(SPECIAL_FIELD_FLAG+"from")
    if SPECIAL_FIELD_FLAG+"excludes" in args_to_check:
        args_to_check.pop(SPECIAL_FIELD_FLAG+"excludes")
    if SPECIAL_FIELD_FLAG+"includes" in args_to_check:
        args_to_check.pop(SPECIAL_FIELD_FLAG+"includes")
    for arg_to_check in args_to_check:
        if arg_to_check not in constructor_dict:
            CustomLogging.warning(f"error in constructor: invalid parameter {arg_to_check}")
        else:
            constructor_dict.pop(arg_to_check) # remove argument so we know it already was defined
    for default_attribute in constructor_dict:
        if default_attribute.startswith(SPECIAL_FIELD_FLAG):
            continue
        args_to_check[default_attribute] = set_type(constructor_dict[default_attribute]["default"], constructor_dict[default_attribute]["type"])
    for arg in args_to_check:
        new_value = cosntruct_replace(response_json, SPECIAL_FIELD_FLAG+arg, args_to_check[arg])
        response_json = new_value
    return response_json
def special_flags_processing(json_dict, *, args = {}, base_folder=None, base_dict={}, object_route=""):
    if SPECIAL_FIELD_FLAG+"constructor" in json_dict:
        json_dict = cosntructor(json_dict, args=args)
        base_dict = copy.deepcopy(json_dict)
    if SPECIAL_FIELD_FLAG+"extends" in json_dict:
        json_dict = extends(json_dict, base_folder=base_folder, base_dict=base_dict, object_route=object_route)
    for attribute in json_dict:
        if type(json_dict[attribute]) == dict:
            json_dict[attribute] = special_flags_processing(json_dict[attribute], args=args, base_folder=base_folder, base_dict=base_dict, object_route=f"{object_route}.{attribute}")
    return copy.deepcopy(json_dict)

def json_global_compile(json_dict, *, args = {}, base_folder=None, base_dict={}, object_route= ""):
    data = special_flags_processing(json_dict, args=args, base_folder=base_folder, base_dict=json_dict, object_route=object_route)
    return data
class Compiler:
    blueprint: dict = {}

    def __init__(self, main_file) -> None:
        self.main_folder = os.path.dirname(main_file)
        self.main_file = main_file
        self.blueprint = load_json_as_dict(main_file)

    def compile_models(self):
        if MODELS_FIELD not in self.blueprint and EXTENDS_FIELD not in self.blueprint:
            CustomLogging.error("models is not defined")
        build = json_global_compile(self.blueprint, base_folder=self.main_folder)
        for model in build["models"].copy():
            model_file_name = self.main_file
            if type(build["models"][model]) == str:
                model_file_name = search_json(
                    build["models"][model], base_folder=self.main_folder)
                if not model_file_name:
                    CustomLogging.error(build["models"][model], "path does not exists in")
                    continue
                model_json = load_json_as_dict(model_file_name)
            elif type(build["models"][model]) == dict:
                model_json = build["models"][model]
            else:
                CustomLogging.error(f"invalid model {model}")
            model_build = json_global_compile(model_json, base_folder = os.path.dirname(model_file_name), object_route=model)
            build["models"][model] = model_build
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(build)

    def compile(self):
        self.compile_models()
