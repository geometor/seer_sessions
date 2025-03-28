"""
This module defines a function to transform a 6x6 input grid into a 3x3 output grid.
The transformation rule involves sampling pixels from the input grid at specific coordinates.
Specifically, the pixel at position (r_out, c_out) in the 3x3 output grid corresponds to
the pixel at position (r_out * 2, c_out * 2) in the 6x6 input grid. The colors of the
sampled pixels are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 6x6 input grid to a 3x3 output grid by sampling pixels.

    Args:
        input_grid (list of lists or numpy array): The 6x6 input grid.

    Returns:
        numpy array: The transformed 3x3 output grid.
    """
    # Convert input to a numpy array for easier indexing
    input_array = np.array(input_grid, dtype=int)

    # Determine the dimensions of the input and output grids
    # Input is assumed to be 6x6 based on examples, output is 3x3
    output_height = 3
    output_width = 3

    # Initialize the output grid with zeros (white)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the output grid
    for r_out in range(output_height):
        for c_out in range(output_width):
            # Calculate the corresponding coordinates in the input grid
            r_in = r_out * 2
            c_in = c_out * 2

            # Copy the pixel value from the input grid to the output grid
            # Check bounds just in case, although for 6x6 -> 3x3 it's guaranteed
            if 0 <= r_in < input_array.shape[0] and 0 <= c_in < input_array.shape[1]:
                output_grid[r_out, c_out] = input_array[r_in, c_in]

    return output_grid.tolist() # Convert back to list of lists as per typical ARC format