# 6d0160f0 • 018 • refine_coder

---
```python
"""
The transformation preserves two horizontal gray lines and replaces most other colored pixels with white.
Only the colored cells in column 11 are kept, and their position is determined by the gray lines and the original non-gray and non-white pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the rows where the gray lines are.
    gray_rows = [r for r in range(rows) if 5 in input_grid[r]]

    # Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Keep the gray pixels (5) unchanged.  All other pixels become white except as described.
            if input_grid[r,c] != 5:
                output_grid[r,c] = 0

    # Iterate over columns
    for c in range(cols):
      # Find colored cells
      colored_cells = []
      for r in range(rows):
        if input_grid[r,c] != 0 and input_grid[r,c] != 5:
          colored_cells.append( (r, input_grid[r,c]) )

      # If gray lines and colors exist, transfer the colors to output grid
      if len(gray_rows) >= 2 and len(colored_cells) > 0:
        for i in range(len(colored_cells)):
            row_index = gray_rows[0] + i
            if row_index < gray_rows[1]:
              output_grid[row_index, 10] = colored_cells[i][1]
            
    return output_grid
```
