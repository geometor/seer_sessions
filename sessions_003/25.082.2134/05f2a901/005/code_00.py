"""
1. Identify Non-White Rows: Determine the rows in the input grid that contain any non-white pixels (i.e., colored rows).
2. Center and Stack: Rearrange *only* the non-white rows from top-to-bottom order so that they are stacked together and positioned vertically in the center of the output grid. Maintain the original vertical order of the identified rows. The output grid has the same dimensions as the input grid.
3. Preserve shape: The output rows have exactly the same contents as the input rows.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by identifying non-white rows,
    and centering them in the output grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Non-White Rows.
    non_white_row_indices = []
    for r in range(rows):
        if not all(input_grid[r] == 0):
            non_white_row_indices.append(r)

    # 2. Calculate the starting row for centering.
    num_non_white_rows = len(non_white_row_indices)
    start_row = (rows - num_non_white_rows) // 2

    # 3. Copy non-white rows to the center of the output grid.
    current_output_row = start_row
    for r in non_white_row_indices:
        output_grid[current_output_row] = input_grid[r]
        current_output_row += 1

    return output_grid.tolist()