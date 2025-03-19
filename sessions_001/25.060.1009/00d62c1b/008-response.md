# 00d62c1b • 008 • refine_coder

---
```python
"""
The transformation rule is to insert a yellow (4) pixel between any two adjacent green (3) pixels in the horizontal or vertical direction. If there are no green pixels, the output is identical to the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid by copying the input.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Create lists to store the positions where rows/cols need to be added
    row_insertions = []
    col_insertions = []

    # Iterate through the original grid to find adjacent greens and mark insertion points.
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 3:
                # Check for vertical adjacency
                if row + 1 < rows and input_grid[row + 1, col] == 3:
                    row_insertions.append(row + 1)
                # Check for horizontal adjacency
                if col + 1 < cols and input_grid[row, col + 1] == 3:
                    col_insertions.append(col + 1)

    # Perform row insertions.  Iterate in reverse order to avoid index shifting problems.
    row_offset = 0
    for row_index in sorted(row_insertions):
        output_grid = np.insert(output_grid, row_index + row_offset, 4, axis=0)
        row_offset += 1

    # Perform column insertions. Iterate in reverse order to avoid index shifting problems.
    col_offset = 0
    for col_index in sorted(col_insertions):
        output_grid = np.insert(output_grid, col_index + col_offset, 4, axis=1)
        col_offset += 1
    
    return output_grid
```
