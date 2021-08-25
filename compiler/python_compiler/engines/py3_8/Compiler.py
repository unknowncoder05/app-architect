from utils.CustomLogging import CustomLogging
FLAG_FRAGMENT_TYPE = "type"
FRAGMENT_TYPES={
    "function":print,
    "class":print,
    "variable":print,
    "conditional":print
}
def compile(blueprint:dict):
    build = {}
    if fragment_type := blueprint.get(FLAG_FRAGMENT_TYPE):
        if fragment_compiler := FRAGMENT_TYPES[fragment_type]:
            build = fragment_compiler(blueprint)
        else:
            CustomLogging.error(f"Fragment type {fragment_type} does not exists")
    else:
        CustomLogging.error(f"Flag {FLAG_FRAGMENT_TYPE} not defined in blueprint")
    return build
