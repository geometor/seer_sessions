```python
"""
The program takes each input pixel and turns it into a 2x2 block of the same color, and then encases everything with a border/frame of '0' (white) color.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Rows
    duplicated_rows_grid = []
    for row in input_grid:
        duplicated_rows_grid.append(row)
        duplicated_rows_grid.append(row)
    
    # Duplicate Columns
    duplicated_cols_grid = []
    for row in duplicated_rows_grid:
        new_row = []
        for cell in row:
            new_row.append(cell)
            new_row.append(cell)
        duplicated_cols_grid.append(new_row)

    # Convert to numpy array for easier manipulation
    expanded_grid = np.array(duplicated_cols_grid)

    # Add 0 border
    rows, cols = expanded_grid.shape
    output_grid = np.zeros((rows + 2, cols + 2), dtype=int)
    output_grid[1:rows+1, 1:cols+1] = expanded_grid

    return output_grid.tolist()
```