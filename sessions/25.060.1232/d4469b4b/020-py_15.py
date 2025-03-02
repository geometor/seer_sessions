"""
1.  Count Green: Determine the number of green (value 3) pixels in the input grid.
2.  Output Dimensions:
    *   The output grid's width is calculated as the input grid's height minus 2.
    *   The output grid has at most as many rows as the count of green + 1, and no more rows than input height - 2.
3.  Gray Placement: Place a number of gray (value 5) pixels in the output grid equal to the green count from step 1. The gray pixels do *not* follow a simple bottom-right fill. The placement logic needs to be clarified. *It appears that a solid block of gray pixels is formed, from bottom to top, and left to right.*
4. Zero Fill: All remaining cells in the output grid are filled with zeros (value 0).
5. Constraint: If the count of green pixels + 1 would result in more rows, then the output is capped.
"""

import numpy as np

def transform(input_grid):
    # Count the number of green pixels (value 3).
    green_count = np.sum(input_grid == 3)

    # Determine output grid dimensions.
    output_width = input_grid.shape[0] - 2
    output_height = min(green_count + 1, input_grid.shape[0] - 2)
    
    # Initialize the output grid filled with 0.
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Fill output - create a solid block of the value '5' based on green count
    gray_count = green_count
    row = output_height - 1
    col = 0

    # fill output with gray pixels until none left, moving from left-to-right
    # and bottom-to-top.
    while gray_count > 0:      
        output_grid[row,col] = 5
        gray_count -= 1
        col += 1
        if col >= output_width:
            col = 0
            row -= 1
            if row < 0:
                break
    
    return output_grid