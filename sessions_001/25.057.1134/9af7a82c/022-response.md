# 9af7a82c • 022 • refine_coder

---
```python
"""
Transforms a 3x3 input grid into a 5x3 output grid. The transformation
replicates the input grid and then adds rows based on the following rule:
- The input grid is copied to the output.
- Two additional rows are added.
- The additional rows are filled conditionally:
  - For each column, if '8' is present, identify its last occurrence.
  - If '8' appears in the column, add '8' to the 4th row in the correct column, otherwise add '0'
  - Add '0' to all columns for the 5th row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows + 2, cols), dtype=int)

    # Copy the input grid to the output grid
    output_grid[:rows, :] = input_grid

    # Iterate through each column
    for j in range(cols):
        input_column = input_grid[:, j]

        # Find the last occurrence of '8' in the column
        last_occurrence = -1
        for i in range(len(input_column) -1, -1, -1):
            if input_column[i] == 8:
                last_occurrence = i
                break

        # set the 4th row, add 8 if it was present
        if last_occurrence != -1:
            output_grid[3, j] = 8
        else:
            output_grid[3,j] = 0

        # set 0 for the 5th row
        output_grid[4,j] = 0

    return output_grid.tolist()
```
