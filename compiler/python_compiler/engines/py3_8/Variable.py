from .Fragment import Fragment
from utils.flags import *
from python_compiler.utils.flags import *
from utils.CustomLogging import CustomLogging
#from python_compiler.engines.utils.types import get_python_type_str, ANY


DEFAULT_ASSIGN_OPERATOR = "="
ASSIGN_OPERATORS = {
    "=":"=",
    "+=":"+=",
    "-=":"-=",
    "*=":"*=",
    "/=":"/=",
    "//=":"//=",
    "%=":"%=",
    "**=":"**=",
    "&=":"&=",
    "|=":"|=",
    "^=":"^=",
    ">>=":">>=",
    "<<=":"<<=",
}

def get_variable_name(fragment) -> str:
    if not (variable_name := fragment.get(ATTRIBUTE_VARIABLE_NAME)):
        CustomLogging.critical(f"Required Fragment type variable '{ATTRIBUTE_VARIABLE_NAME}' attribute does not exist")
    return variable_name

def get_variable_type(fragment) -> str:
    if not (variable_type := fragment.get(ATTRIBUTE_VARIABLE_TYPE)):
        variable_type = ""
    else:
        variable_type = ":"+variable_type
    return variable_type

def get_variable_assign_operator(fragment) -> str:
    if not (variable_assign_operator := fragment.get(ATTRIBUTE_VARIABLE_ASSIGN_OPERATOR)):
        variable_assign_operator = DEFAULT_ASSIGN_OPERATOR
    return ASSIGN_OPERATORS.get(variable_assign_operator)

def get_variable_expression(fragment) -> str:
    if not (variable_expression := fragment.get(ATTRIBUTE_VARIABLE_EXPRESSION)):
        CustomLogging.critical(f"Required Fragment type variable '{ATTRIBUTE_VARIABLE_EXPRESSION}' attribute does not exist")
    return variable_expression


class Variable(Fragment):
    name:str
    variable_type:str
    assign_operator:str
    expression:str
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__(blueprint, *args, **kwargs)
        self.name = get_variable_name(blueprint)
        self.variable_type = get_variable_type(blueprint)
        self.assign_operator = get_variable_assign_operator(blueprint)
        self.expression = get_variable_expression(blueprint)
    
    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines.append(f"{self.name}{self.variable_type} {self.assign_operator} {self.expression}")
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines
    
    def compile(self) -> str:
        
        fragment_build = "\n".join(self.get_lines())
        return fragment_build