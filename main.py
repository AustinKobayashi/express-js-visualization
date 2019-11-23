import router_finder
import endpoint_finder
import file_finder
import handler_finder

# need to grab this dynamically (e.g. express() is not always assigned to 'app')
symbol_table = dict()

def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    file_paths = router_finder.get_js_files(directory)
    endpoint_finder.get_routes(file_paths)
    handler_finder.get_handlers(file_paths)
    print(symbol_table)
    print(endpoint_finder.endpoints)
    print(handler_finder.handlers);

    print(file_finder.paths)


if __name__ == "__main__":
    main()