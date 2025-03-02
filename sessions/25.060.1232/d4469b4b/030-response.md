# d4469b4b • 030 • refine_coder

---
```python
"""
Divide the 5x5 input grid into nine overlapping 3x3 regions.
The centers of these regions in the input grid correspond to the output grid's pixel coordinates.
If any pixel within a 3x3 region is 2 (red) in the input, the output pixel for corresponding region is 5 (gray).
Otherwise the output pixel is 0 (white).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid

    for i in range(3):
        for j in range(3):
            # Define the 3x3 region in the input grid
            row_start = i
            row_end = i + 3
            col_start = j
            col_end = j + 3

            region = input_grid[row_start:row_end, col_start:col_end]
            
            # if any pixel in the region equals to 2, convert output to 5, otherwise 0
            output_grid[i,j] = 5 if 2 in region else 0


    return output_grid.tolist()
```
