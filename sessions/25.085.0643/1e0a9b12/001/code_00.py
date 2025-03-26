"""
Applies gravity to each column independently. Non-white pixels fall down within their column until they hit the bottom edge of the grid or another non-white pixel. The relative vertical order of non-white pixels within a column is preserved. White pixels fill the remaining space above the stacked non-white pixels in each column.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by applying gravity to non-white pixels in each column.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier column slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_np = np.zeros_like(input_np)

    # Iterate through each column of the input grid
    for col_idx in range(width):
        # Get the current column
        column = input_np[:, col_idx]

        # Filter out the non-white pixels (values > 0) from the column
        # Keep them in their original top-to-bottom order
        non_white_pixels = [pixel for pixel in column if pixel != 0]

        # Determine the number of non-white pixels in this column
        num_non_white = len(non_white_pixels)

        # If there are any non-white pixels in this column
        if num_non_white > 0:
            # Place the non-white pixels at the bottom of the corresponding column
            # in the output grid, maintaining their relative order.
            # The index starts from height - num_non_white (the topmost position for the stack)
            # and goes down to height - 1 (the bottom row).
            output_np[height - num_non_white : height, col_idx] = non_white_pixels

    # Convert the numpy array output back to a list of lists
    output_grid = output_np.tolist()

    return output_grid