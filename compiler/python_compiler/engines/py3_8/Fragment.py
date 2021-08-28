class Fragment:
    blueprint:dict
    def __init__(self, blueprint) -> None:
        self.blueprint = blueprint
    def compile(self)->str:
        fragment_build = self.blueprint.get("type","")
        return fragment_build