from json_compiler.Compiler import Compiler as json_compiler
import sys
COMPILERS = {
    "django-postgres": "under development",
    "flask-mongo": "under development",
    "nodejs-mongo": "under development",
    "json": json_compiler
}
def compile(compiler_name, project_name):
    compiler = COMPILERS[compiler_name](project_name)
    compiler.compile()
OPTIONS = {
    "compile": compile,
    "c": compile
}
def main():
    OPTIONS[sys.argv[1]](sys.argv[2], sys.argv[3])
    return

main()
#python .\compiler.py c json ../blueprints/examples/facebook/main.app.json