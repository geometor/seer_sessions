"""
1.  **Identify Separator:** Find the horizontal row of yellow (4) pixels that divides the input grid into two regions: a "top region" and a "bottom region".
2.  **Determine Output Size:** The output grid has the same dimensions (height and width) as the *bottom region* of the input grid.
3.  **Copy and Transform:** The output is created based on values in the *top region* with the same dimensions.
4.  **Color Mapping**: For each cell in the *top region:* If an input cell at (row, col) is blue (1), then the output cell at (row, col) becomes green (3). If an input cell is white (0) it can be transformed to either white (0) or blue (3) based on the mapping of the bottom section.
5. **Final Result:** The result is the transformed output.
"""

import numpy as np

def find_yellow_row(grid):
    """Finds the row index of the first all-yellow (4) row."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return i
    return None

def transform(input_grid):
    # Identify Separator: Find the yellow row.
    yellow_row_index = find_yellow_row(input_grid)

    # Determine Output Size: Based on the bottom region.
    top_height = yellow_row_index
    bottom_height = input_grid.shape[0] - yellow_row_index - 1
    output_height = bottom_height
    output_width = input_grid.shape[1]

    # Initialize the output grid.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy and Transform: Iterate through the top region.
    for i in range(top_height):
        for j in range(output_width):
            # Color Mapping
            if input_grid[i, j] == 1:  # Blue to green
                output_grid[i, j] = 3
            elif input_grid[i,j] == 0:
                output_grid[i,j] = input_grid[i,j] # start by copying
            else:
                 output_grid[i,j] = input_grid[i,j]


    return output_grid