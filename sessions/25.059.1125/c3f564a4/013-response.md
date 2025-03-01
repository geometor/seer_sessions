# c3f564a4 • 013 • refine_coder

---
```python
"""
1.  **Identify the Cross:** Find contiguous regions of black (0) pixels. If no black pixels are present, the input grid remains unchanged.

2.  **Find the Center:** Calculate the center of the black pixel region. The center is defined as the average row and average column of all black pixels.

3. **Remove part of Cross**:
    - all 0 pixels on a vertical line with the cross center.
    - and, any 0 pixels on the same row as the cross center.

4.  **Background Preservation:** Pixels that are not part of the identified "cross part" should remain unchanged.
"""

import numpy as np

def find_cross_center(grid):
    # Find the center of the cross shape
    rows, cols = np.where(grid == 0)
    if len(rows) == 0:
        return None
    center_row = int(np.mean(rows))
    center_col = int(np.mean(cols))
    return center_row, center_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the center of the cross
    center = find_cross_center(input_grid)
    if center is None:
      return output_grid  # No cross found, return original grid
    center_row, center_col = center

    # Iterate through the grid
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            # Remove 0 pixels that are vertically aligned with center or on the same row.
            if input_grid[row, col] == 0:  # Check if the pixel is black
                if col == center_col or row == center_row:
                   output_grid[row,col] = input_grid[row, col] if (col != center_col and row != center_row) else output_grid[row,col] * 0 + input_grid[row,col] ^ input_grid[row,col]


    return output_grid
```
