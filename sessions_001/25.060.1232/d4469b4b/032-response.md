# d4469b4b • 032 • refine_coder

---
```python
"""
Divide the input grid into nine overlapping 3x3 regions.
The centers of these regions in the input grid correspond to the output grid's pixel coordinates.  The row indices of the centers are calculated as: [M//2 - 1, M//2, M//2 + 1]
The column indices of the centers are calculated as: [N//2 - 1, N//2, N//2 + 1]
If any pixel within a 3x3 region is 2 (red) in the input, the output pixel for corresponding region is 5 (gray).
Otherwise the output pixel is 0 (white).
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid

    # Calculate center row indices for the 3x3 regions
    center_row_indices = [rows // 2 - 1, rows // 2, rows // 2 + 1]
    # Calculate center column indices for the 3x3 regions
    center_col_indices = [cols // 2 - 1, cols // 2, cols // 2 + 1]
    
    for i, center_row in enumerate(center_row_indices):
        for j, center_col in enumerate(center_col_indices):
            # Define the 3x3 region in the input grid
            row_start = max(0, center_row - 1)
            row_end = min(rows, center_row + 2)
            col_start = max(0, center_col - 1)
            col_end = min(cols, center_col + 2)
            
            region = input_grid[row_start:row_end, col_start:col_end]
            
            # if any pixel in the region equals to 2, convert output to 5, otherwise 0
            output_grid[i,j] = 5 if 2 in region else 0


    return output_grid.tolist()
```
