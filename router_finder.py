import os
import re

symbol_table = dict([('app', 'express()'), ('router', 'express.Router()')])
regex = {}
app_var = ''
router_var = ''

def get_js_files(directory):
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".js"):
            file_paths.append(os.path.join(directory, file))
    return file_paths

def get_routes(file_paths):
    build_regex()
    for path in file_paths:
        file = open(path)
        for line in file:
            if line.strip().startswith((f'{app_var}.use')):
                print(line)
                
def build_regex():
    # app .use()
    app_var = list(symbol_table.keys())[list(symbol_table.values()).index('express()')]
    # router .get() .post() .put() .delete() .patch()
    router_var = list(symbol_table.keys())[list(symbol_table.values()).index('express.Router()')]

    regex['app_use'] = re.compile(r'' + re.escape(app_var) + r'\.use\((?:\'|\")(.+)(?:\'|\"),\s?(\w+)\)')
    regex['router_get'] = re.compile(r'' + re.escape(router_var) + r'\.get\((?:\'|\")(.+)(?:\'|\"),(.?)')
    regex['router_put'] = re.compile(r'' + re.escape(router_var) + r'\.put\((?:\'|\")(.+)(?:\'|\"),(.?)')
    regex['router_post'] = re.compile(r'' + re.escape(router_var) + r'\.post\((?:\'|\")(.+)(?:\'|\"),(.?)')
    regex['router_delete'] = re.compile(r'' + re.escape(router_var) + r'\.delete\((?:\'|\")(.+)(?:\'|\"),(.?)')
    regex['router_patch'] = re.compile(r'' + re.escape(router_var) + r'\.patch\((?:\'|\")(.+)(?:\'|\"),(.?)')
    