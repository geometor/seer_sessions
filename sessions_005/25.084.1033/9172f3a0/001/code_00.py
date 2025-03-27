"""
Transforms an input grid by scaling it up by a factor of 3.
Each pixel in the input grid is expanded into a 3x3 block of the same color 
in the output grid. The output grid's height and width are 3 times the 
input grid's height and width, respectively.
"""

import numpy as np

def transform(input_grid):
    """
    Scales up the input grid by a factor of 3.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the scaled-up output grid.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_array = np.array(input_grid, dtype=int)
    input_height, input_width = input_array.shape

    # Calculate the dimensions of the output grid
    output_height = input_height * 3
    output_width = input_width * 3

    # Initialize the output grid with zeros. 
    # Using numpy makes initialization and assignment easier.
    output_array = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_array[r, c]

            # Calculate the top-left corner coordinates (R, C) for the 
            # corresponding 3x3 block in the output grid
            output_r_start = r * 3
            output_c_start = c * 3

            # Fill the 3x3 block in the output grid with the input pixel's color.
            # Numpy slicing [start_row:end_row, start_col:end_col] is used.
            # Note: end_row and end_col are exclusive.
            output_array[output_r_start : output_r_start + 3, output_c_start : output_c_start + 3] = color

    # Convert the resulting numpy array back to a list of lists 
    # as required by the ARC framework standard format.
    output_grid = output_array.tolist()

    return output_grid