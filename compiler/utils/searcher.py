import os
from pathlib import Path
dir = Path(os.path.dirname(__file__))
GLOBAL_ROUTE = dir / ".." / ".." / "blueprints"

def list_dir(path):
    return [ x.split(".") for x  in os.listdir(path)]

def get_json_file(splitted_route, dir_path): # dir_path:pathlib.Path
    files_names = list_dir(dir_path)
    for file_name in files_names:
        if splitted_route[0] == file_name[0]:
            new_path = dir_path / ".".join(file_name)
            if os.path.isfile(new_path):
                return new_path
            else:
                new_splitted_route = splitted_route[1:]
                nested = get_json_file(new_splitted_route, new_path)
                return nested

            #get_json(file_name.)
    return False

def search_json(route, *, base_folder=None):
    splitted_route = route.split(".")
    # Local Path
    if base_folder:
        json_component = get_json_file(splitted_route, base_folder)
        if json_component:
            return json_component
    # Global Path
    json_component = get_json_file(splitted_route, GLOBAL_ROUTE)
    if json_component:
        return json_component
