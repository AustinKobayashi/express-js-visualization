import os


def get_js_files(directory):
    list_of_files = os.listdir(directory)
    file_paths = []

    for file in list_of_files:
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            file_paths = file_paths + get_js_files(path)
        elif file.endswith(".js") and "node_modules" not in path:
            file_paths.append(path)

    return file_paths
