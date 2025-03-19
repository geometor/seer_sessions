# 9af7a82c • 022 • example_4 • investigate_coder

---
```python
"""
The program takes each column of the input, finds the max number M, creates M rows related to this input column, and transposes the column values, starting at position 0. The missing slots get filled with 0.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    num_cols = input_grid.shape[1]
    max_values = [np.max(input_grid[:, col]) for col in range(num_cols)]
    total_rows = sum(max_values)
    output_grid = np.zeros((total_rows, num_cols), dtype=int)

    # change output pixels
    row_offset = 0
    for col in range(num_cols):
        max_val = max_values[col]
        for row_index in range(input_grid.shape[0]):
            if row_index < input_grid.shape[0] : #check to prevent out-of-bound error
                value = input_grid[row_index, col]
                if (row_offset + row_index) < output_grid.shape[0]: #check to prevent out of bound error
                  output_grid[row_offset + row_index, col] = value
        row_offset += max_val


    return output_grid.tolist()
```
