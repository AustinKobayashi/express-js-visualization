import os
import re

symbol_table = dict([('app', 'express()'), ('router', 'express.Router()')])
regex = {
    'express_app_var': re.compile(r'app\.use\((?:\'|\")(.+)(?:\'|\"),\s?(\w+)\)')
}

def get_js_files(directory):
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".js"):
            file_paths.append(os.path.join(directory, file))
    return file_paths

def get_routes(file_paths):
    for path in file_paths:
        file = open(path)
        for line in file:
            # app .use()
            express_app_var = list(symbol_table.keys())[list(symbol_table.values()).index('express()')]
            # router .get() .post() .put() .delete() .patch()
            express_router_var = list(symbol_table.keys())[list(symbol_table.values()).index('express.Router()')]
            
            if line.strip().startswith((f'{express_app_var}.use')):
                print(line)
                
