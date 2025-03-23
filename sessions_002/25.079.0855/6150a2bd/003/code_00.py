"""
The input grid is rotated 90 degrees clockwise. After the rotation, the columns of the rotated grid are reversed (the first column becomes the last, the second column becomes the second-to-last, and so on.).
"""

import numpy as np

def rotate_grid_clockwise(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1).tolist()

def reverse_columns(grid):
    """Reverses the order of columns in a grid."""
    return [row[::-1] for row in grid]

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise and
    then reversing the order of the columns.
    """
    # Rotate the grid 90 degrees clockwise.
    rotated_grid = rotate_grid_clockwise(input_grid)

    # Reverse the order of columns.
    output_grid = reverse_columns(rotated_grid)

    return output_grid