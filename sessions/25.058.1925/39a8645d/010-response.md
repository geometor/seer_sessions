# 39a8645d • 010 • refine_coder

---
```python
"""
The output grid represents a vertically compressed version of the input grid, focusing solely on the presence of azure pixels within each row. The output has the same number of rows as the input and one column. Each output cell is azure if the corresponding input row contains at least one azure pixel; otherwise, it's black (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of azure pixels in each row.
    """
    input_grid = np.array(input_grid)
    rows, _ = input_grid.shape
    output_grid = np.zeros((rows, 1), dtype=int)

    # Iterate through each row of the input grid.
    for i in range(rows):
        # Check for the presence of azure (8) in the current row.
        if 8 in input_grid[i]:
            output_grid[i, 0] = 8

    return output_grid.tolist()
```
