# 1e0a9b12 • 006 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Non-Zero Cells:** Find all cells in the input grid that have a non-zero value (i.e., not white).

2.  **Extract Non-Zero Values:** Create a list, preserving order of appearance by reading them from left-to-right and top-to-bottom, containing colors from identified cells.

3.  **Bottom Row Placement:** Place list into the bottom row of output grid.

4. **Fill Zeros** Fill remaining cells in the output grid with zeros.
"""

import numpy as np

def get_nonzero_cells(grid):
    # Find coordinates and values of non-zero cells
    rows, cols = np.nonzero(grid)
    return [(r, c, grid[r, c]) for r, c in zip(rows, cols)]

def transform(input_grid):
    # Initialize output grid with zeros and same shape/type as the input
    output_grid = np.zeros_like(input_grid)
    rows = input_grid.shape[0]
    cols = input_grid.shape[1]

    # Get non-zero cells with their values
    nonzero_cells = get_nonzero_cells(input_grid)
    
    # sort by row, then by col
    nonzero_cells.sort(key=lambda x: (x[0],x[1]))

    # Extract the color (values) from the non-zero cells
    nonzero_values = [cell[2] for cell in nonzero_cells]


    # Place the non-zero values in the bottom row of the output grid
    # Check if there are more values than columns
    if len(nonzero_values) > output_grid.shape[1]:
        raise ValueError("Too many non-zero values to fit in the bottom row.")

     # place into bottom row
    for i, value in enumerate(nonzero_values):
      output_grid[rows-1, i] = value

    return output_grid
```
