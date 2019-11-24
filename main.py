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
    
    
    fake_handler = {
        '/database/old': {
            'methods': ['GET'],
            'file_path': './ExampleServer/ExampleServer\\app.js',
            'path_params': []
        }
    }
    
    for key, object in endpoint_finder.endpoints:
        for method_string in object.methods:
            handler = handler_finder.get_handlers({method: method_string, file_path: object.file_path, route: key})
            print(handler)
            route_subhandlers = functions_called_by_route_handler.get_sub_handler([], file_paths, handler.code)
    #print(symbol_table)
    #print(endpoint_finder.endpoints)

    #print(file_finder.paths)

    fake_data = {
        "endpoint": "/example/:user_id",
        "method": "GET",
        "params": ["user_id"],
        "handler": {
            "file": "Example.js",
            "code": "console.log('Request to example!')"
        },
        "subhandlers": [
            {
                "file": "Backend.js",
                "code": "console.log('Request to backend!')"
            },
            {
                "file": "Database.js",
                "code": "console.log('Request to database!')"
            }
        ]
    }

    # change "file_path" to the path of app.js on your system

    # This function must be passed the code for handler for the route
    # Right now it uses a dummy value: 'DatabaseBuilder.add_articles_to_database() ....'
    #print(route_subhandlers)


if __name__ == "__main__":
    main()
