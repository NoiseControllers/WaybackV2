def load_file(file_path: str) -> list:
    temp = []
    try:
        with open(file_path, encoding='utf-8') as file:
            for line in file:
                if file == "" or file is None:
                    continue
                temp.append(line)
    except (TypeError, FileNotFoundError):
        print(f"[!] No se ha podido abrir el archivo {file_path}")

    return temp
