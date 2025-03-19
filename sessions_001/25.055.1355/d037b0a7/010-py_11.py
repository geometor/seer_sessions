"""
1. Copy the first row of the input grid to the first row of the output grid.
2. Copy the second row of the input grid to the second row of the output grid.
3. Find the central pixel(s) of the second row of the output grid. If the grid width is even, there will be two central pixels; if odd, there will be one.
4. Replace the color(s) of the central pixel(s) of the second row of the output grid with the color(s) of the central pixel(s) of the *first* row.
5. Copy the modified second row of the output grid to the third row of the output grid.
6. Set all rows from the forth row on to be all black/empty/zeros
"""

import numpy as np

def get_center_pixel_indices(width):
    # Helper function to calculate the index/indices of the center pixel(s)
    if width % 2 == 0:  # Even width
        return [width // 2 - 1, width // 2]
    else:  # Odd width
        return [width // 2]

def transform(input_grid):
    # Initialize output_grid as a copy of the input, but with all zeros beyond the third row
    output_grid = np.zeros_like(input_grid)

    # 1. Copy the first row
    output_grid[0] = input_grid[0]

    # 2. Copy the second row
    output_grid[1] = input_grid[1]
    
    # 3. & 4. Find and replace central pixel(s)
    width = input_grid.shape[1]
    center_indices = get_center_pixel_indices(width)
    for i in center_indices:
        output_grid[1, i] = input_grid[0, i]


    # 5. Copy the modified second row to the third row
    if input_grid.shape[0] > 2:
        output_grid[2] = output_grid[1]


    return output_grid