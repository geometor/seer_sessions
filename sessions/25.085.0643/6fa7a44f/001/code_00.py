"""
Generate an output grid by stacking the input grid on top of its vertical reflection.
The output grid has the same width as the input grid and twice the height.
The top half of the output grid is a direct copy of the input grid.
The bottom half of the output grid is the input grid flipped vertically (upside down).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking it on top of its vertical reflection.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Create a vertically reflected copy of the input array
    # np.flipud flips the array vertically (up/down)
    reflected_array = np.flipud(input_array)

    # Concatenate the original array and the reflected array vertically
    # np.vstack stacks arrays in sequence vertically (row wise)
    output_array = np.vstack((input_array, reflected_array))

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
