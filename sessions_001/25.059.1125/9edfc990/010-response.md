# 9edfc990 • 010 • example_2 • investigate_coder

---
```python
"""
1. **Initialization:** Start with the output grid being a copy of the input grid.
2. **Flood Fill (Blue):** Iterate through every pixel of the *output* grid.
3. **Condition for change:** For any pixel that is not blue(1) in the *input* grid, replace the output pixel with blue, if either of following is satisfied
    - It is adjacent (up, down, left, or right) to any pixel colored blue(1)
4. **Stopping criterion:** The iteration through the output grid is completed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid neighbors (up, down, left, right) for a given cell.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def transform(input_grid):
    # initialize output_grid as copy of input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    # loop for pixels in output and flood with 1 if adjacent to existing 1
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] != 1:
          neighbors = get_neighbors(input_grid, r, c)
          for nr, nc in neighbors:
            if input_grid[nr,nc] == 1:
              output_grid[r,c] = 1
              break

    return output_grid
```
