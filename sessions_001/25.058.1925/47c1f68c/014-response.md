# 47c1f68c • 014 • refine_coder

---
```python
"""
The transformation rule involves identifying any azure (8) pixels in the input grid, finding the center of the azure region, and creating a standard-sized 'X' shape centered at that location in the output grid. All other colors in the input are replaced with white (0) in the output. The output grid has the same dimensions as the input.
"""

import numpy as np

def find_azure_center(grid):
    # Find the center of the azure region
    rows, cols = np.where(grid == 8)
    if len(rows) == 0:
        return None
    center_row = int(np.mean(rows))
    center_col = int(np.mean(cols))
    return center_row, center_col

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input, filled with white (0)
    output_grid = np.zeros_like(input_grid, dtype=int)
    
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the center of the azure region
    center = find_azure_center(input_grid)
    if center is None:
        return output_grid.tolist()  # Return blank grid if no azure is found

    center_row, center_col = center

    # Create the standard-sized 'X' shape using azure (8)
    # The 'X' extends one unit in each direction from the center
    for i in range(-1, 2):
        for j in range(-1, 2):
            if abs(i) == abs(j):  # Check for diagonal placement.
                row = center_row + i
                col = center_col + j
                # Ensure we're within grid boundaries
                if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                    output_grid[row, col] = 8

    return output_grid.tolist()
```
