```python
"""
The input grid is expanded into an output grid with dimensions doubled (factor of 2).
The output grid is constructed in two main phases: column-wise replication and insertion, followed by row-wise replication and insertion.

1. **Column-wise Operation:**
   - Each column from the input grid is copied to the output grid.
   - If a column in the input grid contains any non-zero pixels, a new column filled with azure (8) is inserted immediately to the right of the copied column.

2. **Row-wise Operation:**
    - Each row from the input grid is copied to the output grid.
    - If an input row contains any non-zero pixels:
        - A new row is inserted in output, directly below current working row.
        - For the new row, check two conditions:
            - If the corresponding pixel value in the *row above* is 0, the new pixel is 8.
            - The new row values that correspond to original pixel and inserted azure columns are set to 8.

"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    input_height, input_width = input_grid.shape
    output_grid = np.zeros((input_height * 2, input_width * 2), dtype=int)

    # Column-wise replication and insertion
    output_col_idx = 0
    for input_col_idx in range(input_width):
        # Copy the input column
        for input_row_idx in range(input_height):
            output_grid[input_row_idx * 2, output_col_idx] = input_grid[input_row_idx, input_col_idx]

        # Insert azure column if necessary
        if np.any(input_grid[:, input_col_idx] != 0):
            output_col_idx += 1
            for input_row_idx in range(input_height):
                output_grid[input_row_idx * 2, output_col_idx] = 8
        output_col_idx += 1

    # Row-wise replication and insertion
    for input_row_idx in range(input_height):
        if np.any(input_grid[input_row_idx, :] != 0):
            output_row_idx = (input_row_idx * 2) + 1
            for output_col_idx in range(output_grid.shape[1]):
              if output_grid[output_row_idx-1, output_col_idx] == 0:
                output_grid[output_row_idx, output_col_idx] = 8

            for input_col_idx in range(input_width):
                output_grid[output_row_idx, input_col_idx * 2] = 8
                if (input_col_idx * 2 + 1) < output_grid.shape[1]:
                    output_grid[output_row_idx, input_col_idx * 2 + 1] = 8

    return output_grid
```