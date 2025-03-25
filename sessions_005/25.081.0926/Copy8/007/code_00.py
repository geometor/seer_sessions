"""
The transformation rule involves identifying the last two columns of the entire input grid that contain any non-zero pixels. These columns are then duplicated, and the duplicates are inserted immediately to the right of the original columns. This insertion shifts existing pixels to the right, and the grid is extended if necessary.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: duplicate the last two columns containing non-zero pixels and insert them to the right of the original columns.
    """
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Find the last two columns with non-zero elements
    non_zero_cols = [c for c in range(cols) if np.any(input_grid[:, c] != 0)]
    if not non_zero_cols:
        return output_grid  # Nothing to duplicate

    if len(non_zero_cols) >= 2:
      cols_to_duplicate = non_zero_cols[-2:]
    else:
      cols_to_duplicate = non_zero_cols

    # Duplicate the selected columns
    duplicated_cols = input_grid[:, cols_to_duplicate]

    # Insert the duplicated columns into the output grid
    insert_position = cols_to_duplicate[-1] + 1

    # create extended grid
    output_grid = np.insert(output_grid, [insert_position]*duplicated_cols.shape[1], duplicated_cols, axis=1)

    return output_grid