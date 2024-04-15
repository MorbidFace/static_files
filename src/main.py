import os
import shutil

from copy_static import copy_files

static_path = "./static"
public_path = "./public"

def handle_copy():
    print("==============================================")
    print(f"Copy files from {static_path} to {public_path}")
    print("==============================================")
    if (os.path.exists(public_path) and os.path.isdir(public_path)):
        print(f"{public_path} exists: Removing...")
        shutil.rmtree(public_path)
        print(f"Deleted {public_path}")
        print("==============================================")
    print(f"Creating {public_path} directory...")
    os.mkdir(public_path)
    print(f"Created {public_path} directory")
    print("==============================================")
    copy_files(static_path, public_path)
    print("==============================================")
    print("Files Copied!")
    print("==============================================")


def main():
    handle_copy()

main()
