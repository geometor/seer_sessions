"""
Transforms an input grid by identifying all azure (8) pixels, shifting them one position down, changing their color to red (2), and placing them onto an initially white (0) output grid of the same dimensions. Azure pixels shifted beyond the bottom boundary are discarded.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color white (0).
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each pixel of the input grid.
    for r in range(height):
        for c in range(width):
            # If a pixel at coordinates (row, column) has the color azure (8):
            if input_np[r, c] == 8:
                # Calculate the target coordinates for the output grid as (row + 1, column).
                target_r = r + 1
                target_c = c

                # Check if the target row (row + 1) is within the bounds of the grid height.
                if target_r < height:
                    # If the target coordinates are valid (within the grid boundaries), set the pixel at these target coordinates in the output grid to the color red (2).
                    output_grid[target_r, target_c] = 2

    # Return the completed output grid.
    return output_grid.tolist() # Return as list of lists to match ARC standard if needed, though numpy is often used internally.