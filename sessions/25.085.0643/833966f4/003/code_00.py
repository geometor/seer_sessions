"""
Rearranges pixels within a single-column grid, assuming a height of 5.
The transformation swaps the pixels at indices 0 and 1, leaves the pixel 
at index 2 unchanged, and swaps the pixels at indices 3 and 4.
"""

import numpy as np

def transform(input_grid):
    """
    Applies specific index swaps to a 5x1 input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the 5x1 input grid.

    Returns:
        np.array: A 2D numpy array representing the rearranged 5x1 output grid.
                  Returns a copy of the input if the shape is not 5x1.
    """
    # Get the height and width of the input grid
    height, width = input_grid.shape

    # Check if the grid dimensions match the expected 5x1 based on examples
    if height != 5 or width != 1:
        # This logic is derived solely from 5x1 examples.
        # If the input doesn't match, return a copy as we don't know the rule.
        print(f"Warning: Input grid shape {input_grid.shape} is not 5x1. Logic might not apply. Returning copy.")
        return np.copy(input_grid)

    # Initialize output_grid as a copy of the input to modify
    output_grid = np.copy(input_grid)

    # Swap the pixel values at index 0 and index 1
    # Store the value at index 0 temporarily
    temp_0 = output_grid[0, 0]
    # Assign the value at index 1 to index 0
    output_grid[0, 0] = output_grid[1, 0]
    # Assign the temporary value (original value at index 0) to index 1
    output_grid[1, 0] = temp_0

    # The pixel value at index 2 remains unchanged in its position.
    # No action needed for output_grid[2, 0] as it's already copied correctly.

    # Swap the pixel values at index 3 and index 4
    # Store the value at index 3 temporarily
    temp_3 = output_grid[3, 0]
    # Assign the value at index 4 to index 3
    output_grid[3, 0] = output_grid[4, 0]
    # Assign the temporary value (original value at index 3) to index 4
    output_grid[4, 0] = temp_3

    # Return the modified output grid
    return output_grid