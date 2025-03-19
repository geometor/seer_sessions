"""
Transforms a grid by replacing each gray pixel (5) with a blue cross (1) centered on that pixel's location. The gray pixel itself also becomes blue.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating blue crosses centered on gray pixels.
    The gray pixels are replaced by blue pixels.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the locations of gray pixels (5).
    gray_pixel_locations = np.argwhere(input_grid == 5)

    # Create crosses of blue pixels (1) around each gray pixel.
    for row, col in gray_pixel_locations:
        # Replace the gray pixel with a blue one.
        output_grid[row, col] = 1

        # Add blue pixels for the cross arms, checking bounds.
        if row > 0:
            output_grid[row - 1, col] = 1  # Up
        if row < rows - 1:
            output_grid[row + 1, col] = 1  # Down
        if col > 0:
            output_grid[row, col - 1] = 1  # Left
        if col < cols - 1:
            output_grid[row, col + 1] = 1  # Right

    return output_grid.tolist()