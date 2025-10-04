from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
    str_list = [block.strip() for block in markdown.split("\n\n")]
    return [block for block in str_list if not (block.isspace() or len(block) == 0)]
