```python
"""
The transformation involves selecting specific rows from the 8x8 input grid and then expanding and resampling them to create the 3x6 output grid. Specifically, we select rows 1, 3, and 5 from the input. From each selected row, we use the values at every other index, starting with index 0. These values compose the rows of the output grid.
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Initialize output grid
    output_grid = np.zeros((3, 6), dtype=int)

    # Select rows 1, 3, and 5 from input
    selected_rows = [1, 3, 5]

    # Iterate through selected rows and populate output grid
    for row_index, input_row in enumerate(selected_rows):
        output_col = 0
        for col_index in range(0, input_grid.shape[1], 2):
            if output_col < 6:
                output_grid[row_index, output_col] = input_grid[input_row, col_index]
                output_col += 1
            else:
              break
    return output_grid.tolist()
```