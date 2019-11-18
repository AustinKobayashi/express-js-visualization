import os


def get_js_files(directory):
    for file in os.listdir(directory):
        if file.endswith(".js"):
            print("Found: " + os.path.join(directory, file))
