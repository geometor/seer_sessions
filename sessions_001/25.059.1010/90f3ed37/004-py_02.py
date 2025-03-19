"""
1.  **Identify:** Locate all azure (8) pixels within the input grid.
2.  **Preserve:** Copy entire input to output, keeping azure pixels.
3.  **Iterate:** For each contiguous horizontal block of azure pixels:
4.  **Calculate:** Add a horizontal line filled with blue pixels(1) that matches the same shape, width and starting row of the azure object.
5.  **Determine Row:** Find objects with an origin row (lowest y value) that is 4 or less, offset + 5. Find objects with row position 4-9, add row offset +3.
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

    # Iterate through each block and add blue pixels
    for start, end in azure_blocks:
        row_start, col_start = start
        row_end, col_end = end
        
        block_width = col_end - col_start + 1

        # Determine offset based on row number
        if row_start <=4:
            offset = 5
        elif row_start <=9:
            offset = 3
        else:
            offset=0
        
        new_row = row_start + offset
        
        # Check if the new row is within bounds
        if new_row < rows:
            output_grid[new_row, col_start:col_start + block_width] = 1

    return output_grid