"""
Identify one red (2) block and one orange (7) block. Consider a horizontal arrangement where the red and orange blocks are conceptually side-by-side. Note the number of white columns between the blocks, and the height. Insert an azure (8) block into the space between the red and orange blocks. The inserted azure block's width is based on number of white columns. The azure block matches the height of the space available.
"""

import numpy as np

def find_blocks(grid, color):
    # Find contiguous blocks of a specified color.
    blocks = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                block = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    row, col = stack.pop()
                    block.append((row, col))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color and not visited[nr, nc]:
                            stack.append((nr, nc))
                            visited[nr, nc] = True

                blocks.append(block)
    return blocks

def get_bounding_box(block):
    # Get the bounding box of a block.
    min_row = min(p[0] for p in block)
    max_row = max(p[0] for p in block)
    min_col = min(p[1] for p in block)
    max_col = max(p[1] for p in block)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the red and orange blocks.
    red_blocks = find_blocks(input_grid, 2)
    orange_blocks = find_blocks(input_grid, 7)
    
    # this task assumes existence of these two blocks
    if not red_blocks or not orange_blocks:
        return output_grid

    # Get bounding boxes for first found blocks of each color.
    red_min_row, red_max_row, red_min_col, red_max_col = get_bounding_box(red_blocks[0])
    orange_min_row, orange_max_row, orange_min_col, orange_max_col = get_bounding_box(orange_blocks[0])

    # Determine the region for the azure block - horizontal insertion
    azure_min_col = red_max_col + 1
    azure_max_col = orange_min_col - 1
    
    azure_min_row = 0 # top of grid
    azure_max_row = rows - 1 # bottom of grid
    
    # Create the azure block.
    for r in range(azure_min_row, azure_max_row + 1):
        for c in range(azure_min_col, azure_max_col + 1):
            if 0 <= r < rows and 0 <= c < cols: # ensure within grid:
                output_grid[r, c] = 8

    return output_grid