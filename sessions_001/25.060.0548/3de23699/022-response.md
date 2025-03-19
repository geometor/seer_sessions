# 3de23699 • 022 • example_4 • investigate_coder

---
```python
"""
The transformation identifies azure pixels in the input grid and, based on their
location, potentially within a specific neighborhood configuration (e.g., pairs),
creates an azure pixel in the output at a corresponding, potentially offset,
location. Other color pixels, specifically yellow, are entirely disregarded.
The output is a different dimension than the input, and is filled only with azure or white.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 8), dtype=int)

    # Define a function to check neighbors.
    def check_neighbors(r, c):
      for i in range(max(0, r -1), min(rows, r + 2)):
        for j in range(max(0, c-1), min(cols, c+2)):
          if input_grid[i,j] == 8:
            return True
      return False

    # Iterate using a sliding window approach
    output_row = 0
    output_col = 0

    for r in range(0, rows-2, 3): # check offsets for sampling data from input
      for c in range(0, cols-4, 5):
        if (check_neighbors(r,c)):
            output_grid[output_row, output_col] = 8

        if (check_neighbors(r, c+1)):
            output_grid[output_row, output_col + 1] = 8

        output_col += 2

        if output_col >=8:
           output_col = 0
           output_row += 1
           if output_row >=4:
              break


    return output_grid.tolist()
```
