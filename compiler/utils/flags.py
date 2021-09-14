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


TAB = ["\t", " "*4,"*"][1]
