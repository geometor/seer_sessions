"""
Create an output grid of the same dimensions as the input grid, initialized with the background color white (0). Iterate through each pixel of the input grid. If a pixel's color is azure (8), copy its color to the corresponding position in the output grid. Otherwise, leave the output grid pixel as white (0). Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Filters the input grid to keep only azure (8) pixels, replacing all others with white (0).

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid with only azure pixels preserved.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize an output grid of the same dimensions with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Identify the locations of azure (8) pixels in the input grid
    azure_pixels = (input_grid == 8)

    # Set the corresponding locations in the output grid to azure (8)
    output_grid[azure_pixels] = 8

    return output_grid