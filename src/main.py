from generator import generate_page 
import os
import shutil

def main():
    print("Removing old public folder")
    remove_old_public()
    print("Creating new public folder")
    create_new_public()
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def remove_old_public():
    if(os.path.exists("public")):
        print("Removed")
        shutil.rmtree("public")

def create_new_public():
    if not os.path.exists("public"):
        print("Created")
        os.mkdir("public")

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    tree = os.listdir(dir_path_content)

    for item in tree:
        print(item)
        item_path = os.path.join(dir_path_content, item)
        new_item_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            if item.endswith('.md'):
                new_item_path = new_item_path.replace(".md", ".html")
                generate_page(item_path, template_path, new_item_path)
        else: 
            os.mkdir(new_item_path)
            generate_pages_recursive(item_path, template_path, new_item_path)


main()
