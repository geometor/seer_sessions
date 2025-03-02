"""
The transformation rule identifies unique rows in the input grid and adds them to the output grid, preserving the order of their first appearance.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extracting unique rows, preserving original order.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the output grid.
    """
    output_grid = []
    seen_rows = []

    # Iterate through rows
    for row in input_grid:
        # Convert row to a list for easier comparison (np.array_equal is slow)
        row_list = row.tolist()
        # Check if the row has been seen before
        if row_list not in seen_rows:
            # Add the row to the output and mark it as seen
            output_grid.append(row_list)
            seen_rows.append(row_list)

    return np.array(output_grid)