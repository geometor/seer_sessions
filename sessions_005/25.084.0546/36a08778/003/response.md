```python
"""
Replace orange pixels on the left edge with magenta.
Propagate magenta color from the left, replacing orange pixels.
Propagation requires adjacency to both existing magenta and red pixels.
Stop when no more orange pixels meet the adjacency condition.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Replace leftmost orange with magenta.
    for r in range(rows):
        if output_grid[r, 0] == 7:
            output_grid[r, 0] = 6

    # Iterative propagation of magenta.
    while True:
        changed = False
        new_grid = np.copy(output_grid)  # Work on a copy to avoid in-place modification issues.
        for r in range(rows):
            for c in range(cols):
                if new_grid[r, c] == 7:  # Check if it's orange.
                    # Check for adjacency to magenta and red.
                    adjacent_to_magenta = False
                    adjacent_to_red = False

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if new_grid[nr, nc] == 6:
                                adjacent_to_magenta = True
                            if new_grid[nr, nc] == 2:
                                adjacent_to_red = True

                    if adjacent_to_magenta and adjacent_to_red:
                        output_grid[r, c] = 6  # Replace orange with magenta.
                        changed = True

        if not changed:  # Stop if no changes occurred in this iteration.
            break

    return output_grid
```