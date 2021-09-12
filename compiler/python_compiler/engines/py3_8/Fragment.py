from utils.flags import *

class Fragment:
    blueprint = {}
    general_compile = None#:function
    level = 0
    inports = []
    def __init__(self, blueprint, *, compile, level=0) -> None:
        self.general_compile = compile
        self.blueprint = blueprint
        self.level = level

    def get_lines(self) -> list:
        fragment_lines = []
        fragment_lines = self.tabulate(fragment_lines)
        return fragment_lines

    def code_lines_compile(self, fragments) -> list:
        code_build_lines = []
        for line in fragments:
            line_build = self.general_compile(line, level=self.level+1)  # level=self.level+1
            code_build_lines.extend(line_build)
        return code_build_lines
    
    def tabulate(self, lines, custom_tabs=0) -> list:
        tabulated_lines = []
        for line in lines:
            level = self.level if custom_tabs == 0 else custom_tabs
            tabs = TAB * ( 0 if level == 0 else 1)
            tabulated_lines.append(tabs+line)
        return tabulated_lines

    def compile(self) -> str:
        fragment_build = self.blueprint.get("type","")
        return fragment_build
    