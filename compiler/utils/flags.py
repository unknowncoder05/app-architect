MODELS_FIELD = "models"
SEVICES_FIELD = "services"
SPECIAL_FIELD_FLAG = "__"
def is_flag(text:str):
    return text.startswith(SPECIAL_FIELD_FLAG)
def to_flag(text:str):
    return SPECIAL_FIELD_FLAG+text

FLAG_EXTENDS = to_flag("extends")
FLAG_EXCLUDES = to_flag("excludes")
FLAG_INCLUDES = to_flag("includes")

FLAG_FROM = to_flag("from")



ATTRIBUTE_FRAGMENT_TYPE = "type"
ATTRIBUTE_TYPE = "type"

ATTRIBUTE_FUNCTION_NAME = "name"
ATTRIBUTE_FUNCTION_ARGS = "args"
ATTRIBUTE_FUNCTION_KWARGS = "kwargs"
ATTRIBUTE_FUNCTION_OUTPUTS = "outputs"
ATTRIBUTE_FUNCTION_CODE = "code"
