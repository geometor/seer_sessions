# beb8660c • 005 • refine_coder

---
```python
"""
1.  **Identify** all pixels in the input grid that have a non-zero value (i.e., not black/0).
2.  **Create** an output grid with same dimension of the input grid.
3.  **Iterate** through the rows of input grid.
4. **For each row**, move the non-zero pixel to the last column of the same row in the output grid, keeping all others columns of the row as zero.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid with the same dimensions as the input grid, filled with zeros.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row of the input grid.
    for i in range(rows):
        # Find the non-zero pixels in the current row.
        for j in range(cols):
            if input_grid[i,j] != 0:
                # Move the non-zero element to the last column of output grid
                output_grid[i,-1] = input_grid[i,j]
                break # only one non zero per row based on examples

    return output_grid
```
