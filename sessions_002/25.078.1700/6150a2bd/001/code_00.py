"""
Rotate the input grid 90 degrees counter-clockwise to obtain the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array
    input_np = np.array(input_grid)
    
    # Get the dimensions of the input grid
    height, width = input_np.shape
    
    # Initialize the output grid with the same dimensions, filled with zeros
    output_np = np.zeros_like(input_np)

    # Rotate the grid 90 degrees counter-clockwise
    # The new x coordinate is the original y coordinate
    # The new y coordinate is the original width - x coordinate - 1
    for x in range(height):
        for y in range(width):
            output_np[height - 1 - y, x] = input_np[x, y]

    #convert to list
    output_grid = output_np.tolist()
    return output_grid