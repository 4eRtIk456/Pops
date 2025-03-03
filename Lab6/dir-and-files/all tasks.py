import os
import shutil


# 1
def list_files_and_dirs(path):
    try:
        all_items = os.listdir(path)
        dirs = [d for d in all_items if os.path.isdir(os.path.join(path, d))]
        files = [f for f in all_items if os.path.isfile(os.path.join(path, f))]
        return dirs, files, all_items
    except FileNotFoundError:
        return "Path not found"

# 2
def check_access(path):
    return {
        "Exists": os.path.exists(path),
        "Readable": os.access(path, os.R_OK),
        "Writable": os.access(path, os.W_OK),
        "Executable": os.access(path, os.X_OK),
    }

# 3
def path_info(path):
    if os.path.exists(path):
        return os.path.dirname(path), os.path.basename(path)
    return "Path does not exist"

# 4
def count_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        return "File not found"

# 5
def write_list_to_file(filename, data):
    with open(filename, 'w') as file:
        file.writelines("\n".join(map(str, data)))

# 6
def generate_text_files():
    for letter in range(65, 91):  
        with open(f"{chr(letter)}.txt", 'w') as file:
            file.write(f"This is file {chr(letter)}.txt")

# 7
def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
    except FileNotFoundError:
        return "Source file not found"

# 8
def delete_file(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        return "File deleted"
    return "File not found or access denied"
