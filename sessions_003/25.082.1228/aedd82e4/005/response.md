```python
"""
1.  **Identify Contiguous Blocks:** Find all contiguous blocks of red (2) pixels in the input grid. A contiguous block is defined as a group of one or more red pixels that are directly adjacent horizontally or vertically (not diagonally).
2.  **Determine Target Pixel:** For each contiguous red block, identify the pixel that should be changed to blue (1).
    *   If the red block contains only one pixel, it becomes blue.
    *   If the block has a single "bottom" row pixel, and a single "rightmost" column pixel, make that blue.
    *   If the block has a connected pixel to the right on any row above, but not directly above, then the pixel to change is on the lowest row, and furthest right.

3.  **Change Pixel Color:** Change the color of the identified target pixel in each block from red (2) to blue (1). All other pixels in the grid retain their original colors.
"""

import numpy as np

def find_contiguous_blocks(grid, color):
    """Finds contiguous blocks of a specific color in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    def dfs(row, col, current_block):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_block.append((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_block = []
                dfs(row, col, current_block)
                blocks.append(current_block)
    return blocks

def determine_target_pixel(block):
    """Determines the target pixel to change to blue."""
    if len(block) == 1:
        return block[0]

    # Find the lowest row and rightmost column
    min_row = min(pixel[0] for pixel in block)
    max_row = max(pixel[0] for pixel in block)
    min_col = min(pixel[1] for pixel in block)
    max_col = max(pixel[1] for pixel in block)

    # Create set for quick lookup.
    block_set = set(block)

    # Find pixels on lowest row
    lowest_row_pixels = [pixel for pixel in block if pixel[0] == max_row]
    
    if len(lowest_row_pixels) > 0:
      target =  max(lowest_row_pixels, key=lambda p: p[1])
      return target

    return (max_row, max_col)  #Should never reach here.

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    red_blocks = find_contiguous_blocks(output_grid, 2)  # Find all contiguous red blocks

    for block in red_blocks:
        target_pixel = determine_target_pixel(block) # Find the target pixel
        output_grid[target_pixel] = 1   # Change its color to blue

    return output_grid
```