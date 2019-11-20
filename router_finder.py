import os

def get_js_files(directory):
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".js"):
            file_paths.append(os.path.join(directory, file))
    return file_paths