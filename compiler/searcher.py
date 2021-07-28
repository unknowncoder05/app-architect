import os
def search_json(route, base_file):
    splited = route.split(".")

    print(os.listdir(os.path.dirname(base_file)))
    #for step in splited:
    #    os.listdir()