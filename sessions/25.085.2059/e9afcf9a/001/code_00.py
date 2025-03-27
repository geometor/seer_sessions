"""
Transforms an input grid consisting of two solid-colored rows into an output grid
of the same dimensions where the colors alternate in a checkerboard pattern.
The top row starts with the color of the original top row, and the bottom row
starts with the color of the original bottom row.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the checkerboard transformation based on the two input row colors.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
                                 Expected to have 2 rows.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Identify the color of the first row (Color1)
    color1 = input_grid[0, 0]

    # Identify the color of the second row (Color2)
    color2 = input_grid[1, 0]

    # Create a new output grid with the same dimensions, initialized with zeros
    # (or any placeholder, as it will be fully overwritten)
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each column index 'c' from 0 to width-1
    for c in range(width):
        # Check if the column index 'c' is even or odd
        if c % 2 == 0:  # Even column index
            # Set the pixel at (row=0, column=c) to Color1
            output_grid[0, c] = color1
            # Set the pixel at (row=1, column=c) to Color2
            output_grid[1, c] = color2
        else:  # Odd column index
            # Set the pixel at (row=0, column=c) to Color2
            output_grid[0, c] = color2
            # Set the pixel at (row=1, column=c) to Color1
            output_grid[1, c] = color1

    # Return the resulting output grid
    return output_grid