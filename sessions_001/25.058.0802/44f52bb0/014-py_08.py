"""
Counts the number of red (2) pixels in the input grid.
If the count is even, the output is a 1x1 grid containing '1' (blue).
"""

import numpy as np

def count_pixels(grid, color_value):
    # Count the number of pixels of a specific color in the grid.
    return np.sum(grid == color_value)

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Count the number of red (2) pixels.
    red_count = count_pixels(input_grid, 2)

    # Determine the output based on whether the count is even.
    if red_count % 2 == 0:
        output_grid = np.array([[1]])  # Create a 1x1 grid with the value 1.
    else:
        output_grid = np.array([[0]]) # Placeholder for odd counts
    return output_grid