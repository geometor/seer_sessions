"""
The input grid is expanded by doubling each row and then doubling each column.  Each pixel in the input becomes a 2x2 block of the same pixel in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by doubling each row and then doubling each column.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the expanded output grid.
    """
    # Double the Rows: Create two copies of each row.
    rows_doubled = []
    for row in input_grid:
        rows_doubled.append(row)
        rows_doubled.append(row)  # Add the same row twice

    rows_doubled_array = np.array(rows_doubled)

    # Double the Columns: Create two copies of each column.
    output_grid = []
    for row in rows_doubled_array:
        new_row = []
        for pixel in row:
            new_row.append(pixel)
            new_row.append(pixel)  # Duplicate each pixel horizontally
        output_grid.append(new_row)
        
    return np.array(output_grid)