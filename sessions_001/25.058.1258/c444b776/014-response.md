# c444b776 • 014 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to replicate the top section (rows 0-8) of the input grid and place it below row 9. The original content of rows 11 and below is discarded.
"""

import numpy as np

def find_landmark_row(grid, color):
    # Find a row that is entirely of the specified color.
    for i, row in enumerate(grid):
        if all(cell == color for cell in row):
            return i
    return None

def transform(input_grid):
    # Convert input_grid to a NumPy array for easier manipulation.
    input_grid = np.array(input_grid)

    # Identify source region (rows 0-8).
    source_region = input_grid[0:9]

    # Find the landmark row (all yellow/4s)
    landmark_row_index = find_landmark_row(input_grid, 4)

    # Initialize the output grid as a copy of input
    output_grid = input_grid.copy()

    # Calculate the destination start row (two rows below landmark row)
    destination_start_row = landmark_row_index + 2 if landmark_row_index is not None else None


    if(destination_start_row is not None and destination_start_row + source_region.shape[0] <= output_grid.shape[0] ):
        # Paste the source region into the destination area in the output grid.
        output_grid[destination_start_row:destination_start_row + source_region.shape[0]] = source_region
    else:
        return input_grid # cant do it, return the original

    #clear all rows after pasting operation
    output_grid[destination_start_row+ source_region.shape[0]:] = 0

    return output_grid.tolist()
```
