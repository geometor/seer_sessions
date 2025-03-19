# 1e0a9b12 • 012 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Objects:** Find all non-zero, single-cell colored squares (objects) within the input grid.
2.  **Observe The Maroon 9:** Locate '9' (maroon) in the input. Note the change in position.
3. **Move Other Objects:** The 9 (maroon) moves to the output position that, relative to the 8 (cyan), occupies a location that is in the same column but one row below the 8 instead of one column to the right.
4. **All of the other objects stay in place except for the 9** The 8, 7, and 4 are unchanged in the output.
5.   **Output Grid:** Create the output grid with all other cells filled with '0' (white).
"""

import numpy as np

def find_object(grid, color):
    """Finds the coordinates of a single-cell object with the given color."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the rule."""

    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the position of 8 (cyan) and 9 (maroon).
    pos_8 = find_object(input_grid, 8)
    pos_9 = find_object(input_grid, 9)
    
    if pos_8 is not None and pos_9 is not None:

        # Calculate the new position of 9 relative to 8.
        new_pos_9 = (pos_8[0] + 1, pos_8[1])

        # move object in output
        output_grid[pos_9[0], pos_9[1]] = 0
        output_grid[new_pos_9[0], new_pos_9[1]] = 9

    return output_grid
```
