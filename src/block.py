from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERD_LIST = "unordered_list"
    ORDERD_LIST = "ordered_list"
