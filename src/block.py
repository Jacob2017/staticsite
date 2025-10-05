import re
from enum import Enum


class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def block_to_block_type(block_md: str) -> BlockType:
    if check_heading(block_md):
        return BlockType.HEADING
    if check_code(block_md):
        return BlockType.CODE
    if check_quote(block_md):
        return BlockType.QUOTE
    if check_ulist(block_md):
        return BlockType.ULIST
    if check_olist(block_md):
        return BlockType.OLIST
    return BlockType.PARA


def check_heading(block_md: str) -> bool:
    pattern = r"^#{1,6}\s+(.+)"
    matches = re.findall(pattern, block_md)
    if matches:
        return True
    return False


def check_code(block_md: str) -> bool:
    if block_md.startswith("```") and block_md.endswith("```"):
        return True
    return False


def check_quote(block_md: str) -> bool:
    for line in block_md.split("\n"):
        if not line.startswith(">"):
            return False
    return True


def check_ulist(block_md: str) -> bool:
    for line in block_md.split("\n"):
        if not line.startswith("- "):
            return False
    return True


def check_olist(block_md: str) -> bool:
    for line_num, line in enumerate(block_md.split("\n"), 1):
        if not line.startswith(f"{line_num}. "):
            return False
    return True
