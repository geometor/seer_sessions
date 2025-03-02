# 6e02f1e3 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the main diagonal:**  Locate the cells that form a diagonal line from the top-left corner to the bottom-right corner of the input grid.
2.  **Replace Diagonal:** Change the value of all cells located on the main diagonal to 5 (gray).
3. **Replace Off-Diagonal:** Change value of the cells *not* on the main diagonal to 0 (white)
4.  **Output:** The resulting grid is the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid and apply the transformation.
    for i in range(rows):
        for j in range(cols):
            if i == j:  # Check for main diagonal
                output_grid[i, j] = 5  # set to 5
            else:
                output_grid[i, j] = 0 #set to 0

    return output_grid
```
