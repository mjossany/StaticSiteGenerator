import os

from pathlib import Path

from block_markdown import (markdown_to_html_node, extract_title)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as markdown_content:
        markdown = markdown_content.read()
    with open(template_path) as template_content:
        template = template_content.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    file_path = Path(dest_path)
    new_file_path = file_path.with_suffix(".html")
    dest_path = new_file_path

    with open(dest_path, 'w') as dest_file:
        dest_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        dest_file_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path) and is_markdown(file):
            generate_page(file_path, template_path, dest_file_path)
        else:
            generate_pages_recursive(file_path, template_path, dest_file_path)

def is_markdown(file):
    markdown_extensions = {".md", ".markdown"}
    _, extension = os.path.splitext(file)
    return extension.lower() in markdown_extensions