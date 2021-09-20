import os
import json
from pathlib import Path

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict, object_route_join
from python_compiler.Compiler import Compiler as python_compiler, compile_import_lines_generator
from utils.CustomLogging import CustomLogging
from utils.flags import *
from python_compiler.utils.flags import *


CURRENT_PYTHON_ENGINE = "python3.8"
DJANGO_FIELD_TYPES = {
    "email":{
        "name":"EmailField",
        "kwargs":{
            "max": {
                "required":True,
                "name":"max_length"
            }
        }
    },
    "bool":{
        "name":"BooleanField",
        "kwargs":{
            "default": {
                "name":"default"
            }
        }
    },
    "id":{
        "name":"BigAutoField",
        "kwargs":{
            "primary_key": {
                "user_input":False,  # automatically added kwarg
                "default":True,
                "name":"primary_key"
            }
        }
    },
    "str":{
        "name":"CharField",
        "kwargs":{
            "max": {
                "required":True,
                "name":"max_length"
            }
        }
    },
    "password":{
        "name":"CharField",
        "kwargs":{
            "widget": {
                "user_input":False,  # automatically added kwarg
                "default":"forms.PasswordInput",
                "name":"widget",
                "imports":{
                    "forms":{
                        "from":"django"
                    }
                }
            }
        }
    },
    "email":{
        "name":"EmailField",
        "kwargs":{
            "max": {
                "required":True,
                "name":"max_length"
            },
            "unique":{
                "name":"unique",
                "default":True
            }
        }
    },
    "foreign":{
        "name":"ForeignKey",
        "kwargs":{
            "on_delete": {
                "name":"on_delete",
                "default":"models.CASCADE"
            }
        }
    },
    "datetime":{
        "name":"DateTimeField",
        "kwargs":{
            "on_create":{
                "name":"auto_now_add"
            },
            "on_update":{
                "name":"auto_now"
            }
        }
    }
}

def compile_field(field_dict:dict, model_names:list, *, base_folder="", object_route=""):
    #compiled = ""
    if not (field_type_name := field_dict.get("type")):
        #models.BigAutoField(primary_key=True)
        CustomLogging.error(f"model field {object_route} has no type defined")
        return
    if field_type_name == "id":
        #models.BigAutoField(primary_key=True)
        CustomLogging.log(f"skipping id from model {object_route} since django already defines it")
        return
    field_args = []
    if field_type_name in model_names:
        field_type_name = "foreign"
        field_args = [field_dict["type"].title()] # TODO: load name from compiler, not just generate it
    
    
    if not (field_type := DJANGO_FIELD_TYPES.get(field_type_name, False)):
        CustomLogging.error(f"{object_route} {field_type_name} type is not defined")
        return
    
    field_kwargs = {}
    for kwarg in field_type["kwargs"]:
        kwarg_definition = field_type["kwargs"][kwarg]
        if not kwarg_definition.get("user_input", True):
            field_kwargs[kwarg_definition["name"]] = kwarg_definition["default"]
            continue

        if kwarg_definition.get("required", False) and kwarg not in field_dict:
            CustomLogging.error(f"{object_route} {kwarg} argument is required")
            continue
        
        if "default" in kwarg_definition and kwarg not in field_dict:
            field_kwargs[kwarg_definition["name"]] = kwarg_definition["default"]
            continue
        if kwarg in field_dict:
            field_kwargs[kwarg_definition["name"]] = field_dict[kwarg]
    # TODO: add args and import handling
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
        # TODO: add field grouping argument and order argument
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
    models_imports: dict = {}

    def __init__(self, *, main_file, save_folder) -> None:
        self.main_folder = Path(os.path.dirname(main_file))
        self.main_file = Path(main_file)
        self.save_folder = Path(save_folder)

        jcompiler = json_compiler(main_file=main_file)
        self.blueprint = jcompiler.compile()["file"]

    def compile_models_to_json(self) -> dict:
        if MODELS_FIELD not in self.blueprint:
            CustomLogging.error(f"{MODELS_FIELD} field is not defined")
        models = self.blueprint[MODELS_FIELD]
        self.model_names = list(models.keys())
        for model in models.copy():
            compiled_model = compile_model(model, models[model]["attributes"], self.model_names, base_folder=self.main_folder, base_dict=models[model], object_route=model)
            models[model] = compiled_model
        return models

    def compile_models(self) -> list:
        model_json_build = self.compile_models_to_json()
        model_build = ""
        for model in model_json_build:
            model_python_compiler = python_compiler(main_file=self.main_file, blueprint=model_json_build[model])
            model_code = model_python_compiler.compile(imports=False)
            self.models_imports.update(model_python_compiler.imports)
            page = model_code[list(model_code.keys())[0]]
            model_build += page
            model_build += "\n"*2
        return model_build
    
    def compile_import_lines(self):
        for import_name in self.models_imports:
            from_statement = ""
            as_statement = ""
            import_definition = self.models_imports[import_name]
            if ATTRIBUTE_IMPORT_FROM in import_definition:
                from_statement = f"from {import_definition[ATTRIBUTE_IMPORT_FROM]} "
            if ATTRIBUTE_IMPORT_AS in import_definition:
                as_statement = f" as {import_definition[ATTRIBUTE_IMPORT_AS]}"
            yield f"{from_statement}import {import_name}{as_statement}"
    
    def compile_imports(self):
        imports_build = ""
        for line in self.compile_import_lines():
            imports_build += line+"\n"
        return imports_build
    def compile_services(self, build:dict) -> dict:
        if SEVICES_FIELD not in build:
            CustomLogging.error(f"{SEVICES_FIELD} field is not defined")
        services = build[SEVICES_FIELD]
        for service in services.copy():
            print(service)
        build[SEVICES_FIELD] = services
        return build

    def compile(self, *, save:bool=False) -> dict:
        model_build = self.compile_models()
        model_imports_build = self.compile_imports()
        #build = self.compile_services(build)
        files = {}
        model_page = model_imports_build+"\n"*2+model_build
        files[str(self.save_folder/"models.py")] = model_page
        print(model_page)
        return files
