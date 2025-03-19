# 6e02f1e3 • 006 • refine_coder

---
```python
"""
1.  **Identify the Main Diagonal:** Locate the cells forming the main diagonal (top-left to bottom-right) of the input grid. A cell is on the main diagonal if its row index is equal to its column index.
2.  **Set Diagonal to Gray:** Change the value of all cells on the main diagonal to 5 (gray).
3. **Set Off-Diagonal to White:** Chang the value of the cells *not* on the main diagonal to 0 (white).
4.  **Output:** The modified grid is the output.
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

