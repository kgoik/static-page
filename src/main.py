from generator import generate_page 
import os
import shutil
import sys

def main():
    
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    dest_folder = "docs"
    print(f"Removing old {dest_folder} folder")
    remove_old_dest(dest_folder)
    print(f"Creating new {dest_folder} folder")
    create_new_dest(dest_folder)
    copy_files("static", "docs")
    generate_pages_recursive(basepath, "content", "template.html", "docs")

def remove_old_dest(dest_folder):
    if(os.path.exists(dest_folder)):
        print("Removed")
        shutil.rmtree(dest_folder)

def create_new_dest(dest_folder):
    if not os.path.exists(dest_folder):
        print("Created")
        os.mkdir(dest_folder)

def copy_files(old_path, new_path):
    tree = os.listdir(old_path)
    
    for item in tree:
        item_path = os.path.join(old_path, item)
        new_item_path = os.path.join(new_path, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, os.path.join(new_item_path))
        else: 
            os.mkdir(new_item_path)
            copy_files(item_path, new_item_path)

def generate_pages_recursive(base_path, dir_path_content, template_path, dest_dir_path):
    tree = os.listdir(dir_path_content)

    for item in tree:
        print(item)
        item_path = os.path.join(dir_path_content, item)
        new_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            if item.endswith('.md'):
                new_item_path = new_item_path.replace(".md", ".html")
                generate_page(base_path, item_path, template_path, new_item_path)
        else: 
            os.mkdir(new_item_path)
            generate_pages_recursive(base_path, item_path, template_path, new_item_path)


main()
