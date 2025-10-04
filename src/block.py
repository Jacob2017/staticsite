from enum import Enum


class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block_md: str) -> BlockType:
    
