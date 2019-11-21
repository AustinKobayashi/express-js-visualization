import re
paths = {}

def router_files(file, path, line):
    if 'Router()' in line:
        name = re.sub(r'\s?=(.+)|((var|let|const)\s)|\n', '', line)
        if path not in paths:
            paths[path] = [name]
        else:
            if name not in paths[path]:
                paths[path].append(name)
