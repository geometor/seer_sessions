# 25ff71a9 • 016 • refine_coder

---
```python
"""
The transformation rule identifies a row containing all blue pixels (value 1). If such a row is found and is not already the last row, it moves this row to the bottom of the grid. The rows originally below the "blue row" are shifted upwards to fill the gap. If no all-blue row is found, or if it's already at the bottom, the grid remains unchanged.
"""

import numpy as np

def find_all_blue_row(grid):
    """Helper function to find the index of the row with all blue pixels."""
    for i, row in enumerate(grid):
        if np.all(row == 1):
            return i
    return -1

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    num_rows = output_grid.shape[0]

    # Find the row with all blue pixels (value 1)
    blue_row_index = find_all_blue_row(input_grid)

    # If a blue row is found and it is not the last row, perform the row shift
    if blue_row_index != -1 and blue_row_index != num_rows -1:
        # Store the all blue row
        blue_row = output_grid[blue_row_index]
        
        # Shift rows down from blue_row_index to num_rows-1
        output_grid[blue_row_index:num_rows-1] = output_grid[blue_row_index+1:num_rows]
        
        # Move the blue row to the bottom
        output_grid[num_rows-1] = blue_row

    return output_grid
```
