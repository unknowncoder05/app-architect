class Fragment:
    blueprint:dict
    general_compile=None#:function
    def __init__(self, blueprint, *, compile) -> None:
        self.general_compile = compile
        self.blueprint = blueprint
    def compile(self)->str:
        fragment_build = self.blueprint.get("type","")
        return fragment_build