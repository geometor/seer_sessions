# 7447852a • 006 • refine_coder

---
```python
"""
1.  **Copy:** Create a copy of the input grid as the output grid.
2.  **Iterate:** Examine each pixel in the input grid.
3.  **Identify Red:** If a pixel is red (value 2):
    a. **Count Neighbors:** Count the number of adjacent red pixels (horizontally and vertically, but not diagonally).
    b. **Apply Rule:** If a red pixel has exactly two adjacent red pixels that are horizontal and vertical neighbors, change its color to yellow (value 4) in the *output* grid.
4.  **Return:** Return the modified output grid. All other pixels remain unchanged.
"""

import numpy as np

def count_adjacent_reds(grid, row, col):
    """Counts the number of red neighbors (horizontal and vertical) for a given cell."""
    count = 0
    rows, cols = grid.shape
    if row > 0 and grid[row-1, col] == 2:
        count += 1
    if row < rows - 1 and grid[row+1, col] == 2:
        count += 1
    if col > 0 and grid[row, col-1] == 2:
        count += 1
    if col < cols - 1 and grid[row, col+1] == 2:
        count += 1
    return count

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 2: #if red pixel
              adjacent_reds = count_adjacent_reds(input_grid, row, col)
              if adjacent_reds == 2 :
                output_grid[row,col] = 4
    return output_grid
```
