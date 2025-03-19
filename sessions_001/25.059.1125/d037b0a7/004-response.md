# d037b0a7 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Preserve Non-White:** Iterate through the input grid. If a pixel is not white (0), keep its value unchanged in the corresponding position of the output grid.
2.  **Propagate Magenta and Yellow:** For each white (0) pixel in the input grid:
    *   Check its immediate neighbors (up, down, left, right). Diagonal is not considered to be adjacent.
    *   If any neighbor is magenta (6), change the white pixel to magenta (6) in the output grid.
    *    If any neighbor is yellow (4), change the white pixel to yellow(4) in the output grid.
3. **Fill Remaining:** In this example, there are no remaining white cells. If white cells had remained, those would stay white.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the immediate neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row+1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col-1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col+1])  # Right
    return neighbors

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Preserve Non-White Pixels
            if input_grid[row, col] != 0:
                continue  # Skip non-white pixels
            
            # Propagate Magenta and Yellow
            neighbors = get_neighbors(input_grid, row, col)
            if 6 in neighbors:
                output_grid[row, col] = 6  # Change to magenta
            elif 4 in neighbors:
                output_grid[row,col] = 4 # Change to yellow

    return output_grid
```
