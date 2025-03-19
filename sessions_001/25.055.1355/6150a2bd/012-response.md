# 6150a2bd • 012 • refine_coder

---
```python
"""
Identify the diagonal line of azure (color 8) pixels extending from the
bottom-left corner to the top-right corner.  Shift this diagonal line down by
one row. The empty spaces created by the shift are filled with white pixels
(color 0). The rest of the grid should be filled by azure pixels.
"""

import numpy as np

def find_diagonal_line(grid):
    """Finds the coordinates of the diagonal azure line."""
    grid_np = np.array(grid)
    rows, cols = grid_np.shape
    line_coords = []
    for i in range(rows):
        for j in range(cols):
            if grid_np[i, j] == 8 and (rows - 1 - i) == j: # Check for bottom-left to top-right diagonal
                line_coords.append((i, j))
    return line_coords

def transform(input_grid):
    # Initialize output grid with all azure (8)
    input_np = np.array(input_grid)
    rows, cols = input_np.shape
    output_np = np.full((rows, cols), 8)

    # Find the diagonal line coordinates
    line_coords = find_diagonal_line(input_grid)

    # Shift the diagonal line down by one row and fill with white(0)
    for r, c in line_coords:
        if r + 1 < rows:  # Check bounds
            output_np[r + 1, c] = 8
        output_np[r,c] = 0


    output_grid = output_np.tolist()
    return output_grid
```
