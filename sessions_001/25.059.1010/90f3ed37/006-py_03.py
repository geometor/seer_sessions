"""
1.  **Identify:** Locate all azure (8) pixels within the input grid.
2.  **Preserve:** Copy entire input to output, keeping azure pixels.
3.  **Iterate:** For each contiguous horizontal block of azure pixels:
4.  **Calculate Offset:** Determine the row difference (offset) between the azure block and its corresponding blue block. The offset is consistently 2 for all examples.
5.  **Create Blue Block:** Add a horizontal line filled with blue pixels (1) with the same shape (width) as the azure block.
6. **Apply Offset:** Position the blue block `offset` rows below the azure block.

"""

import numpy as np

def find_horizontal_blocks(grid, color):
    blocks = []
    rows, cols = grid.shape
    for r in range(rows):
        start_col = None
        for c in range(cols):
            if grid[r, c] == color:
                if start_col is None:
                    start_col = c
            elif start_col is not None:
                blocks.append(((r, start_col), (r, c - 1)))
                start_col = None
        if start_col is not None:
            blocks.append(((r, start_col), (r, cols - 1)))
    return blocks

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find horizontal blocks of azure pixels
    azure_blocks = find_horizontal_blocks(input_grid, 8)

    # Iterate through each block and add blue pixels with a fixed offset of 2
    for start, end in azure_blocks:
        row_start, col_start = start
        row_end, col_end = end
        
        block_width = col_end - col_start + 1
        offset = 2
        new_row = row_start + offset
        
        # Check if the new row is within bounds
        if new_row < rows:
            output_grid[new_row, col_start:col_start + block_width] = 1

    return output_grid