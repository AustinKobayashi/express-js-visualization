def get_files(file_path):
    for path in file_path:
        parse_file(path)

def parse_file(path):
    with open(path, 'r') as file:
        for line in file:
            if 'router()' in line:
                print(line)