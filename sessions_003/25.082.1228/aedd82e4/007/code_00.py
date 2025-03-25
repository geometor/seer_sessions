"""
1.  **Identify Red Blocks:** Find all contiguous blocks of red (2) pixels in the input grid.  A contiguous block is a group of red pixels that are directly adjacent horizontally or vertically (not diagonally). Each disjoint block is treated separately.

2.  **Determine Target Pixel:** For each contiguous red block, identify the pixel that should be changed to blue (1).
    *   If the red block contains only *one* pixel, that pixel is the target.
    *   Otherwise, the target pixel is the one located at the *bottom-most* row and, among those, the *right-most* column occupied by the red block.

3.  **Change Pixel Color:** Change the color of the identified target pixel in each block from red (2) to blue (1).  All other pixels in the grid remain unchanged.
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
    """Determines the target pixel (bottom-most, then right-most)."""
    if len(block) == 1:
        return block[0]

    # Find the lowest row (max row index)
    max_row = max(pixel[0] for pixel in block)
    # Get all pixels on the lowest row
    lowest_row_pixels = [pixel for pixel in block if pixel[0] == max_row]
    # Find the rightmost column (max col index) among the lowest row pixels
    target_pixel = max(lowest_row_pixels, key=lambda p: p[1])
    return target_pixel

def transform(input_grid):
    """Transforms the input grid by changing one red pixel to blue in each contiguous red block."""
    output_grid = np.copy(input_grid)
    red_blocks = find_contiguous_blocks(output_grid, 2)  # Find all contiguous red blocks

    for block in red_blocks:
        target_pixel = determine_target_pixel(block) # Determine the target pixel (bottom-right)
        output_grid[target_pixel] = 1   # Change the target pixel to blue

    return output_grid