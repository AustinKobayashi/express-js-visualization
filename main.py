import functions_called_by_route_handler
import router_finder
import endpoint_finder
import file_finder
import handler_finder

# need to grab this dynamically (e.g. express() is not always assigned to 'app')
symbol_table = dict()


def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    valid = False
    file_paths = []
    while not valid:
        try:
            file_paths = router_finder.get_js_files(directory)
            valid = True
        except FileNotFoundError:
            directory = input("Please enter the path to the directory to scan:\n").strip()

    print(file_paths)
    endpoint_finder.get_routes(file_paths)
    
    for key, object in endpoint_finder.endpoints:
        for method_string in object.methods
            handler = handler_finder.get_handlers({method: method_string, file_path: object.file_path, route: key})
    print(symbol_table)
    print(endpoint_finder.endpoints)
    print(handler_finder.handlers);

    print(file_finder.paths)


    # This function must be passed the code for handler for the route
    # Right now it uses a dummy value: 'DatabaseBuilder.add_articles_to_database() ....'
    for handler in handler_finder.handlers:
        route_subhandlers = functions_called_by_route_handler.get_sub_handler([], file_paths, handler)
    print(route_subhandlers)


if __name__ == "__main__":
    main()
