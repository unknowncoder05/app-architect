class Fragment:
    blueprint:dict
    general_compile=None#:function
    level=0
    def __init__(self, blueprint, *, compile, level=0) -> None:
        self.general_compile = compile
        self.blueprint = blueprint
        self.level = level
    def compile(self)->str:
        fragment_build = self.blueprint.get("type","")
        return fragment_build