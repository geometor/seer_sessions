"""
1.  **Identify Blocks:** Find all contiguous blocks of red (2) pixels and orange (7) pixels within the input grid.
2.  **Select Blocks**: If multiple blocks, take the first red and first orange.
3.  **Horizontal Bounds:** Determine the horizontal boundaries for the azure (8) block. The starting column is one position to the right of the rightmost edge of the red block. The ending column is one position to the left of the leftmost edge of the orange block.
4.  **Vertical Bounds:** Determine the vertical boundaries for the azure block. Find the maximum of the top row indices of the red and orange blocks, and use as top. Find the minimum of the bottom row indices of the red and orange blocks, and use as bottom.
5.  **Insert Azure Block:** Within the calculated horizontal and vertical bounds, replace the existing pixel values with azure (8) to create the new block.
6.  **Output:** Return the modified grid.
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

    # Determine the horizontal region for the azure block.
    azure_min_col = red_max_col + 1
    azure_max_col = orange_min_col - 1

    # Determine the vertical region for the azure block.
    azure_min_row = max(red_min_row, orange_min_row)
    azure_max_row = min(red_max_row, orange_max_row)

    # Create the azure block.
    for r in range(azure_min_row, azure_max_row + 1):
        for c in range(azure_min_col, azure_max_col + 1):
            if 0 <= r < rows and 0 <= c < cols: # ensure within grid
                output_grid[r, c] = 8

    return output_grid