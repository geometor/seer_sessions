# 50846271 • 004 • refine_coder

---
```python
"""
1.  **Identify Red Objects:** Locate all contiguous regions of red (2) pixels. These are the "red objects".
2.  **Determine Extremities:** For each red pixel within a red object, count its red neighbors (up, down, left, right - not diagonal). If a red pixel has *one or fewer* red neighbors, it's an "extremity".
3. **Determine Inner**: Any red pixel which is *not* an extremity, will be considered "inner".
4.  **Construct Output:** Create the output grid as follows:
    *   Copy all non-red pixels from the input grid to the output grid, preserving their values.
    *   For each "inner" red pixel identified in step 3, set corresponding pixel of the output to azure(8)
    *   For each "extremity" red pixel identified in step 2, keep its value to red (2).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in a grid (diagonal not considered)."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def is_extremity(grid, row, col):
    """Checks if a red pixel is an extremity."""
    if grid[row, col] != 2:
        return False

    neighbors = get_neighbors(grid, row, col)
    red_neighbors = 0
    for r, c in neighbors:
        if grid[r, c] == 2:
            red_neighbors += 1

    return red_neighbors <= 1

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)    # Initialize output grid

    rows, cols = input_grid.shape

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            # check if red and NOT an extremity (i.e., inner)
            if input_grid[row,col] == 2 and not is_extremity(input_grid, row, col):
                output_grid[row, col] = 8  # change to azure

    return output_grid.tolist()
```
