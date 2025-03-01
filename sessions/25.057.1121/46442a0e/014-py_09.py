"""
The input grid is expanded into a larger 6x6 grid. The core 3x3 input is copied to the center.
The border is created from an alternating pattern from the top row and the top right corner of the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Copy the input grid into the center of the output grid.
    output_grid[1:4, 1:4] = input_grid

    # Create the frame
    # Top row
    output_grid[0, 0] = input_grid[0, 0]  # 6
    output_grid[0, 1] = input_grid[0, 1]  # 9
    output_grid[0, 2] = input_grid[0, 2]  # 9
    output_grid[0, 3] = input_grid[0, 0]  # 6
    output_grid[0, 4] = input_grid[0, 0]  # 6
    output_grid[0, 5] = input_grid[0, 0]  # 6

    # Left and right borders, excluding the corners already filled.
    output_grid[1, 0] = input_grid[0, 0]  # 6
    output_grid[2, 0] = input_grid[0, 0]  # 6

    output_grid[1, 5] = input_grid[0, 2]  # 9
    output_grid[2, 5] = input_grid[0, 2]  # 9

    output_grid[3, 0] = input_grid[0, 2]  # 9
    output_grid[4, 0] = input_grid[0, 2]  # 9
    
    output_grid[3, 5] = input_grid[0, 0]  # 6
    output_grid[4, 5] = input_grid[0, 0]  # 6

    # Bottom row
    output_grid[5, 0] = input_grid[0, 0]  # 6
    output_grid[5, 1] = input_grid[0, 0]  # 6
    output_grid[5, 2] = input_grid[0, 0]  # 6
    output_grid[5, 3] = input_grid[0, 1]  # 9
    output_grid[5, 4] = input_grid[0, 2]  # 9
    output_grid[5, 5] = input_grid[0,0]   #9

    return output_grid