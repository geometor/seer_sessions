"""
Transforms an input grid based on the presence of '2' (red). 
The transformation involves mirroring across the x and y axis.
"""

import numpy as np

def get_mirrored_position(pos, max_len):
    """
    calculate mirrored position
    """
    return max_len - 1 - pos

def transform(input_grid):
    """
    find all "2"s and mirror them across the x and y axis 
    with positions and values set by these rules:

    y axis mirroring:
    - at mirrored y position 1 set to output "3"
    - at mirrored y position 2 set to output "6"
    x axis mirroring:
    - at mirrored x position 1 set to output "8"
    - at mirrored x position 2 set to output "7"

    all non 2 values are copied to the ouput
    """
    # Initialize output grid with the same dimensions and values as the input grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the input grid
    for row in range(rows):
        for col in range(cols):
            if input_grid[row][col] == 2:
                # y axis
                mirrored_y = get_mirrored_position(col, cols)
                if mirrored_y < col:
                    output_grid[row][mirrored_y] = 3
                elif mirrored_y > col:
                    output_grid[row][get_mirrored_position(mirrored_y, cols)] = 6
                    
                # x axis
                mirrored_x = get_mirrored_position(row, rows)
                if mirrored_x < row:
                    output_grid[mirrored_x][col] = 8
                elif mirrored_x > row:
                    output_grid[get_mirrored_position(mirrored_x,rows)][col] = 7

    return output_grid