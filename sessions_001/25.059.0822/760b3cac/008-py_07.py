"""
Transforms an input grid by moving all azure (8) pixels to the top row of the output grid, filling the rest with black (0).
"""

import numpy as np

def find_all_pixels(grid, color):
    """
    Finds the coordinates of all pixels of a specified color.

    Args:
        grid: The input grid.
        color: The color to search for.

    Returns:
        A list of tuples, where each tuple contains (row, col).
    """
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                pixels.append((r,c))
    return pixels

def transform(input_grid):
    # Initialize output_grid as all black
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # 1. Identify all azure pixels
    azure_pixels = find_all_pixels(input_grid, 8)

    # 2. Count azure pixels
    num_azure = len(azure_pixels)

    # 3. Reposition azure pixels to the top row
    for i in range(min(num_azure, cols)):  # Ensure we don't exceed grid width
        output_grid[0, i] = 8

    return output_grid