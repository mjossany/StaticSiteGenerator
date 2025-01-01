def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks]
    filtered_blocks = [block for block in stripped_blocks if block]
    return filtered_blocks