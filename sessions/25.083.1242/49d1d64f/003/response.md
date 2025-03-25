```python
"""
The input grid's rows and columns are duplicated, and then a border of '0' (white) pixels is added by overlapping the edges.
"""

import numpy as np

def transform(input_grid):
    # Duplicate Rows
    duplicated_rows_grid = []
    for row in input_grid:
        duplicated_rows_grid.append(row)
        duplicated_rows_grid.append(row)  # Add the row again to duplicate

    duplicated_rows_grid = np.array(duplicated_rows_grid)

    # Duplicate Columns
    duplicated_cols_grid = []
    for row in duplicated_rows_grid:
        new_row = []
        for cell in row:
            new_row.append(cell)
            new_row.append(cell) #add the cell again
        duplicated_cols_grid.append(new_row)

    duplicated_cols_grid = np.array(duplicated_cols_grid)

    # Create Output Grid with correct dimensions
    height, width = duplicated_cols_grid.shape
    output_grid = np.zeros((height + 1, width + 1), dtype=int)  # Initialize with zeros

    # Place the duplicated grid into output grid, overlapping the edges.
    output_grid[0:height, 0:width] = duplicated_cols_grid

    return output_grid
```