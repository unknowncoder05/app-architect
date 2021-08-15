import os

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict
from utils.CustomLogging import CustomLogging
from utils.flags import *

def compile_model(model_name:str, model_dict:dict, *, base_folder="", base_dict={}, object_route=""):
    print(model_name)
    if not model_name == "user":
        return
    args = {
        "model_name":model_name,
        "atributes":{
            "test1":"n1",
            "test2":"n2"
        }
    }
    model_template = load_json_as_dict("./django_compiler/templates/model.code.json")
    processed = special_flags_processing(model_template, args=args, base_folder=base_folder, base_dict=base_dict, object_route=object_route)
    print(processed)


class Compiler:
    blueprint: dict = {}

    def __init__(self, main_file) -> None:
        self.main_folder = os.path.dirname(main_file)
        self.main_file = main_file

        jcompiler = json_compiler(main_file)
        self.blueprint = jcompiler.compile()

    def compile_models(self, build):
        if MODELS_FIELD not in build:
            CustomLogging.error(f"{MODELS_FIELD} field is not defined")
        models = build[MODELS_FIELD]
        for model in models.copy():
            compile_model(model, models[model]["attributes"], base_folder=self.main_folder, base_dict=models[model], object_route=model)
        build[MODELS_FIELD] = models
        return build
    def compile_services(self, build):
        if SEVICES_FIELD not in build:
            CustomLogging.error(f"{SEVICES_FIELD} field is not defined")
        services = build[SEVICES_FIELD]
        for service in services.copy():
            print(service)
        build[SEVICES_FIELD] = services
        return build

    def compile(self):
        build = self.compile_models(self.blueprint)
        #build = self.compile_services(build)
        #print(build)
        return build
