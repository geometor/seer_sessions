"""
Replace color 9 in a color block with the block's original color.
"""

import numpy as np

def find_contiguous_block(grid, start_row, start_col, color):
    """
    Finds a contiguous block of the given color starting from a given cell.
    Uses a depth-first search approach.
    """
    rows, cols = grid.shape
    block_pixels = []
    visited = set()
    stack = [(start_row, start_col)]

    while stack:
        r, c = stack.pop()
        if (r, c) in visited:
            continue
        visited.add((r, c))

        if 0 <= r < rows and 0 <= c < cols and grid[r, c] == color:
            block_pixels.append((r, c))
            # Add adjacent cells to the stack
            stack.append((r + 1, c))
            stack.append((r - 1, c))
            stack.append((r, c + 1))
            stack.append((r, c - 1))
    return block_pixels

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    visited = set()

    for r in range(rows):
        for c in range(cols):
            if (r,c) not in visited and input_grid[r,c] != 0 and input_grid[r,c]!=9:
                block = find_contiguous_block(input_grid, r, c, input_grid[r,c])
                visited.update(block)
                if any(input_grid[x,y] == 9 for x,y in block):
                     block9 = find_contiguous_block(input_grid, *next((x,y) for x,y in block if input_grid[x,y] == 9), 9)
                     for x,y in block9:
                          output_grid[x,y] = input_grid[r,c]




    return output_grid.tolist()