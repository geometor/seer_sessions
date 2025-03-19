# beb8660c • 011 • refine_coder

---
```python
"""
Preserve rows containing non-zero (non-background) pixels. If an object is
present in a row, preserve that entire row in the output grid. All background
rows become background in the output. Non background rows appear to shift down
if a preceeding row is removed.
"""

import numpy as np

def find_rows_with_objects(grid):
   grid = np.array(grid)
   rows_with_objects = []
   for i, row in enumerate(grid):
       if np.any(row != 0):  # Check if the row has any non-background pixels
          rows_with_objects.append(i)
   return rows_with_objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find rows with objects
    rows_with_objects = find_rows_with_objects(input_grid)

    # change output pixels 
    output_row_index = 0
    for i, row in enumerate(input_grid):
        if i in rows_with_objects:
          output_grid[output_row_index] = row
          output_row_index += 1

    return output_grid
```
