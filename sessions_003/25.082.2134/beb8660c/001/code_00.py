"""
Transforms the input grid by reordering rows. Data rows (rows with at least one non-black pixel) are identified, their relative order is preserved, and they are stacked at the bottom of the output grid. The remaining rows at the top are filled with padding (all black pixels).
"""

import numpy as np

def _is_data_row(row):
    """Checks if a row contains at least one non-black pixel."""
    return np.any(row != 0)

def _get_data_rows(grid):
    """Extracts and returns data rows from the grid."""
    data_rows = []
    for row in grid:
        if _is_data_row(row):
            data_rows.append(row)
    return data_rows

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Get data rows from the input grid
    data_rows = _get_data_rows(input_grid)

    # Calculate the starting row index for placing data rows at the bottom
    num_data_rows = len(data_rows)
    start_row = rows - num_data_rows

    # Place data rows at the bottom of the output grid
    for i, row in enumerate(data_rows):
        output_grid[start_row + i, :] = row

    return output_grid.tolist()