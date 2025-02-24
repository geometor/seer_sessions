"""
Replaces all values in the input grid with the value 3.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing all its elements with the value 3.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the output grid, with all elements set to 3.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0  # Handle empty input case
    output_grid = np.full((rows, cols), 3)


    return output_grid.tolist()