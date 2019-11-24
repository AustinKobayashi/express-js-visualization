import main
import re
from collections import defaultdict
import file_finder
import os

EXPRESS = 'express()'

regex = {}

def get_handlers(route_obj):
  build_regex(route_obj.method, route_obj.route)
  return get_handler_code(route_obj)
              
def build_regex(route_method, route):
  app_var = list(main.symbol_table.keys())[list(main.symbol_table.values()).index('express()')]

  if route_method == "get":
    regex['app_get'] = re.compile(r'' + re.escape(app_var) + r'\.get\((?:\'|\")' + re.escape(route) + '(?:\'|\"),(.?)')
  
  if route_method == "put":
    regex['app_put'] = re.compile(r'' + re.escape(app_var) + r'\.put\((?:\'|\")' + re.escape(route) + '(?:\'|\"),(.?)')
  
  if route_method == "post":
    regex['app_post'] = re.compile(r'' + re.escape(app_var) + r'\.post\((?:\'|\")' + re.escape(route) + '(?:\'|\"),(.?)')
  
  if route_method == "delete":
    regex['app_delete'] = re.compile(r'' + re.escape(app_var) + r'\.delete\((?:\'|\")' + re.escape(route) + '(?:\'|\"),(.?)')
  
  if route_method == "patch":
    regex['app_patch'] = re.compile(r'' + re.escape(app_var) + r'\.patch\((?:\'|\")' + re.escape(route) + '(?:\'|\"),(.?)')

def parse_line(line):
  for key, rx in regex.items():
    match = rx.search(line)
    if match:
      return key, match
  return None, None
  
def remove_garbage_from_path(router):
    return file[file.rindex(os.path.sep) + 1:]

def get_handler_code(route_obj):
  counting_brackets = False;
  cumulative_string = "";
  bracket_count = 0;
  with open(route_obj.file_path, 'r') as file:

    file_finder.router_files(route_obj.file_path)
    
    for line in file:

      key, match = parse_line(line)

      if counting_brackets:
        bracket_count += line.count("{") - line.count("}")
        if bracket_count == 0:
            counting_brackets = False
            return {file: remove_garbage_from_path(route_obj.file_path), code: cumulative_string}
        else:
            cumulative_string += line;
      
      if key != None:
        bracket_count = line.count("{") - line.count("}")
        counting_brackets = True;