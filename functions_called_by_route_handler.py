import re

reserved = ['forEach', 'then', 'push', 'toJSON', 'log', 'on', 'eachSeries', 'setTimeout', 'sleep', 'get',
            'post', 'put', 'delete', 'warn', 'error', 'split', 'join', 'dir']


def is_reserved(word):
    word = word.replace('(', '')
    word = word.replace(')', '')
    return word in reserved


def get_sub_handler(found, file_paths, parent_handler):
    handlers = {}

    functions = re.findall("\.[^().;]+\(.*\)\s*[.;]", parent_handler)

    for function_name in functions:
        function_name = function_name[1:]

        if function_name.find('(') > 0:
            function_name = function_name[:function_name.find('(')]

        if function_name in found:
            continue

        if is_reserved(function_name):
            continue

        for file in file_paths:
            f = open(file, "r")
            file_text = f.read()

            if function_name not in file_text:
                continue

            if re.search(function_name + '\s*\([^();:\'"]*\)\s*{', file_text):
                index = re.search(function_name + '\s*\([^();:\'"]*\)\s*{', file_text).start()
                file_text = file_text[index:]
                open_brackets = 0
                closing_brackets = 0
                end_index = 0
                for i in range(0, len(file_text)):
                    char = file_text[i]
                    if char == '{':
                        open_brackets += 1
                    elif char == '}':
                        closing_brackets += 1

                    if open_brackets == closing_brackets and open_brackets != 0:
                        end_index = i + 1
                        break

                file_text = file_text[:end_index]
                file_text = file_text[file_text.index('{') + 1: file_text.rindex('}')]
                found.append(function_name)
                handlers[function_name] = file_text

                sub_handlers = get_sub_handler(found, file_paths, file_text)
                handlers = merge_two_dicts(handlers, sub_handlers)

    return handlers


def merge_two_dicts(dict1, dict2):
    merged = dict1.copy()
    merged.update(dict2)
    return merged
