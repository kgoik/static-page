from block_converter import markdown_to_blocks, block_to_block_type
from node_converter import text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode
from block import BlockType
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        type = block_to_block_type(block)
        node = convert_to_htmlnode(block, type)
        children.append(node)

    parent_node = HTMLNode("div", None, children)
    return parent_node



def convert_to_htmlnode(block, type):
    #1 get tag based on the block type 
    tag = get_tag_for_block_type(block, type)

    #2 if multi level create children nodes
    if type == BlockType.CODE:
        clean_block = ""

        for line in block.splitlines():
            if line.strip().startswith("```"):
                continue
            else:
                clean_block += line + "\n"
        node = TextNode(clean_block, TextType.CODE)
        children = [text_node_to_html_node(node)]
    else:
        children = text_to_children(block, type)

    #1 create parent level node based on type
    parent_node = HTMLNode(tag, None, children)

    return parent_node

    

    #3 transform text to text_nodes with text_to_textnodes

    #4 transform textnodes to leaf_node text_node_to_html_node(text_node):

    #5 place inside of parent node 

def get_tag_for_block_type(block, type):
    match(type):
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            level = len(block.split()[0])
            return f"h{level}"
        case BlockType.CODE:
            return "pre"
        case BlockType.ORDERD_LIST:
            return "ol"
        case BlockType.UNORDERD_LIST:
            return "ul"
        case BlockType.QUOTE:
            return "blockquote"
        case _: 
            raise ValueError("no such block type")
        
def text_to_children(block, type):
    children = []
    if type in [BlockType.UNORDERD_LIST, BlockType.ORDERD_LIST]:
        children = transform_list_element(block)
    elif type == BlockType.QUOTE:
        children = transform_quote_element(block)
    else:
        text = block
        if type == BlockType.HEADING:
            text = block.split(maxsplit=1)[1]

        inline_text = ""
        for line in text.split("\n"):
            inline_text += line.strip() + " "
    
        inline_text = inline_text.strip()

        text_nodes = text_to_textnodes(inline_text)
        for text_node in text_nodes:
            children.append(text_node_to_html_node(text_node))

    return children
                
def transform_list_element(block):
    nodes = []
    for line in block.split("\n"):
        line = line.split(maxsplit=1)[1]
        text_nodes = text_to_textnodes(line)
        children = []
        for text_node in text_nodes:
            children.append(text_node_to_html_node(text_node))
        
        nodes.append(HTMLNode("li", children=children))

    return nodes

def transform_quote_element(block):
    children = []
    for line in block.split("\n"):
        text_nodes = text_to_textnodes(line[2:])
        for text_node in text_nodes:
            children.append(text_node_to_html_node(text_node))

    return children


# def get_child_tag

# md = """1. this is test list
# 2. this is list"""

# md = "### this is heading text and some **bold** text too!"

# md = """```
# this is _code_ **block**
# ```"""

# markdown_to_html_node(md)