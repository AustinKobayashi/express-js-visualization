import main
import re
from collections import defaultdict
import file_finder

EXPRESS = 'express()'

regex = {
  'express_app': re.compile(r'(var|const|let)(\s+)(?P<app_var>.+)(\s*)\=(\s*)' + re.escape(EXPRESS)),
}
# example key value pair
# '/database': ['get', 'post']
endpoints = defaultdict(list)

def get_routes(file_paths): 
  for file_path in file_paths:
    add_symbol(file_path)
  
  build_regex()
  
  for file_path in file_paths:
    get_supported(file_path)
              
def build_regex():
  app_var = list(main.symbol_table.keys())[list(main.symbol_table.values()).index('express()')]

  regex['app_get'] = re.compile(r'' + re.escape(app_var) + r'\.get\((?:\'|\")(?P<endpoint_get>.+)(?:\'|\"),(.?)')
  regex['app_put'] = re.compile(r'' + re.escape(app_var) + r'\.put\((?:\'|\")(?P<endpoint_put>.+)(?:\'|\"),(.?)')
  regex['app_post'] = re.compile(r'' + re.escape(app_var) + r'\.post\((?:\'|\")(?P<endpoint_post>.+)(?:\'|\"),(.?)')
  regex['app_delete'] = re.compile(r'' + re.escape(app_var) + r'\.delete\((?:\'|\")(?P<endpoint_delete>.+)(?:\'|\"),(.?)')
  regex['app_patch'] = re.compile(r'' + re.escape(app_var) + r'\.patch\((?:\'|\")(?P<endpoint_patch>.+)(?:\'|\"),(.?)')

def parse_line(line):
  for key, rx in regex.items():
    match = rx.search(line)
    if match:
      return key, match
  return None, None

def get_supported(file_path):
  with open(file_path, 'r') as file:

    file_finder.router_files(file_path)
    
    for line in file:

      key, match = parse_line(line)

      # extract endpoint string and respective HTTP method
      if key == 'app_get':
        endpoints[match.group('endpoint_get')]['methods'].append('get')
        endpoints[match.group('endpoint_get')]['file_path'] = file_path
        params = [s[1:] for s in re.findall(':[^/]+', match.group('endpoint_get'))]
        endpoints[match.group('endpoint_get')]['params'] = params
      if key == 'app_put':
        endpoints[match.group('endpoint_put')]['methods'].append('put')
        endpoints[match.group('endpoint_put')]['file_path'] = file_path
        params = [s[1:] for s in re.findall(':[^/]+', match.group('endpoint_put'))]
        endpoints[match.group('endpoint_put')]['params'] = params
      if key == 'app_post':
        endpoints[match.group('endpoint_post')]['methods'].append('post')
        endpoints[match.group('endpoint_post')]['file_path'] = file_path
        params = [s[1:] for s in re.findall(':[^/]+', match.group('endpoint_post'))]
        endpoints[match.group('endpoint_post')]['params'] = params
      if key == 'app_delete':
        endpoints[match.group('endpoint_delete')]['methods'].append('delete')
        endpoints[match.group('endpoint_delete')]['file_path'] = file_path
        params = [s[1:] for s in re.findall(':[^/]+', match.group('endpoint_delete'))]
        endpoints[match.group('endpoint_delete')]['params'] = params
      if key == 'app_patch':
        endpoints[match.group('endpoint_patch')]['methods'].append('patch')
        endpoints[match.group('endpoint_patch')]['file_path'] = file_path
        params = [s[1:] for s in re.findall(':[^/]+', match.group('endpoint_patch'))]
        endpoints[match.group('endpoint_patch')]['params'] = params

def add_symbol(file_path):
  with open(file_path, 'r') as file:
    for line in file:
      key, match = parse_line(line)
      # find variable names and add to symbol table
      if key == 'express_app':
        main.symbol_table[match.group('app_var').strip()] = EXPRESS