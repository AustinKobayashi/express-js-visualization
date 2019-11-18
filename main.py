import router_finder


def main():
    directory = input("Please enter the path to the directory to scan:\n").strip()
    router_finder.get_js_files(directory)


if __name__ == "__main__":
    main()