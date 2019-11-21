import router_finder
import endpoint_finder

# need to grab this dynamically (e.g. express() is not always assigned to 'app')
symbol_table = dict()

def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    file_paths = router_finder.get_js_files(directory)
    endpoint_finder.get_routes(file_paths)
    print(endpoint_finder.endpoints)


if __name__ == "__main__":
    main()