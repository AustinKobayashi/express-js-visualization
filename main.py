import router_finder


def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    file_paths = router_finder.get_js_files(directory)
    router_finder.get_routes(file_paths)


if __name__ == "__main__":
    main()