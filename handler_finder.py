import main
import re
from collections import defaultdict
import file_finder

EXPRESS = 'express()'

regex = {}
handlers = []

def get_handlers(file_paths):
  build_regex()
  
  for file_path in file_paths:
    get_handler_code(file_path)
              
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

def get_handler_code(file_path):
  counting_brackets = False;
  cumulative_string = "";
  bracket_count = 0;
  with open(file_path, 'r') as file:

    file_finder.router_files(file_path)
    
    for line in file:

      key, match = parse_line(line)

      if counting_brackets:
        bracket_count += line.count("{") - line.count("}")
        if bracket_count == 0:
            counting_brackets = False
            handlers.append(cumulative_string);
        else:
            cumulative_string += line;
      
      if key == 'app_get' or key == 'app_put' or key == 'app_post' or key == 'app_delete' or key == 'app_patch':
        bracket_count = line.count("{") - line.count("}")
        counting_brackets = True;