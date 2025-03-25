```python
"""
1.  **Preserve Outer Frame:** Keep the first row and last row of the grid identical to the input.

2.  **Iterate Through Inner Rows:** For each row from the second row to the second-to-last row:

3.  **Iterate each inner cell:** Iterate each cell of the row from left to right, check its adjacent cells.

4.  **Check pattern and apply rule**: If the cell's left neighbor and the cell's right neighbor are the same, copy the right side neighbor's color into the current cell, if not, skip current cell.

5.  **Output:** The output will be generated.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Iterate through inner rows
    for i in range(1, rows - 1):
        # Iterate through columns, applying the rule
        for j in range(0, cols):  # Iterate through all columns
            
            if j > 0 and j < cols -1: # only apply rule for inner cells
                left_neighbor = output_grid[i, j - 1]
                right_neighbor = output_grid[i, j+1]
                if left_neighbor == right_neighbor:
                  output_grid[i,j] = right_neighbor

    return output_grid
```
