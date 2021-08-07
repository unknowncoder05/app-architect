import json
import os
import pprint
import copy
from utils.searcher import search_json
from utils.CustomLogin import CustomLogin

MODELS_FIELD = "models"
SPECIAL_FIELD_FLAG = "__"
EXTENDS_FIELD = SPECIAL_FIELD_FLAG+"extends"


def load_json_as_dict(file_name):
    with open(file_name, "r") as f:
        return json.load(f)
def special_flags_processing(json_dict, args = {}, *, base_folder=None, base_dict={}, object_route=""):
    if SPECIAL_FIELD_FLAG+"constructor" in json_dict:
        json_dict.pop(SPECIAL_FIELD_FLAG+"constructor")
    if SPECIAL_FIELD_FLAG+"extends" in json_dict:
        extends_from = json_dict[SPECIAL_FIELD_FLAG+"extends"]["from"].split(".")
        attr_build = {}
        if len(extends_from) == 1:
            if extends_from[0] in base_dict:
                attr_build = special_flags_processing(base_dict[extends_from[0]], base_dict=base_dict, object_route = object_route+"."+extends_from[0])
            else:
                CustomLogin.error(f"ERROR: Attribute not found {object_route}.{extends_from[0]}\n{base_dict}")
        else:
            attr_file_name = search_json(json_dict[SPECIAL_FIELD_FLAG+"extends"]["from"], base_folder=base_folder)
            if not attr_file_name:
                CustomLogin.error(f"ERROR! {json_dict[SPECIAL_FIELD_FLAG+'extends']['from']} path does not exists in")
            attr_json = load_json_as_dict(attr_file_name)
            attr_build = json_global_compile(attr_json, base_folder = os.path.dirname(attr_file_name),object_route=json_dict[SPECIAL_FIELD_FLAG+"extends"]["from"])
        is_excluding = SPECIAL_FIELD_FLAG+"excludes" in json_dict[SPECIAL_FIELD_FLAG+"extends"]
        is_including = SPECIAL_FIELD_FLAG+"includes" in json_dict[SPECIAL_FIELD_FLAG+"extends"]
        if is_including and is_excluding:
            CustomLogin.error("can not use excludes and includes in a same block")
        if is_including:
            new_attr_build = {}
            for include in json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"includes"]:
                if include not in attr_build:
                    raise NameError(f"include error: attribute {include} not in {json_dict[SPECIAL_FIELD_FLAG+'extends']['from']}")
                new_attr_build[include] = attr_build[include]
            attr_build = new_attr_build
        if is_excluding:
            for exclude in json_dict[SPECIAL_FIELD_FLAG+"extends"][SPECIAL_FIELD_FLAG+"excludes"]:
                if exclude in attr_build:
                    attr_build.pop(exclude)
                else:
                    CustomLogin.warning(f"exclude error: attribute {exclude} not in {json_dict[SPECIAL_FIELD_FLAG+'extends']['from']}")
        json_dict.update(attr_build)
        json_dict.pop(SPECIAL_FIELD_FLAG+"extends")
    for attribute in json_dict:
        if type(json_dict[attribute]) == dict:
            json_dict[attribute] = special_flags_processing(json_dict[attribute], args, base_folder=base_folder, base_dict=base_dict, object_route=f"{object_route}.{attribute}")
    return copy.deepcopy(json_dict)

def json_global_compile(json_dict, args = {}, *, base_folder=None, base_dict={}, object_route= ""):
    data = special_flags_processing(json_dict, args, base_folder=base_folder, base_dict=json_dict, object_route=object_route)
    return data
class Compiler:
    blueprint: dict = {}

    def __init__(self, main_file) -> None:
        self.main_folder = os.path.dirname(main_file)
        self.main_file = main_file
        self.blueprint = load_json_as_dict(main_file)

    def compile_models(self):
        if MODELS_FIELD not in self.blueprint and EXTENDS_FIELD not in self.blueprint:
            raise NameError("models is not defined")
        build = json_global_compile(self.blueprint)
        for model in build["models"].copy():
            model_file_name = self.main_file
            if type(model) == str:
                model_file_name = search_json(
                    build["models"][model], base_folder=self.main_folder)
                if not model_file_name:
                    print(
                        "ERROR!", build["models"][model], "path does not exists in")
                    continue
                model_json = load_json_as_dict(model_file_name)
            elif type(model) == dict:
                model_json = model
            model_build = json_global_compile(model_json, base_folder = os.path.dirname(model_file_name), object_route=model)
            build["models"][model] = model_build
        pp = pprint.PrettyPrinter(indent=2)
        pp.pprint(build)

    def compile(self):
        self.compile_models()
