from json_compiler.Compiler import Compiler as json_compiler
import sys
COMPILERS = {
    "django-postgres.v1": "under development",
    "flask-mongo.v1": "under development",
    "nodejs-mongo.v1": "under development",
    "json.v1": json_compiler
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
# python .\compiler.py c "json.v1" ../blueprints/examples/facebook/main.app.json
# python .\compiler.py c "json.v1" ./sample_blueprints/samples/import.app.json