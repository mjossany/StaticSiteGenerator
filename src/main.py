import os
import shutil

from textnode import TextNode
from textnode import TextType

def main():
    print(TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
    copy_from_static_to_public()

def copy_from_static_to_public():
    destination_dir = "public"
    if os.path.exists("public") and len(os.listdir("public")) > 0:
        clear_destination_folder("public")
    if not os.path.exists("public"):
        current_path = os.path.dirname(os.path.abspath("src"))
        destination_path = os.path.join(current_path, destination_dir)
        os.mkdir(destination_path)
    copy_files_from_source_folder_to_destination_folder("static", "public")
    

def clear_destination_folder(destination_folder):
    destination_folder_path = os.path.abspath(destination_folder)
    for file in os.listdir(destination_folder):
        file_path = os.path.join(destination_folder_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)

def copy_files_from_source_folder_to_destination_folder(source_folder, destination_folder):
    source_folder_path = os.path.abspath(source_folder)
    destination_folder_path = os.path.abspath(destination_folder)
    for file in os.listdir(source_folder_path):
        file_path = os.path.join(source_folder_path, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination_folder_path)
        else:
            new_destination_folder_path = os.path.join(destination_folder_path, file)
            os.mkdir(new_destination_folder_path)
            copy_files_from_source_folder_to_destination_folder(file_path, new_destination_folder_path)

main()
