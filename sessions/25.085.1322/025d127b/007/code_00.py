"""
Transforms the input grid by shifting all non-background pixels (color > 0) 
one column to the right, with horizontal wrap-around. Pixels that shift 
beyond the rightmost column reappear in the leftmost column of the same row. 
The output grid has the same dimensions as the input grid and is initially 
filled with the background color (0). Background pixels remain in place.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a horizontal shift with wrap-around to non-background pixels.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: A 2D NumPy array representing the transformed grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize the output grid with the background color (0)
    # Using np.zeros_like ensures the same shape and dtype as the input
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current pixel
            color = input_grid[r, c]

            # Check if the pixel is not the background color
            if color > 0:
                # Calculate the new column index for the shift with wrap-around
                # The modulo operator (%) handles the wrap-around automatically:
                # - If c + 1 < width, new_c = c + 1
                # - If c + 1 == width (i.e., c is the last column index width - 1), new_c = width % width = 0
                new_c = (c + 1) % width

                # Place the pixel in the shifted position (same row, new column) in the output grid
                output_grid[r, new_c] = color
            # else:
                # If the color is background (0), the corresponding output cell
                # remains 0 as initialized, effectively keeping background pixels in place.

    # Return the modified output grid
    return output_grid