```python
"""
The transformation rule is: For each contiguous block of '2' (red) pixels,
identify the lowest, rightmost pixel of the block, and change its color to '1' (blue).
All other pixels remain unchanged.
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

def find_bottom_right_pixel(block):
    """Finds the bottom-rightmost pixel in a block."""
    bottom_right_pixel = block[0]
    for pixel in block:
        if pixel[0] > bottom_right_pixel[0]:
            bottom_right_pixel = pixel
        elif pixel[0] == bottom_right_pixel[0] and pixel[1] > bottom_right_pixel[1]:
            bottom_right_pixel = pixel
    return bottom_right_pixel

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    red_blocks = find_contiguous_blocks(output_grid, 2)  # Find all contiguous red blocks

    for block in red_blocks:
        bottom_right = find_bottom_right_pixel(block) # Find the bottom-right pixel of the current block
        output_grid[bottom_right] = 1   # Change its color to blue

    return output_grid
```