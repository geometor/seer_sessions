"""
This module transforms an input grid based on the count of 2x2 green blocks.

The transformation rule is as follows:
1. Count the number of solid 2x2 blocks composed entirely of green pixels (value 3)
   within the input grid.
2. Create a 3x3 output grid initialized with white pixels (value 0).
3. Place blue pixels (value 1) along the main diagonal (top-left to bottom-right)
   of the output grid. The number of blue pixels placed is equal to the count
   of 2x2 green blocks found in the input grid, capped at a maximum of 3
   (since the output grid is 3x3).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by counting 2x2 green blocks and representing
    the count on the diagonal of a 3x3 output grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid containing
                                                 integer color values.

    Returns:
        np.ndarray: A 3x3 numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # --- Count 2x2 green blocks ---
    green_2x2_count = 0
    # Iterate through possible top-left corners (r, c) of a 2x2 block
    # The loops need to stop at height-2 and width-2 to avoid index out of bounds
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the 2x2 block starting at (r, c) is all green (3)
            if (input_array[r, c] == 3 and
                input_array[r + 1, c] == 3 and
                input_array[r, c + 1] == 3 and
                input_array[r + 1, c + 1] == 3):
                green_2x2_count += 1

    # --- Create the output grid ---
    # Initialize a 3x3 grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # --- Place blue pixels on the diagonal ---
    # Determine the number of blue pixels to place (capped at 3)
    num_blue_pixels = min(green_2x2_count, 3)

    # Place blue (1) pixels on the diagonal (i, i)
    for i in range(num_blue_pixels):
        output_grid[i, i] = 1

    return output_grid