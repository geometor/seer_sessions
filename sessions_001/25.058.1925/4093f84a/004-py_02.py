"""
The transformation rule is as follows:

1. Identify the constant horizontal gray (5) block in the middle of the input grid.
2. Locate all red (2) pixels within the input grid.
3. Replace the red (2) pixels from the input grid and copy to the output grid in the same positions, but use gray (5).
4. The constant horizontal gray (5) block that exists in the input grid is copied unchanged to the output grid.
5. All other cells are white (0).
"""

import numpy as np

def find_gray_block(grid):
    # Find rows that are all gray (5)
    gray_rows = []
    for i, row in enumerate(grid):
        if np.all(row == 5):
            gray_rows.append(i)
    return gray_rows

def find_red_pixels(grid):
    # Find coordinates of red (2) pixels
    red_coords = []
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if pixel == 2:
                red_coords.append((i, j))
    return red_coords
    

def transform(input_grid):
    # Initialize output_grid as all white (0)
    output_grid = np.zeros_like(input_grid)

    # Find the gray block rows
    gray_rows = find_gray_block(input_grid)
    
    # Copy the gray block to the output grid
    for row_index in gray_rows:
        output_grid[row_index, :] = 5

    # Find red pixel coordinates
    red_pixels = find_red_pixels(input_grid)

    # Replace red pixels with gray in the output grid
    for row, col in red_pixels:
        output_grid[row, col] = 5

    return output_grid