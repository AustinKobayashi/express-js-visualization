import re
from collections import defaultdict
paths = {}
regex = {}


def router_files(path):
    with open(path, 'r') as file:
        for line in file:
            if 'Router()' in line:
                name = re.sub(r'\s?=(.+)|((var|let|const)\s)|\n', '', line)
                print(name)
                if path not in paths:
                    paths[path] = {}

                if name not in paths[path]:
                    routes = search_router_use(file, name)
                    paths[path][name] = routes
                    router_files(path)

def find_use(line):
    for key, rx in regex.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def search_router_use(file, name):
    build_regex(name)
    routes = defaultdict(list)
    for line in file:
        key, match = find_use(line)

        if key == 'router_get':
            routes[match.group('endpoint_get')].append('get')
        if key == 'router_put':
            routes[match.group('endpoint_put')].append('put')
        if key == 'router_post':
            routes[match.group('endpoint_post')].append('post')
        if key == 'router_delete':
            routes[match.group('endpoint_delete')].append('delete')
        if key == 'router_patch':
            routes[match.group('endpoint_delete')].append('delete')
    return routes

def build_regex(name):
    regex['router_get'] = re.compile(r'' + re.escape(name) + r'\.get\((?:\'|\")(?P<endpoint_get>.+)(?:\'|\"),(.?)')
    regex['router_put'] = re.compile(r'' + re.escape(name) + r'\.put\((?:\'|\")(?P<endpoint_put>.+)(?:\'|\"),(.?)')
    regex['router_post'] = re.compile(r'' + re.escape(name) + r'\.post\((?:\'|\")(?P<endpoint_post>.+)(?:\'|\"),(.?)')
    regex['router_delete'] = re.compile(r'' + re.escape(name) + r'\.delete\((?:\'|\")(?P<endpoint_delete>.+)(?:\'|\"),(.?)')
    regex['router_patch'] = re.compile(r'' + re.escape(name) + r'\.patch\((?:\'|\")(?P<endpoint_patch>.+)(?:\'|\"),(.?)')