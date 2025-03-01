"""
1.  **Initialization:** Create an output grid filled with black (0) pixels, having the same dimensions as the input grid.
2.  **Identify Azure Blocks:** Locate all horizontal, contiguous blocks of azure (8) pixels in the input grid.
3.  **Iterate:** For each identified azure block:
    *   **Create Blue Block:** Create a horizontal line of blue (1) pixels with the same width as the azure block.
    *   **Position Blue Block:** Place the newly created blue block one row directly below the corresponding azure block.
4. **Return** Return the output grid.
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
    # initialize output_grid as all black (0)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find horizontal blocks of azure pixels
    azure_blocks = find_horizontal_blocks(input_grid, 8)

    # Iterate through each block and add blue pixels one row below
    for start, end in azure_blocks:
        row_start, col_start = start
        row_end, col_end = end
        
        block_width = col_end - col_start + 1
        new_row = row_start + 1  # One row below
        
        # Check if the new row is within bounds
        if new_row < rows:
            output_grid[new_row, col_start:col_start + block_width] = 1

    return output_grid