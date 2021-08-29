import os
import json

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict
from .engines.py3_8.Compiler import compile as py3_9_compiler
from utils.CustomLogging import CustomLogging

FLAG_ENGINE = "engine"
ENGINES = {
    "python3.8":py3_9_compiler
}
class Compiler:
    blueprint: dict = {}

    def __init__(self, *, save_file, main_file:str = "", blueprint:dict = {}) -> None:
        self.save_file = save_file
        if main_file:
            self.main_folder = os.path.dirname(main_file)
            self.main_file = main_file
            if not blueprint:
                raw_blueprint = load_json_as_dict(main_file)
                self.blueprint = special_flags_processing(raw_blueprint, base_folder=self.main_folder)
        if blueprint:
            self.blueprint = special_flags_processing(blueprint, base_folder=self.main_folder)
            
    def compile(self, *, save = False) -> dict:
        build = ""
        if engine_type := self.blueprint.get(FLAG_ENGINE):
            if engine_compiler := ENGINES.get(engine_type):
                build = engine_compiler(self.blueprint)
            else:
                CustomLogging.error(f"Compiler {engine_type} does not exists")
        else:
            CustomLogging.error(f"Flag {FLAG_ENGINE} not defined")
        if save:
            with open(self.save_file, "w") as f:
                f.write(build)
        return build
