"""
The transformation identifies the color of the top-right cell in the input grid and replicates it across all cells of a new 3x3 grid, resulting in a uniform-colored output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid into a new grid where all cells have the same color
    as the top-right cell of the input grid.

    Args:
      input_grid: A 3x3 NumPy array representing the input grid.

    Returns:
      A 3x3 NumPy array where all cells have the same color as the top-right
      cell of the input_grid.
    """
    # Get the color of the top-right cell.
    top_right_color = input_grid[0, -1]

    # Create a new 3x3 grid filled with the top-right color.
    output_grid = np.full((3, 3), top_right_color)

    return output_grid