import json
from searcher import search_json
MODELS_FIELD = "models"
EXTENDS_FIELD = "__extends"

class Compiler:
    blueprint:dict = {}
    def __init__(self, main_file) -> None:
        self.main_file = main_file
        with open(main_file, "r") as f:
            self.blueprint = json.load(f)
    def compile_models(self):
        if MODELS_FIELD not in self.blueprint and EXTENDS_FIELD not in self.blueprint:
            raise NameError("models is not defined")
        for model in self.blueprint["models"]:
            print(model)
            if type(model) == str:
                search_json(model, self.main_file)
    def compile(self):
        self.compile_models()