import json
import os
import pprint
from utils.searcher import search_json
MODELS_FIELD = "models"
SPECIAL_FIELD_FLAG = "__"
EXTENDS_FIELD = SPECIAL_FIELD_FLAG+"extends"


def load_json_as_dict(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def json_global_compile(json_dict, args = {}, *, main_file=""):
    data = json_dict.copy()
    for attr in json_dict:
        if type(attr) == dict:
            sub_data = json_global_compile(json_dict[attr])
        if not attr.startswith(SPECIAL_FIELD_FLAG):
            continue
        if attr == SPECIAL_FIELD_FLAG+"constructor":
            print("Constructing!")
            data.pop(SPECIAL_FIELD_FLAG+"constructor")
        elif attr == SPECIAL_FIELD_FLAG+"extends":
            print("Recursive extends!")
            file_name = search_json(data[SPECIAL_FIELD_FLAG+"extends"]["from"], os.path.dirname(main_file))
            if file_name == None:
                print("ERROR!", main_file, "path does not exists")
                return
            attr_json = load_json_as_dict(file_name)
            attr_buid = json_global_compile(attr_json, data[SPECIAL_FIELD_FLAG+"extends"])
            data.pop(SPECIAL_FIELD_FLAG+"extends")
            data.update(attr_buid)
            #sub_data = json_global_compile(json_dict[attr])
    return data

class Compiler:
    blueprint: dict = {}

    def __init__(self, main_file) -> None:
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
                    build["models"][model], self.main_file)
                if model_file_name == None:
                    print(
                        "ERROR!", build["models"][model], "path does not exists")
                    continue
                model_json = load_json_as_dict(model_file_name)
            elif type(model) == dict:
                model_json = model
            model_build = json_global_compile(model_json, main_file = model_file_name)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(model_build)

    def compile(self):
        self.compile_models()
