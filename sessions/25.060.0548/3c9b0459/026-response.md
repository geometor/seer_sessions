# 3c9b0459 • 026 • refine_coder

---
```python
"""
1.  **Identify** all rows containing non-zero pixels in the input grid.
2.  **Sort** these rows by the color values in ascending order.
3.  **Move** the lowest color value row to the top of the output grid (row 0).
4. **Move** other identified rows so that the color value order is maintained.
5.  **All other rows** (those containing only zeros) are shifted down in the output grid, filling the remaining spaces.
"""

import numpy as np

def find_nonzero_rows(grid):
    """Finds the indices of rows containing at least one non-zero pixel."""
    nonzero_rows = []
    for i, row in enumerate(grid):
        if np.any(row != 0):
            nonzero_rows.append(i)
    return nonzero_rows

def get_row_color_value(row):
    """Returns the color value of a row.  Assumes a single color per row."""
    for val in row:
      if val !=0:
        return val
    return 0

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find rows with non-zero pixels
    nonzero_row_indices = find_nonzero_rows(input_grid)
    
    # Create a list of (color_value, row_index, row_content) tuples
    row_data = []
    for i in nonzero_row_indices:
        row = input_grid[i]
        color_value = get_row_color_value(row)
        row_data.append((color_value, i, row))

    # Sort by color value (ascending)
    row_data.sort()

    # Place sorted rows at the top of the output grid
    output_row_index = 0
    for color_value, original_index, row in row_data:
        output_grid[output_row_index] = row
        output_row_index += 1

    return output_grid
```
