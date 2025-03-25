```python
"""
1.  **Identify** the *start row* and *end row* of a contiguous block of rows containing green (3) pixels. A contiguous block is defined as one or more consecutive rows, each containing at least one green pixel.
2.  **For the start row**:
    *   Insert an orange (7) pixel to the immediate left of the leftmost green (3) pixel.
    *   Insert an orange (7) pixel to the immediate right of the rightmost green (3) pixel.
3.  **For the end row**:
    *   Insert an orange (7) pixel to the immediate left of the leftmost green (3) pixel.
    *   Insert an orange (7) pixel to the immediate right of the rightmost green (3) pixel.
4.  **All other rows** in the output grid remain identical to the input grid.
"""

import numpy as np

def get_green_rows(grid):
    # returns rows containing green pixels
    green_rows = []
    for i, row in enumerate(grid):
        if 3 in row:
            green_rows.append(i)
    return green_rows

def get_start_end_rows(green_rows):
     # gets the start and end rows
    if not green_rows:
        return None, None
    return green_rows[0], green_rows[-1]
            
def transform(input_grid):
    """Transforms the input grid by wrapping green blocks with orange pixels."""

    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows_with_green = get_green_rows(input_grid)
    start_row, end_row = get_start_end_rows(rows_with_green)
    
    if start_row is None:
        return output_grid.tolist()

    # Iterate through rows that have green pixels
    for row_index in [start_row, end_row]:
      if 0 <= row_index < input_grid.shape[0]:
        row = input_grid[row_index]
        
        # Find the indices of the green pixels
        green_indices = np.where(row == 3)[0]

        # find the leftmost and rightmost
        leftmost_green_index = green_indices[0]
        rightmost_green_index = green_indices[-1]
        
        # bounds check and set left pixel to orange (7)
        if leftmost_green_index > 0:
            output_grid[row_index, leftmost_green_index - 1] = 7
        # bounds check and set right pixel to orange (7)
        if rightmost_green_index < len(row) - 1:
            output_grid[row_index, rightmost_green_index + 1] = 7

    return output_grid.tolist()
```