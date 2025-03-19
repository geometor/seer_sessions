# aba27056 • 018 • refine_coder

---
```python
"""
1.  **Identify Objects:** The input grid contains green pixels (source) and white pixels (target).
2.  **Propagate Yellow:** Any white pixel that is directly adjacent (horizontally, vertically, or diagonally) to a green pixel changes to yellow.
3. **No Other Changes:** White pixels not adjacent to a green pixel are unchanged. Green pixels are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the input grid
    for row in range(rows):
        for col in range(cols):
            # Propogate Yellow: change to Yellow if adjacent to Green.
            if input_grid[row, col] == 0:  # Check if the pixel is white
                neighbors = get_neighbors(input_grid, row, col)
                if 3 in neighbors:  # Check if any neighbor is green
                    output_grid[row, col] = 4  # Change to yellow

    return output_grid
```
