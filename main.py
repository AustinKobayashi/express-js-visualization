import functions_called_by_route_handler
import router_finder
import endpoint_finder
import file_finder
import handle_graph
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
    
    paths = file_finder.router_files(file_paths)
    print(paths)

    endpoint_finder.get_routes(paths)

    routes = []

    for key, value in endpoint_finder.endpoints.items():
        for method_string in value['methods']:
            handler = handler_finder.get_handlers({'method': method_string, 'file_path': value['file_path'], 'route': key})
            route_subhandlers = functions_called_by_route_handler.get_sub_handler([], file_paths, handler['code'])
            route = {
                'endpoint': key,
                'method': method_string.upper(),
                'params': value['params'],
                'handler': handler,
                'subhandlers': route_subhandlers
            }
            routes.append(route)

    print(routes)
    handle_graph.generate_graph(routes)


if __name__ == "__main__":
    main()
