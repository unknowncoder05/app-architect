import json
import sys
from json_compiler.Compiler import Compiler as json_compiler
from django_compiler.Compiler import Compiler as django_compiler
from python_compiler.Compiler import Compiler as python_compiler

COMPILERS = { # "framework.language.version: compiler"
    "django.json.v1": django_compiler,
    "python.json.v1": python_compiler,
    "flask.json.v1": "under development",
    "nodejs.json.v1": "under development",
    "json.v1": json_compiler
}
def compile(compiler_name, project_name):
    compiler = COMPILERS[compiler_name](main_file=project_name)
    compiled_project = compiler.compile()
    with open(f"./{sys.argv[4]}/{compiled_project.get('name', 'project')}.build.json", "w") as f:
        json.dump(compiled_project, f, indent=4)
OPTIONS = {
    "compile": compile,
    "c": compile
}
def main():
    # 1 action
    # 2 compiler
    # 3 project
    # 4 destination folder
    OPTIONS[sys.argv[1]](sys.argv[2], sys.argv[3])
    return

main()
# python .\compiler.py c "json.v1" ../blueprints/examples/facebook/main.app.json build
# python .\compiler.py c "json.v1" ./sample_blueprints/samples/import.app.json build
# python .\compiler.py c "json.v1" ./sample_blueprints/samples/construct.app.json build
# python .\compiler.py c "json.v1" ../blueprints/examples/calculator/v2/main.app.json build

# python .\compiler.py c "django.json.v1" ../blueprints/examples/facebook/main.app.json build
# python .\compiler.py c "python.json.v1" ../blueprints/examples/calculator/v2/services/processing/operations/sum.code.json build

