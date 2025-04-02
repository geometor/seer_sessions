"""
Transformation Rule:

Iterate through the input 1D grid (vector). For each position `i` (excluding the first and last elements), check if the triplet of pixels at indices `i-1`, `i`, and `i+1` matches the pattern [white, C, white], where C is any non-white color (1-9). If this pattern is found, replace this triplet in the output grid with [C, C, C]. All other pixels remain unchanged from the input.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to a 1D input grid.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input grid.

    Returns:
        list: The transformed 1D grid.
    """
    # Ensure input is a list for easier manipulation if it's numpy array
    if isinstance(input_grid, np.ndarray):
        # Assuming it's a 1D array or a 2D array with one row
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
             input_list = input_grid[0].tolist()
        elif input_grid.ndim == 1:
             input_list = input_grid.tolist()
        else:
             # Handle potential unexpected shapes if necessary, maybe raise error
             # For now, assume it fits the 1D pattern described
             raise ValueError("Input grid is not 1-dimensional or a single row.")
    else:
        input_list = list(input_grid) # Ensure it's a mutable list copy

    # Initialize output_grid as a copy of the input list
    output_grid = list(input_list)
    grid_length = len(input_list)

    # Define white color value
    white = 0

    # Iterate through the grid, checking triplets
    # We need to look at i-1, i, i+1, so we iterate from index 1 up to index length-2
    for i in range(1, grid_length - 1):
        # Get the colors of the triplet from the *original* input grid
        left_pixel = input_list[i-1]
        center_pixel = input_list[i]
        right_pixel = input_list[i+1]

        # Check if the pattern [white, C, white] is matched, where C is not white
        if left_pixel == white and center_pixel != white and right_pixel == white:
            # Apply the transformation: replace [white, C, white] with [C, C, C] in the output_grid
            output_grid[i-1] = center_pixel
            output_grid[i] = center_pixel
            output_grid[i+1] = center_pixel
            # Note: We modify the output_grid, not the input_list we are iterating over,
            # to avoid cascading effects within a single pass if patterns overlap
            # in ways that might interact (though not apparent in these examples).

    # Return the modified output grid
    return output_grid
