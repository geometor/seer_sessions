# 7447852a • 002 • example_1 • investigate_coder

---
```python
"""
1. **Identify '2's:** Locate all pixels in the input grid with the value '2' (red).

2. **Locate Targets:** Find all '0' (white) pixels directly adjacent (horizontally or vertically, not diagonally) to the '2's.

3. **Conditional Modification:** There was at least one instance of a '0' adjacent to more than one 2. If this happens, fill with yellow (value 4).

4.  **Fill:** Transform each located '0' adjacent to a `2` pixel into a '4' (yellow).

5.  **Preserve**: All other pixel locations in the input keep their value in the output.

6.  **Output**: The result is the modified grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify '2's
    red_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 2]

    # Locate Targets and Fill
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                neighbor_coords = get_neighbors(input_grid, r, c)
                adjacent_reds = 0
                for nr, nc in neighbor_coords:
                    if input_grid[nr, nc] == 2:
                        adjacent_reds += 1
                if adjacent_reds > 0:
                   output_grid[r,c] = 4
    return output_grid.tolist()
```
