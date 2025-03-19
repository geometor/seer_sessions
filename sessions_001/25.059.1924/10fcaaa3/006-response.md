# 10fcaaa3 • 006 • example_2 • investigate_coder

---
```python
"""
1.  **Expansion:** The input grid is doubled in both dimensions (height and width). The 3x4 input becomes a 6x8 output.
2.  **Magenta Replication:** Each magenta (6) pixel in the input grid is maintained in the output grid. And for every magenta, insert a magenta in a column 3 spaces to the right.
3.  **Azure Fill:** All spaces immediately below a magenta, above a magenta, and all rows in between get filled with azure (8). All other pixels are left white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 2
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # iterate input grid
    for row in range(input_height):
        for col in range(input_width):
            # magenta replication
            if input_grid[row, col] == 6:
                output_grid[row, col] = 6
                output_grid[row, col + (output_width // 2) ] = 6
    
    # azure fill rows
    for row in range(output_height):
      if 6 in output_grid[row]:
        output_grid[row,:] = [8 if x == 0 else x for x in output_grid[row,:] ]

    # azure fill between columns
    magenta_cols = [ c for c in range(output_width) if 6 in output_grid[:,c] ]
    if len(magenta_cols) > 1:
      for r in range(output_height):
        for c in range(min(magenta_cols), max(magenta_cols) + 1):
          if output_grid[r,c] == 0:
            output_grid[r,c] = 8

    return output_grid
```
