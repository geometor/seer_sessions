# 5ad4f10b • 016 • example_3 • investigate_coder

---
```python
"""
The transformation extracts the '3' (green) pixels from the input grid and represents their relative positions in a 3x3 output grid. Other colored pixels are ignored.
"""

import numpy as np

def get_green_pixel_rows_cols(input_grid):
    """
    Finds the rows and columns containing green (3) pixels.
    Returns a tuple of sets: (rows, cols)
    """
    rows = set()
    cols = set()
    for r_idx, row in enumerate(input_grid):
        for c_idx, val in enumerate(row):
            if val == 3:
                rows.add(r_idx)
                cols.add(c_idx)
    return rows, cols

def transform(input_grid):
    """
    Transforms the input grid by extracting green pixels and representing them in a compressed 3x3 grid.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the row and column indices containing green pixels.
    green_rows, green_cols = get_green_pixel_rows_cols(input_grid)

    # initialize output grid as all zeros
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Determine which rows and columns in the output should have greens
    
    num_rows = input_grid.shape[0]
    num_cols = input_grid.shape[1]

    row_splits = np.array_split(np.arange(num_rows), 3)
    col_splits = np.array_split(np.arange(num_cols), 3)

    row_map = {}
    for i, split in enumerate(row_splits):
        for item in split:
          row_map[item] = i

    col_map = {}
    for i, split in enumerate(col_splits):
        for item in split:
            col_map[item] = i

    # Populate output grid
    for r in green_rows:
        for c in green_cols:
            output_row_index = row_map[r]
            output_col_index = col_map[c]
            output_grid[output_row_index, output_col_index] = 3


    return output_grid.tolist()
```
