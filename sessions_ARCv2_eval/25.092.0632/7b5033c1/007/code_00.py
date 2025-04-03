"""
Identifies the background color from the top-left pixel of the input grid, 
then scans the grid row by row, left to right, collecting all pixels that 
do not match the background color. These collected 'foreground' pixels are 
then arranged sequentially into a single-column output grid, preserving 
their original scan order.
"""

import numpy as np
from typing import List 

# Using List typing hint as the core structure, though numpy might be used internally 
# by the testing framework. The logic should be robust to either.

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Filters out the background color from the input grid and returns the 
    remaining pixels as a single column grid, maintaining scan order.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the 1-column output grid containing
        the non-background pixels in scan order. Returns an empty list if 
        the input is empty or contains only background pixels.
    """
    
    # Handle edge case: empty input grid
    if not input_grid or not input_grid[0]:
        return [] 

    # 1. Determine the background color from the top-left pixel.
    # Accessing [0][0] works for both list of lists and numpy arrays.
    background_color = input_grid[0][0]

    # 2. Initialize an empty list to store the foreground pixel colors.
    foreground_pixels = []

    # 3. Iterate through the input grid using row-major order (top-to-bottom, left-to-right).
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) # Assuming a rectangular grid
    
    for r in range(num_rows):
        for c in range(num_cols):
            # 4. Get the current pixel's color.
            # Accessing [r][c] works for both list of lists and numpy arrays.
            pixel = input_grid[r][c]
            
            # 5. Compare its value to the background_color.
            # This comparison should work correctly for scalar integers.
            if pixel != background_color:
                # 6. If different, add this pixel's color value to the foreground pixel list.
                foreground_pixels.append(pixel)

    # 7. Create the output grid. It will have one column.
    output_grid = []
    
    # 8. Populate the single column of the output grid using the collected foreground colors,
    #    maintaining the order. Each color becomes a single-element row.
    for color in foreground_pixels:
        output_grid.append([color])

    # Return the constructed output grid. If no foreground pixels were found, 
    # foreground_pixels will be empty, resulting in an empty output_grid, which is correct.
    return output_grid