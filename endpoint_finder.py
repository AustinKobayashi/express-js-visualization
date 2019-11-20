import main
import re

regex = {}
app_var = ''
router_var = ''
# '/database': 'databaseRouter' 
endpoints = {}
# 'databaseRouter': [{ 'get': '/old' }, { 'get': '/' }, { 'post': '/' }]
subendpoints = {}
# 'databaseRouter': {path_to_databaseRouter}
subendpoints_files = {}

def get_routes(file_paths):
    build_regex()
    for file_path in file_paths:
        # file = open(path)
        # for line in file:
        #     if line.strip().startswith((f'{app_var}.use')):
        #         print(line)
        parse_file(file_path)
                
def build_regex():
    # app .use()
    app_var = list(main.symbol_table.keys())[list(main.symbol_table.values()).index('express()')]
    # router .get() .post() .put() .delete() .patch()
    router_var = list(main.symbol_table.keys())[list(main.symbol_table.values()).index('express.Router()')]

    regex['app_use'] = re.compile(r'' + re.escape(app_var) + r'\.use\((?:\'|\")(?P<endpoint>.+)(?:\'|\"),\s?(?P<subendpoint_filename>\w+)\)')
    regex['router_get'] = re.compile(r'' + re.escape(router_var) + r'\.get\((?:\'|\")(?P<subendpoint_get><.+)(?:\'|\"),(.?)')
    regex['router_put'] = re.compile(r'' + re.escape(router_var) + r'\.put\((?:\'|\")(?P<subendpoint_put>.+)(?:\'|\"),(.?)')
    regex['router_post'] = re.compile(r'' + re.escape(router_var) + r'\.post\((?:\'|\")(?P<subendpoint_post>.+)(?:\'|\"),(.?)')
    regex['router_delete'] = re.compile(r'' + re.escape(router_var) + r'\.delete\((?:\'|\")(?P<subendpoint_delete>.+)(?:\'|\"),(.?)')
    regex['router_patch'] = re.compile(r'' + re.escape(router_var) + r'\.patch\((?:\'|\")(?P<subendpoint_patch>.+)(?:\'|\"),(.?)')

def parse_line(line):
  for key, rx in regex.items():
    match = rx.search(line)
    if match:
      return key, match
  return None, None

def parse_file(file_path):
  with open(file_path, 'r') as file:
    for line in file:
      key, match = parse_line(line)
      # extract endpoint string and respective router variable
      if key == 'app_use':
        endpoints[match.group('endpoint')] = match.group('subendpoint_filename')