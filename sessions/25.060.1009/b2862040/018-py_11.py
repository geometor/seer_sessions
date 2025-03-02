"""
1.  Identify Target: Locate all blue (1) pixels within the input grid.
2.  Identify Trigger: Locate all maroon (9) pixels within the input grid.
3.  Bottom-Rightmost Rule: Of the blue pixels, determine the bottom-rightmost pixel.
4.  Conditional Transformation: The bottom-rightmost blue pixel changes to azure (8) only if at least one of its neighboring pixels is maroon (9).
5.  Preserve other colors: All colors other than the transformed blue pixel are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of the values of the 8 neighbors of a cell (up, down, left, right, and diagonals).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def find_bottom_rightmost_blue(grid):
    """
    Finds the bottom-rightmost blue (1) pixel in the grid.
    Returns its coordinates as a tuple (row, col).
    Returns None if no blue pixel is found.
    """
    rows, cols = grid.shape
    blue_pixels = []
    for row in range(rows):
        for col in range(cols):
            if grid[row, col] == 1:
                blue_pixels.append((row, col))

    if not blue_pixels:
        return None

    # Find the pixel with the largest row and then the largest column
    return max(blue_pixels, key=lambda item: (item[0], item[1]))

def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the bottom-rightmost blue pixel.
    bottom_rightmost_blue = find_bottom_rightmost_blue(input_grid)

    if bottom_rightmost_blue:
        row, col = bottom_rightmost_blue
        # Get the neighbors of the bottom-rightmost blue pixel.
        neighbors = get_neighbors(input_grid, row, col)
        # Check if at least one neighbor is maroon (9).
        if any(neighbor == 9 for neighbor in neighbors):
            # Change the bottom-rightmost blue pixel to azure (8).
            output_grid[row, col] = 8

    # Return the transformed grid.
    return output_grid