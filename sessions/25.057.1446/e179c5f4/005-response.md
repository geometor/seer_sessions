# e179c5f4 • 005 • refine_coder

---
```python
"""
1.  **Invariant 5s:** If a pixel has the value 5 (gray), its value remains unchanged.

2.  **Transforming 0s:** If a pixel has the value 0 (white):
    *   If a 0 (white) pixel is diagonally adjacent to another 0 (white) pixel, it transforms into an 8 (azure).
    *   If a 0 (white) pixel is cardinally adjacent (up, down, left, or right - but *not* diagonally) to another 0 (white) pixel, it becomes a 1 (blue).
    * If neither of the above are true for an input of 0, it is ambiguous. The provided examples do not provide information about other scenarios.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Returns a dictionary of adjacent neighbors and their values."""
    rows, cols = grid.shape
    neighbors = {}
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue  # Skip the cell itself
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors[(nr, nc)] = grid[nr, nc]
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    # Iterate over each pixel
    for r in range(rows):
        for c in range(cols):
            # Invariant 5s
            if input_grid[r, c] == 5:
                continue  # Output is the same as input
            # Transforming 0s
            elif input_grid[r, c] == 0:
                neighbors = get_neighbors(input_grid, r, c)
                found_diagonal_zero = False
                found_cardinal_zero = False

                for (nr, nc), value in neighbors.items():
                    if value == 0:
                        if abs(nr - r) == 1 and abs(nc - c) == 1:
                            found_diagonal_zero = True
                        elif (abs(nr - r) == 1 and abs(nc - c) == 0) or (abs(nr-r) == 0 and abs(nc -c) == 1):
                            found_cardinal_zero = True
                if found_diagonal_zero:
                  output_grid[r,c] = 8
                elif found_cardinal_zero:
                  output_grid[r,c] = 1

    return output_grid
```
