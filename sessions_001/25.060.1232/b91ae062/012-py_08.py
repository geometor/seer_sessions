"""
Transforms an input grid into an output grid by expanding each pixel in the input to a 2x2 block of the same color in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Expands each pixel of the input grid into a 2x2 block in the output grid.
    """
    # Get input grid dimensions
    input_height, input_width = input_grid.shape
    
    # Calculate output grid dimensions (twice the size of input)
    output_height, output_width = input_height * 2, input_width * 2
    
    # Initialize the output grid with zeros and the correct dimensions
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for row in range(input_height):
        for col in range(input_width):
            # Get color of current input pixel
            color = input_grid[row, col]

            # Expand the pixel to 2x2 block in output grid
            output_grid[2*row:2*row+2, 2*col:2*col+2] = color

    return output_grid