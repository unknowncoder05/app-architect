import os
import json
from pathlib import Path

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict
from .engines.py3_8.Compiler import compile as py3_9_compiler
from utils.CustomLogging import CustomLogging


FLAG_ENGINE = "engine"
ENGINES = {
    "python3.8":py3_9_compiler
}
def compile_import_lines_generator(import_definition:dict, import_name:str) -> str:
    """Import definition like
    "compile":{
        "from":".engines.py3_8.Compiler",
        "as":"py3_9_compiler"
    }
    equals
    from .engines.py3_8.Compiler import compile as py3_9_compiler
    """
    from_statement = ""
    as_statement = ""
    if "from" in import_definition:
        from_statement = f"from {import_definition['from']} "
    if "as" in import_definition:
        as_statement = f" as {import_definition['as']}"
    return f"{from_statement}import {import_name}{as_statement}"

def compile_import_lines_generator(imports:list):
    for import_name in imports:
        yield compile_import_lines_generator(imports[import_name], import_name)

class Compiler:
    blueprint: dict = {}
    imports: dict = {}

    def __init__(self, *, save_folder:str="", main_file:str="", blueprint:dict={}) -> None:
        self.save_folder = Path(save_folder)
        if main_file:
            self.main_folder = os.path.dirname(main_file)
            self.main_file = main_file
            if not blueprint:
                raw_blueprint = load_json_as_dict(main_file)
                self.blueprint = special_flags_processing(raw_blueprint, base_folder=self.main_folder)
        if blueprint:
            self.blueprint = special_flags_processing(blueprint, base_folder=self.main_folder)
    
    def compile_imports(self) -> str:
        imports_build = ""
        for line in compile_import_lines_generator(self.models_imports):
            imports_build += line+"\n"
        return imports_build

    def compile_lines(self, *, save = False, imports=True) -> dict:
        pass

    def compile(self, *, save = False, imports=True) -> dict:
        build = ""
        if engine_type := self.blueprint.get(FLAG_ENGINE):
            if engine_compiler := ENGINES.get(engine_type):
                self.imports, build = engine_compiler(self.blueprint)
                if len(self.imports) != 0 and imports:
                    build = self.compile_imports()+"\n"*2+build
            else:
                CustomLogging.error(f"Compiler {engine_type} does not exists")
        else:
            CustomLogging.error(f"Flag {FLAG_ENGINE} not defined")
        file_path = str(self.save_folder / (self.blueprint.get("name","main")+".py"))
        if save:
            with open(file_path, "w") as f:
                f.write(build)
        files = {}
        files[file_path] = build
        return files
