ANY = "any"
PYTHON_TYPE_NAMES={
    ANY:False,
    "str":"str", #{"name":"str", "type":str}
    "int":"int",
    "bool":"bool",
    "list":"list",
    "tuple":"tuple",
    "dict":"dict",
    
}
def get_python_type_str(type_name:str) -> str:
    return PYTHON_TYPE_NAMES.get(type_name)