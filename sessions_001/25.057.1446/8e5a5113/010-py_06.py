"""
The leftmost block of non-zero colors is identified.  This block's sequence of colors, within each row, is then repeated across the rest of the row to the right.
"""

import numpy as np

def find_left_block(grid):
    """Finds the bounding box of the leftmost non-zero block."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = 0, 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the left block
    min_row, min_col, max_row, max_col = find_left_block(input_grid)
    block_width = max_col - min_col + 1

    # Propagate colors to the right (row-wise), repeating the sequence
    for r in range(rows):
        for c_fill in range(min_col, cols):
            # Calculate the index within the source block using modulo
            source_col = min_col + (c_fill - min_col) % block_width
            output_grid[r, c_fill] = input_grid[r, source_col]

    return output_grid