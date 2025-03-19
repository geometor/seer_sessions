# 5614dbcf • 008 • example_1 • investigate_coder

---
```python
"""
1. Divide the input 9x9 grid into nine 3x3 subgrids.
2. For each 3x3 subgrid, select the color/digit value in the top-left cell (row 1, column 1 of subgrid).
3. Construct a new 3x3 output grid.
4. Place the selected color/digit from each subgrid into the corresponding cell of the output grid. For example, color of top-left input sub-grid is placed at the output's top-left cell.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through each 3x3 subgrid
    for i in range(3):
        for j in range(3):
            # Calculate the starting row and column indices of the subgrid
            start_row = i * 3
            start_col = j * 3

            # Select the top-left cell's value of the subgrid
            selected_value = input_grid[start_row][start_col]

            # Place the selected value into the corresponding cell of the output grid
            output_grid[i][j] = selected_value

    return output_grid
```

