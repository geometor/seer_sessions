# 0520fde7 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Center Column:** Find the column in the input grid that contains the gray (5) pixels. This column represents the x-coordinate of the center of the output.
2.  **Determine output value row:** The row number of the output is same as the input.
3. **Create Subgrid:** make all values in the subgrid white (0) except the central one which should be red (2)
"""

import numpy as np

def find_gray_column(grid):
    # Find the column index containing gray (5) pixels.
    for j in range(grid.shape[1]):
        for i in range(grid.shape[0]):
            if grid[i, j] == 5:
                return j
    return -1  # Return -1 if no gray pixel is found

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the column containing the gray pixel
    center_column = find_gray_column(input_grid)

    # Initialize the output grid as 3x3 with all white (0) pixels
    output_grid = np.zeros((3, 3), dtype=int)

    # determine center row and column
    center_row = 1
    center_col = 1

    # Place the red (2) pixel in the center of output
    output_grid[center_row, center_col] = 2

    return output_grid.tolist()
```
