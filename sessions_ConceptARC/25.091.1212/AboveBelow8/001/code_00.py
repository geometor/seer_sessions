"""
Isolate 'azure' pixels (color 8) from the input grid.

The transformation function creates an output grid of the same dimensions as the input grid. It iterates through each pixel of the input grid. If a pixel's color is 'azure' (8), its color is copied to the corresponding position in the output grid. All other pixels in the output grid are set to 'white' (0).
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only 'azure' (8) pixels, replacing others with 'white' (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only 'azure' pixels
                  preserved against a 'white' background.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the same dimensions, filled with 'white' (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel's color is 'azure' (8)
            if input_grid[r, c] == 8:
                # If it is 'azure', set the corresponding pixel in the output grid to 'azure' (8)
                output_grid[r, c] = 8
            # Otherwise, the output grid pixel remains 'white' (0) as initialized

    # Return the resulting output grid
    return output_grid