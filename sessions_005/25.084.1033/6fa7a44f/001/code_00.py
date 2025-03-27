"""
Construct the output grid by stacking the original input grid on top of a vertically flipped version of the input grid. The height of the output grid will be twice the height of the input grid, while the width remains the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by stacking it on top of its vertical reflection.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Create a vertically flipped version of the input array
    # np.flipud reverses the order of rows (flips along the up-down axis)
    flipped_array = np.flipud(input_array)

    # Concatenate the original input array and the flipped array vertically
    # np.vstack stacks arrays in sequence vertically (row-wise)
    output_array = np.vstack((input_array, flipped_array))

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
