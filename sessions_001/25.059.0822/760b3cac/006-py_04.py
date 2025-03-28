"""
Transforms an input grid by moving all azure (8) pixels to the top row of the output grid, preserving yellow (4) pixels, and copying other non-azure pixels where possible.
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
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape

    # 1. Identify all azure pixels
    azure_pixels = find_all_pixels(input_grid, 8)

    # 2. Count azure pixels
    num_azure = len(azure_pixels)

    # 3. Clear the first row of the output grid
    output_grid[0, :] = 0

    # 4. Reposition azure pixels to the top row
    for i in range(min(num_azure, cols)):  # Ensure we don't exceed grid width
        output_grid[0, i] = 8

    # 5. & 6. Preserve yellow and copy other pixels.  This is handled implicitly
    # by initializing output_grid as a copy and only modifying the top row
    # and azure pixel locations. We iterate and check for conflicts
    for r in range(rows):
        for c in range(cols):
            if (r,c) in azure_pixels:
                if r != 0:
                  output_grid[r,c] = 0



    return output_grid