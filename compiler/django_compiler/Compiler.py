import os
import json
from pathlib import Path

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict, object_route_join
from python_compiler.Compiler import Compiler as python_compiler
from utils.CustomLogging import CustomLogging
from utils.flags import *


CURRENT_PYTHON_ENGINE = "python3.8"
DJANGO_FIELD_TYPES = {
    "email":{
        "name":"CharField",
        "max":"max_length"
    },
    "id":{
        "name":"BigAutoField",
        "required":{
            "primary_key": True
        }
    },
    "str":{
        "name":"CharField",
        "max":"max_length"
    },
    "password":{
        "name":"CharField",
        "max":"max_length"
    },
    "email":{
        "name":"CharField",
        "max":"max_length"
    },
    "foreign":{
        "name":"ForeignKey",
        "required":{
            "on_delete": "models.CASCADE"
        }
    },
}

def compile_field(field_dict, model_names, *, base_folder="", object_route=""):
    #compiled = ""
    if field_dict["type"] == "id":
        #models.BigAutoField(primary_key=True)
        CustomLogging.log(f"skipping id since django already defines it")
        return
    field_type_name = field_dict['type']
    field_args = []
    if field_dict['type'] in model_names:
        field_type_name = "foreign"
        field_args = [field_dict['type']]
    field_type = DJANGO_FIELD_TYPES.get(field_type_name, False)
    
    if not field_type:
        CustomLogging.error(f"{object_route} {field_dict['type']} type is not defined")
    
    field_kwargs = {}
    if "max" in field_dict and "max" in field_type:
        field_kwargs[field_type["max"]] = field_dict["max"]
    field_call_definition = {
        "function":f"models.{field_type['name']}",
        "kwargs":field_kwargs,
        "args":field_args
    }
    #field_compiled_args = ", ".join([ f"{x}={field_args[x]}" for x in field_args])
    #compiled = f"models.{field_type['name']}({field_compiled_args})"
    return field_call_definition#compiled
def compile_model(model_name:str, model_dict:dict, model_names:list, *, base_folder="", base_dict={}, object_route=""):
    attributes = {}
    for field_name in model_dict:
        compiled_field = compile_field(model_dict[field_name], model_names, base_folder=base_folder, object_route=object_route_join(object_route, field_name))
        if compiled_field:
            attributes[field_name] = compiled_field
    args = {
        "model_name":model_name.title(),
        "attributes": attributes,
        "desc":"__model_name model class" # recursive constructor
    }
    dir = Path(os.path.dirname(__file__))
    model_path = dir / "templates" / "model.code.json"
    model_template = load_json_as_dict(model_path)
    processed = special_flags_processing(model_template, args=args, base_folder=base_folder, base_dict=base_dict, object_route=object_route)
    return processed


class Compiler:
    blueprint: dict = {}

    def __init__(self, *, main_file, save_folder) -> None:
        self.main_folder = Path(os.path.dirname(main_file))
        self.main_file = Path(main_file)
        self.save_folder = Path(save_folder)

        jcompiler = json_compiler(main_file=main_file, save_folder="temp")
        self.blueprint = jcompiler.compile()["temp"]

    def compile_models_to_json(self, build:dict) -> dict:
        if MODELS_FIELD not in build:
            CustomLogging.error(f"{MODELS_FIELD} field is not defined")
        models = build[MODELS_FIELD]
        self.model_names = list(models.keys())
        for model in models.copy():
            compiled_model = compile_model(model, models[model]["attributes"], self.model_names, base_folder=self.main_folder, base_dict=models[model], object_route=model)
            models[model] = compiled_model
        return models
    def compile_model_lines(self, build:dict) -> str:
        model_json_build = self.compile_models_to_json(build)
        model_build = ""
        for model in model_json_build:
            model_python_compiler = python_compiler(main_file=self.main_file, blueprint=model_json_build[model])
            model_code = model_python_compiler.compile()
            model_build += model_code[list(model_code.keys())[0]]
            model_build += "\n"*2
        return model_build
    def compile_services(self, build:dict) -> dict:
        if SEVICES_FIELD not in build:
            CustomLogging.error(f"{SEVICES_FIELD} field is not defined")
        services = build[SEVICES_FIELD]
        for service in services.copy():
            print(service)
        build[SEVICES_FIELD] = services
        return build

    def compile(self, *, save:bool=False) -> dict:
        model_build = self.compile_model_lines(self.blueprint)
        #build = self.compile_services(build)
        files = {}
        files[str(self.save_folder/"models.py")] = model_build
        print(model_build)
        return files
