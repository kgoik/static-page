import re
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_to_textnodes(text):
    root = TextNode(text, TextType.NORMAL)

    bold_nodes = split_nodes_delimiter([root], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)

    return link_nodes


def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.NORMAL):
            return LeafNode(value=text_node.text)
        case(TextType.BOLD):
            return LeafNode(tag="b", value=text_node.text)
        case(TextType.ITALIC):
            return LeafNode(tag="i", value=text_node.text)
        case(TextType.CODE):
            return LeafNode(tag="code", value=text_node.text)
        case(TextType.LINK):
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case(TextType.IMAGE):
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("text node type is incorrect")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes= []
    
    for node in old_nodes:
        new_nodes.extend(convert_delimiter_node(node, delimiter, text_type))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes= []
    
    for node in old_nodes:
        new_nodes.extend(convert_ref_nodes(node, TextType.IMAGE))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes= []
    
    for node in old_nodes:
        new_nodes.extend(convert_ref_nodes(node, TextType.LINK))
    
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches




# def split_nodes_link(old_nodes):

def convert_delimiter_node(node, delimiter, text_type):
    if node.text_type != TextType.NORMAL:
        return [node]

    new_nodes = []
    if delimiter in node.text:
        text = node.text
        delimiter_count = text.count(delimiter)
        
        if delimiter_count % 2 == 1:
            raise Exception("delimiter closing not found")

        while delimiter_count > 0:
            nodes, text = split_the_text(delimiter, text, text_type)

            if nodes != None:
                new_nodes.extend(nodes)
            delimiter_count -= 2

        if len(text) > 0:
            new_node = TextNode(text, TextType.NORMAL)
            new_nodes.append(new_node)
    else: 
        new_node = TextNode(node.text, TextType.NORMAL)
        new_nodes.append(new_node)

    return new_nodes

def convert_ref_nodes(node, type):
    if node.text_type != TextType.NORMAL:
        return [node]

    new_nodes = []
    matches = []
    splitter = ""
    text = node.text
    if type == TextType.IMAGE:
        matches = extract_markdown_images(node.text)
    elif type == TextType.LINK:
        matches = extract_markdown_links(node.text)

    if len(matches) > 0:
        delimiter_count = len(matches)
        i = 0

        while delimiter_count > 0:
            if type == TextType.IMAGE:
                splitter = f"![{matches[i][0]}]({matches[i][1]})"
            elif type == TextType.LINK:
                splitter = f"[{matches[i][0]}]({matches[i][1]})" 
            else:
                raise Exception("incorrect type for reference node")
            
            nodes, text = split_the_ref_text(text, type, splitter, matches[i][0], matches[i][1])
            i += 1
            new_nodes.extend(nodes)
            delimiter_count -= 1

    if len(text) > 0:
        new_node = TextNode(text, TextType.NORMAL)
        new_nodes.append(new_node)
        
    return new_nodes

def split_the_text(delimiter, text, text_type, url=None):
    split = text.split(delimiter, maxsplit=2)
    new_nodes = []

    if len(split) == 1:
        new_nodes.append(TextNode(split[0], TextType.NORMAL))
        return new_nodes, text
    else: 
        if split[0] != "":
            new_nodes.append(TextNode(split[0], TextType.NORMAL, url))
        
        new_nodes.append(TextNode(split[1], text_type, url))
        text = split[2]

        return new_nodes, text
    
def split_the_ref_text(text, text_type, delimiter, alt, url=None):
    split = text.split(delimiter, maxsplit=1)
    new_nodes = []

    if len(split) == 1:
        new_nodes.append(TextNode(split[0], TextType.NORMAL))
        return new_nodes, text
    else: 
        if split[0] != "":
            new_nodes.append(TextNode(split[0], TextType.NORMAL))
        
        new_nodes.append(TextNode(alt, text_type, url))
        text = split[1]

        return new_nodes, text
    

text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
new_nodes = text_to_textnodes(text)