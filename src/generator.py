from block_converter import markdown_to_blocks, heading_level, block_to_block_type
from block import BlockType
from markdown_converter import markdown_to_html_node
from htmlnode import HTMLNode
import os

def extract_title(markdown):
    
    if markdown == None or markdown.strip() == "":
        raise Exception("markdown cannot be empty")

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        type = block_to_block_type(block)
        if type == BlockType.HEADING:
            if heading_level(block, type) == 1:
                return block.split(" ", maxsplit=1)[1]
    
    raise ValueError("No title in the markdown file")

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception("from path does not exist")

    md = ""
    with open(from_path, 'r') as f:
        md = f.read()

    node = markdown_to_html_node(md)
    html = node.to_html()

    title = extract_title(md)

    template = ""
    with open(template_path, 'r') as f:
        template = f.read()
    template_with_title = template.replace("{{ Title }}", title)

    output = template_with_title.replace("{{ Content }}", html)

    output = output.replace("href=\"/", f"href=\"{basepath}")
    output = output.replace("src=\"/", f"href=\"{basepath}")


    dest_dir = dest_path.split("/")
    dest_dir = "/".join(dest_dir[:-1])
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        template = f.write(output)
