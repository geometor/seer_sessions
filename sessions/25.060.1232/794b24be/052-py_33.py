"""
1.  Iterate through each pixel of the input grid.
2.  White Pixels: If a pixel is white (0), it remains white (0) in the output grid.
3.  Blue Pixels - Top Row Contiguous Blocks: If a pixel is blue (1) and is located
    in the top row (row index 0), and part of the block is 2 or more pixels,
    change the color of the entire block to red(2).
4.  Blue Pixels - Single Pixel 2nd or 3rd Row: If a blue pixel is in the second
    or third row (row index 1 or 2) and part of a contiguous block, change the
    color to white (0).
5.  Blue Pixels - Contiguous Blocks not Top Row: If a blue pixel is not in the
    top row and part of the block is 2 or more pixels, change the color of the
    entire block to red(2).
6.  Blue Pixel - Single: Change any other single blue cell to red (2)
7.  Output: The output grid is created by applying these transformations.
"""

import numpy as np

def get_contiguous_blocks(grid, color):
    """
    Finds contiguous blocks of the specified color in the grid.
    Returns a list of sets, where each set contains the coordinates of a contiguous block.
    """
    visited = set()
    blocks = []

    def dfs(row, col, current_block):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_block.add((row, col))
        dfs(row + 1, col, current_block)
        dfs(row - 1, col, current_block)
        dfs(row, col + 1, current_block)
        dfs(row, col - 1, current_block)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_block = set()
                dfs(row, col, current_block)
                blocks.append(current_block)
    return blocks

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find contiguous blue blocks
    blue_blocks = get_contiguous_blocks(input_grid, 1)

    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            # White Pixels
            if input_grid[r,c] == 0:
                output_grid[r,c] = 0
            # Blue Pixels
            elif input_grid[r,c] == 1:
                is_single = True
                for block in blue_blocks:
                    if (r,c) in block:
                        if len(block) >= 2:
                            is_single = False
                            # Top Row Contiguous
                            if r == 0:
                                for cell in block:
                                    output_grid[cell] = 2
                            # Contiguous Blocks not Top Row
                            else:
                                for cell in block:
                                    output_grid[cell] = 2
                        
                # Single Pixel 2nd or 3rd Row
                if is_single and (r == 1 or r==2):
                        output_grid[r,c] = 0
                # Single
                elif is_single:
                    output_grid[r,c] = 2

    return output_grid