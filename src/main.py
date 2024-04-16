import os
import shutil

from copy_static import copy_files
from page_generator import generate_pages_recursive

static_path = "./static"
public_path = "./public"
content_path = "./content"
template_path = "./template.html"

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
    if os.path.exists(template_path) and os.path.isfile(template_path):
        generate_pages_recursive(content_path, template_path, public_path)

main()
