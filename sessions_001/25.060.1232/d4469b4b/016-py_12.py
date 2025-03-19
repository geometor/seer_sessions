"""
1. Count: Count the number of green (value 3) pixels in the input grid.
2. Compress: Reduce the grid size from 5x5 to 3x3.
3. Fill output: If the green count is greater than 0, fill the bottom right
   corner cells with the value 5, in a square, the amount of pixels equals the
   count of the green. Fill all other cells with zero.
"""

import numpy as np

def transform(input_grid):
    # Count the number of green pixels (value 3).
    green_count = np.sum(input_grid == 3)

    # Initialize a 3x3 output grid filled with 0.
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Fill output - create a solid square of the value '5' based on green count
    if green_count > 0:
        side = int(np.sqrt(green_count))
        if side <= 3:          
            output_grid[-side:, -side:] = 5
        else:
            output_grid[:,:] = 5


    return output_grid