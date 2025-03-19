"""
1.  **Divide Input Vertically:** Divide the input grid into vertical blocks. Considering white spaces as delimiters, in the given example, the block length can be identified as 4.
2.  **Analyze Rows in blocks:** For each block.
    *   If a row exists filled with only gray, encode the number 8.
    *   If a row exists in which the second and third pixel is white, encode the number 2.
    *   If the entire block does not satisfy any condition above, encode 4.
3.  **Construct Output:** Create a 3x3 output grid. Each row in it represents the extracted information using rules from step 2 for first three blocks vertically.
"""

import numpy as np

def get_blocks(grid, block_width):
    blocks = []
    for i in range(0, grid.shape[1], block_width):
        block = grid[:, i:i+block_width]
        blocks.append(block)
    return blocks

def analyze_block(block):
    # If a row exists filled with only gray (5), encode 8.
    for row in block:
        if np.all(row == 5):
            return 8
    # If a row exists in which the second and third pixel is white (0), encode 2.
    for row in block:
        if row[1] == 0 and row[2] == 0:
            return 2
    # If the entire block does not satisfy any condition above, encode 4.       
    return 4

def transform(input_grid):
    """
    Transforms the input grid according to the defined rules.
    """
    input_grid = np.array(input_grid)
    block_width = 4
    blocks = get_blocks(input_grid, block_width)
    output_grid = np.zeros((3, 3), dtype=int)

    # Process only first three blocks
    for i in range(min(3, len(blocks))):  # Limit to 3 blocks
      block_code = analyze_block(blocks[i])
      output_grid[i,:] = block_code


    return output_grid.tolist()