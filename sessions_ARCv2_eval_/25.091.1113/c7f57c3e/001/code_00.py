"""
Perform a pixel-wise color swap transformation on the input grid.
Pixels with color yellow (4) are changed to magenta (6).
Pixels with color magenta (6) are changed to yellow (4).
All other pixel colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a color swap transformation to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid where each cell
                                                   is an integer from 0 to 9.

    Returns:
        numpy array: The transformed grid with yellow (4) swapped with magenta (6).
    """
    # Convert input_grid to a NumPy array for easier element-wise operations
    input_array = np.array(input_grid, dtype=int)

    # Create a copy of the input array to modify and return as the output
    output_grid = np.copy(input_array)

    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check the color of the current pixel in the input grid
            current_color = input_array[r, c]

            # Apply the swap rule
            if current_color == 4:
                # If the color is yellow (4), change it to magenta (6) in the output grid
                output_grid[r, c] = 6
            elif current_color == 6:
                # If the color is magenta (6), change it to yellow (4) in the output grid
                output_grid[r, c] = 4
            # No 'else' needed, as other colors remain unchanged (already copied)

    return output_grid
