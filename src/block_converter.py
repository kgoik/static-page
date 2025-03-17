from block import BlockType
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        if block.strip() == "":
            continue
        block = block.strip()
        clean_blocks.append(block)

    return clean_blocks

def block_to_block_type(block):
    
    header_regex = r"^#{1,6} "
    code_regex = r"^`{3}[^`].*[^`]`{3}$"

    if re.search(header_regex, block):
        return BlockType.HEADING
    elif is_code_block(block):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unorderd_list_block(block):
        return BlockType.UNORDERD_LIST
    elif is_orderd_list_block(block):
        return BlockType.ORDERD_LIST
    else:
        return BlockType.PARAGRAPH

def is_code_block(block):
    lines = block.split("\n")
    return len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```")

def is_quote_block(block):
    lines = block.split('\n')
    return all(line.startswith('>') for line in lines)

def is_unorderd_list_block(block):
    lines = block.split('\n')
    return all(line.startswith('- ') for line in lines)

def is_orderd_list_block(block):
    lines = block.split('\n')
    i = 1
    for line in lines:
        if not line.startswith(f'{i}. '):
            return False
        i += 1
    return True

def heading_level(block, type):
    if block == None or block.strip() == "":
        raise Exception("block cannot be empty")

    if type != BlockType.HEADING:
        raise ValueError("Block type must be HEADING")
    
    heading = block.split(" ")[0]

    return len(heading)