from .Fragment import Fragment
from .FunctionCall import FunctionCall
from utils.flags import *
from python_compiler.utils.flags import *
from utils.CustomLogging import CustomLogging

def get_class_name(fragment) -> str:
    if not (class_name := fragment.get(ATTRIBUTE_CLASS_NAME)):
        CustomLogging.critical(f"Required Fragment type class 'name' attribute not defined")
    return class_name

def get_class_extends(fragment) -> dict:
    if not (class_extends := fragment.get(ATTRIBUTE_CLASS_EXTENDS)):
        class_extends = {}
    return class_extends

def get_class_attributes(fragment) -> dict:
    if not (class_attributes := fragment.get(ATTRIBUTE_CLASS_ATTRIBUTES)):
        class_attributes = {}
    return class_attributes

def get_class_code(fragment) -> list:
    if not (class_code := fragment.get(ATTRIBUTE_CLASS_CODE)):
        class_code = []
    return class_code

class Class(Fragment):
    name:str
    extends:dict
    attributes:dict
    code:dict
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__( blueprint, *args, **kwargs)
        self.name = get_class_name(blueprint)
        self.extends = get_class_extends(blueprint)
        self.attributes = get_class_attributes(blueprint)
        self.code = get_class_code(blueprint)
    def extends_compile(self) -> str:
        extends_build = ""
        if len(self.extends) > 0:
            extends_build = f"({', '.join(self.extends)})"
        return extends_build
    
    def get_attributes(self) -> list:
        lines = []
        for attr in self.attributes:
            self.attributes[attr]["type"] = "variable"
            fc = FunctionCall(self.attributes[attr], compile=self.general_compile)
            lines.append(
                attr+" = "+fc.compile()
            )
        return self.tabulate(lines, 1)
        
    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines.append(f"class {self.name}{self.extends_compile()}:")
        fragment_lines.extend(self.get_attributes())
        fragment_lines.extend(self.code_lines_compile(self.code))
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines
    
    def compile(self) -> str:
        fragment_build = "\n".join(self.get_lines())
        return fragment_build