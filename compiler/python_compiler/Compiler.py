import os
import json

from json_compiler.Compiler import Compiler as json_compiler, special_flags_processing, load_json_as_dict, object_route_join
from utils.CustomLogging import CustomLogging

class Compiler:
    blueprint: dict = {}

    def __init__(self, *, main_file:str = "", blueprint:dict = {}) -> None:
        if blueprint:
            self.blueprint = blueprint
        if main_file:
            if not blueprint:
                self.blueprint = load_json_as_dict(main_file)
            self.main_folder = os.path.dirname(main_file)
            self.main_file = main_file
            
    def compile(self):
        return
