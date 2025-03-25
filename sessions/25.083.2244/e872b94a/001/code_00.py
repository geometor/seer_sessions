"""
Counts the number of rows containing at least one gray (5) pixel in the input grid and creates a single-column output grid filled with black (0) pixels, where the height of the output grid corresponds to the counted rows.
"""

import numpy as np

def count_rows_with_gray(input_grid):
    """Counts rows with at least one gray (5) pixel."""
    count = 0
    for row in input_grid:
        if 5 in row:
            count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid into an output grid based on the presence of gray pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    # Count the number of rows that contain at least one gray (5) pixel.
    num_rows = count_rows_with_gray(input_grid)

    # Create an output grid that is a single column with a height equal to the counted rows.
    output_grid = np.zeros((num_rows, 1), dtype=int)

    # Fill all cells of the output grid with black (0).  (Already done by np.zeros)

    return output_grid