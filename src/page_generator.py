import os

from blockmarkdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if (line.startswith("# ")):
            return line.lstrip("# ")
    raise Exception("Page needs an <h1>")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.isfile(from_path) and os.path.isfile(template_path):
        print("Reading markdown and storing to memory...")
        base_index = open(from_path, "r")
        index_md = base_index.read()
        base_index.close()
        print("Done!")
        print("----------------------------------------------")
        print("Reading template and storing to memory...")
        template = open(template_path, "r")
        template_html = template.read()
        template.close()
        print("Done!")
        print("----------------------------------------------")
        print("Generating HTML nodes from markdown...")
        markdown_html_node = markdown_to_html_node(index_md)
        html_from_markdown = markdown_html_node.to_html()
        title = extract_title(index_md)
        template_html = template_html.replace("{{ Title }}", title)
        template_html = template_html.replace("{{ Content }}", html_from_markdown)
        print("Done!")
        print("----------------------------------------------")
        print("Writing to new index.html file...")
        dest_dir_path = os.path.dirname(dest_path)
        if dest_dir_path != "":
            os.makedirs(dest_dir_path, exist_ok=True)
        new_file = open(dest_path, "w")
        new_file.write(template_html)
        new_file.close()
        print("Done!")
        print("----------------------------------------------")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if (os.path.exists(dir_path_content)):
        list_of_files = os.listdir(dir_path_content) 
        for file in list_of_files:
            existing_file_path = os.path.join(dir_path_content, file)
            if (os.path.isfile(existing_file_path)):
                print(file)
                file_html = f"{file.strip(".md")}.html"
                new_file_path = os.path.join(dest_dir_path, file_html)
                generate_page(existing_file_path, template_path, new_file_path)
            else:
                new_file_path = os.path.join(dest_dir_path, file)
                generate_pages_recursive(existing_file_path, template_path, new_file_path)
