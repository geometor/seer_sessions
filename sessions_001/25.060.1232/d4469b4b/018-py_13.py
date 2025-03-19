"""
1. Count the number of green (value 3) pixels in the input grid.
2. The output grid has as many rows as the count of green + 1.
3. The output grid has a width equal to the height of the input minus 2.
4. Fill the output grid with gray (value 5) from bottom right, and upwards
   and to the left. The total number of gray pixels is equal to the count of
   green pixels in the input grid.
5. All other cells in the output grid are filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Count the number of green pixels (value 3).
    green_count = np.sum(input_grid == 3)

    # Determine output grid dimensions.
    output_height = green_count + 1
    output_width = input_grid.shape[0] - 2
    
    # Initialize the output grid filled with 0.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Fill output - create a solid block of the value '5' based on green count
    gray_count = green_count
    row = output_height -1
    col = output_width - 1

    # fill output with gray pixels until none left, moving from right-to-left
    # and bottom-to-top.
    while gray_count > 0:      
        output_grid[row,col] = 5
        gray_count -= 1
        col -= 1
        if col < 0:
            col = output_width - 1
            row -= 1
            if row < 0:
                break
    
    return output_grid