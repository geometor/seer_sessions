# 2dee498d • 006 • refine_coder

---
```python
"""
The transformation rule works as follows: The input grid's width is reduced to one-third of its original size, while the height remains the same. The input grid's columns are processed in groups of three. For each group of three consecutive columns, the very first columns values are used to create the output column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = input_width // 3
    output_height = input_height
    output_grid = []

    # Iterate through rows to maintain height
    for row_index in range(output_height):
      new_row = []
      #take every third column starting at 0
      for col_index in range(0,input_width,3):
        new_row.append(input_grid[row_index][col_index])
      output_grid.append(new_row)


    return output_grid
```

