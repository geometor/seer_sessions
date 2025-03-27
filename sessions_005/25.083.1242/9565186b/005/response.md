```python
"""
Iterates through each row of the input grid. For each row, it checks if any cells
contain the colors 1 (blue), 2 (red), 3 (green), or 8 (azure). If a row contains
any of these colors, all cells in that entire row of the output grid are changed
to 5 (gray), unless that cell has a colour not in the trigger colours. If the
row does not contain the trigger colors, the entire row is copied unchanged
from the input grid to the output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row
    for i in range(rows):
        row = input_grid[i, :]
        # Check if the row contains any of the trigger colors (1, 2, 3, or 8)
        if any(color in row for color in [1, 2, 3, 8]):
            # Change all cells in the row to 5 (gray)
            for j in range(cols):
              if input_grid[i,j] in [1,2,3,8]:
                output_grid[i, j] = 5
        #else the copy has already happened

    return output_grid
```