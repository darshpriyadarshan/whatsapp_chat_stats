def read_file(file_path):
    file = open(file_path, encoding="utf8", mode="r")
    file_contents = file.read()
    return file_contents
