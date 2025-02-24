"""
If the input grid is 3x3, rotate it 90 degrees counter-clockwise. Otherwise, return the input grid unchanged.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)
    
    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape
    
    # Check if the input grid is 3x3.
    if input_height == 3 and input_width == 3:
        # Initialize the output grid with swapped dimensions.
        output_grid = np.zeros((input_width, input_height), dtype=int)

        # Iterate through the input grid and perform the rotation.
        for x in range(input_height):
            for y in range(input_width):
                # Calculate the new position of the pixel after rotation.
                new_x = y
                new_y = input_height - 1 - x
                
                # Place the pixel's value in the output grid at its new position.
                output_grid[new_x, new_y] = input_grid[x, y]
    else:
        # Otherwise, return the input grid unchanged.
        output_grid = input_grid.copy()

    return output_grid.tolist()