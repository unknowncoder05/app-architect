import json
from utils.searcher import search_json
MODELS_FIELD = "models"
SPECIAL_FIELD_FLAG="__"
EXTENDS_FIELD = SPECIAL_FIELD_FLAG+"extends"


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
            if model.startswith(SPECIAL_FIELD_FLAG):
                if model == "__extends":
                    print("extends!")
                    # Extend
                continue
            if type(model) == str:
                print("model", search_json(self.blueprint["models"][model], self.main_file))
    def compile(self):
        self.compile_models()