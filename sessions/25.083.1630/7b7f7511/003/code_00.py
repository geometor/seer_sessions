"""
The transformation rule involves splitting the input grid and taking a portion of the original grid.

1.  **Determine the axis of truncation:**
    *   If the input grid's width is greater than its height, perform a *horizontal* truncation.
    *   Otherwise, if the input grid's width is less or equal to its height, perform a *vertical* truncation.
        *(Note: need a more complex rule based on width / height of the example inputs)*

2.  **Horizontal Truncation:** Divide the input grid's width by 2. The output grid consists of all rows and the first half of the columns of the input grid.

3.  **Vertical Truncation:** Divide the input grid's height by 2. The output grid consists of the first half of the rows and all the columns.

The core operation is determining the truncation axis and then slicing the input grid appropriately.
"""

import numpy as np

def transform(input_grid):
    input_rows, input_cols = input_grid.shape

    # Determine the axis of truncation.
    if input_cols > input_rows:
        # Horizontal Truncation
        output_cols = input_cols // 2
        output_grid = input_grid[:, :output_cols]  # All rows, first half of columns.
    else:
        # Vertical Truncation
        output_rows = input_rows // 2
        output_grid = input_grid[:output_rows, :]  # First half of rows, all columns.

    return output_grid