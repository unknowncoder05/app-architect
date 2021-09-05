from .Fragment import Fragment
from utils.flags import *
from utils.CustomLogging import CustomLogging
from python_compiler.engines.utils.types import get_python_type_str, ANY


class FunctionArgs(Fragment):
    def __init__(self, blueprint, *args, **kwargs) -> None:
        super().__init__(blueprint, *args, **kwargs)
    def compile(self) -> str:
        fragment_build = ""
        cleaned_args = []
        for arg in self.blueprint:
            if not (arg_type_name := self.blueprint[arg].get(ATTRIBUTE_TYPE)):
                arg_type_name = ANY
            if (arg_default_value := self.blueprint[arg].get(ATTRIBUTE_DEFAULT, "")) != "":
                arg_default_value = "="+str(arg_default_value)
            if arg_type := get_python_type_str(arg_type_name):
                arg_type = ":"+arg_type
            cleaned_arg = f"{arg}{arg_type}{arg_default_value}"
            cleaned_args.append(cleaned_arg)
        fragment_build = ", ".join(cleaned_args)
        return fragment_build