# d631b094 • 014 • example_3 • investigate_coder

---
```python
"""
Examine the input grid. Locate the single cell that has a non-zero value. Create a 1x1 output grid. Place the value of the non-zero cell into the output grid.
"""

import numpy as np

def find_non_zero_cell(grid):
    # Iterate through the grid to find the non-zero cell
    for row_idx, row in enumerate(grid):
        for col_idx, cell_value in enumerate(row):
            if cell_value != 0:
                return row_idx, col_idx, cell_value
    return None  # Return None if no non-zero cell is found

def transform(input_grid):
    # Find the non-zero cell and its value
    result = find_non_zero_cell(input_grid)
    
    if result is None:  # Handle cases where no non-zero cell exists. Could return an empty grid or raise an exception.
        return np.array([])

    row_idx, col_idx, cell_value = result

    # Create a 1x1 output grid with the non-zero value
    output_grid = np.array([[cell_value]])

    return output_grid
```
