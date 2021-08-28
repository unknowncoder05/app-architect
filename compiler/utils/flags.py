SPECIAL_FIELD_FLAG = "__"
def is_flag(text:str):
    return text.startswith(SPECIAL_FIELD_FLAG)
def to_flag(text:str):
    return SPECIAL_FIELD_FLAG+text

MODELS_FIELD = "models"
SEVICES_FIELD = "services"

FLAG_EXTENDS = to_flag("extends")
FLAG_EXCLUDES = to_flag("excludes")
FLAG_INCLUDES = to_flag("includes")

FLAG_FROM = to_flag("from")


TAB = "\t"

ATTRIBUTE_FRAGMENT_TYPE = "type"
ATTRIBUTE_TYPE = "type"
ATTRIBUTE_DEFAULT = "default"

ATTRIBUTE_FUNCTION_NAME = "name"
ATTRIBUTE_FUNCTION_ARGS = "args"
ATTRIBUTE_FUNCTION_KWARGS = "kwargs"
ATTRIBUTE_FUNCTION_OUTPUTS = "outputs"
ATTRIBUTE_FUNCTION_CODE = "code"

ATTRIBUTE_FUNCTION_RETURN_ARGS = "args"


ATTRIBUTE_VARIABLE_NAME = "name"
ATTRIBUTE_VARIABLE_TYPE = "variable_type"
ATTRIBUTE_VARIABLE_EXPRESSION = "expression"
ATTRIBUTE_VARIABLE_ASSIGN_OPERATOR = "assign_operator"