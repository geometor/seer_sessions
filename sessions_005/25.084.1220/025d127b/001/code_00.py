"""
Shift all non-background (non-white) pixels horizontally to the right by one column.
Pixels shifted beyond the right edge are discarded. The original positions of the
shifted pixels become background (white).
"""

import numpy as np

def transform(input_grid):
    """
    Shifts all non-background pixels one column to the right within the grid boundaries.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the same dimensions as input, filled with background color (0)
    output_grid = np.zeros_like(input_np)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            pixel_color = input_np[r, c]

            # Check if the pixel is not background (white, 0)
            if pixel_color != 0:
                # Calculate the target column index for the shift
                new_c = c + 1

                # Check if the new column is within the grid's width boundaries
                if new_c < width:
                    # If within bounds, place the pixel's color in the new position in the output grid
                    output_grid[r, new_c] = pixel_color

    return output_grid