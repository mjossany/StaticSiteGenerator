import os
import shutil

from copystatic import copy_files_recursive
from generatepage import (generate_pages_recursive)

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_template = "./template.html"

def main():
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public)

main()