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
    handler_finder.get_handlers(file_paths)
    print(symbol_table)
    print(endpoint_finder.endpoints)
    print(handler_finder.handlers);

    print(file_finder.paths)


    # This function must be passed the code for handler for the route
    # Right now it uses a dummy value: 'DatabaseBuilder.add_articles_to_database() ....'
    route_subhandlers = functions_called_by_route_handler.get_sub_handler([], file_paths, '''DatabaseBuilder.add_articles_to_database(); 
    res.end();''')
    print(route_subhandlers)


if __name__ == "__main__":
    main()
