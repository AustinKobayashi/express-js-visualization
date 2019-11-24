import re
from collections import defaultdict
paths = []


def router_files(file_paths):
    for path in file_paths:
        with open(path, 'r') as file:
            for line in file:
                rx = re.compile(r'require\((?:\'|\")express(?:\'|\")\)')
                match = rx.search(line)
                if match and path not in paths:
                    paths.append(path)
    print(paths)
    return paths