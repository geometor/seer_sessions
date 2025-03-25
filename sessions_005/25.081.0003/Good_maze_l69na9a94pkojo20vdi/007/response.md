```python
"""
1.  **Identify Key Pixels:** Find all yellow (4) and red (2) pixels in the input grid. Black pixels are considered background and do not change.

2.  **Yellow Pixel Pairs:** Consider pairs of yellow pixels.

3.  **Path Creation:**  For each yellow pixel (or pair, if clearly related by being the only yellows in a row or column, or by being at the "ends" of a diagonal):
    *   Find Red pixels (2) that lie on direct horizontal or vertical paths, which are obstructed only by other red pixels.
    *   Change those red pixels to azure (8).

4. Result: The output is the original grid with red pixels that connect the yellows changed to azure.
"""

import numpy as np

def get_positions(grid, color):
    """Finds positions of pixels of a specific color."""
    positions = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color:
                positions.append((r_idx, c_idx))
    return positions

def transform(input_grid):
    """Transforms the input grid according to the maze-solving rules."""

    # initialize output_grid
    output_grid = np.copy(input_grid).astype(int)
    yellow_positions = get_positions(input_grid, 4)
    red_positions = get_positions(input_grid, 2)


    # Iterate through rows and columns to find paths
    for r_idx, row in enumerate(input_grid):
      yellow_in_row = [c_idx for r_idx2, c_idx in yellow_positions if r_idx2 == r_idx]
      if len(yellow_in_row) > 1 :
        min_yellow = min(yellow_in_row)
        max_yellow = max(yellow_in_row)
        for c_idx in range(min_yellow + 1, max_yellow):
            if input_grid[r_idx, c_idx] == 2:
              output_grid[r_idx, c_idx] = 8

    for c_idx in range(len(input_grid[0])):
        yellow_in_col = [r_idx for r_idx, c_idx2 in yellow_positions if c_idx2 == c_idx]
        if len(yellow_in_col) > 1:
            min_yellow = min(yellow_in_col)
            max_yellow = max(yellow_in_col)
            for r_idx in range(min_yellow + 1, max_yellow):
                if input_grid[r_idx, c_idx] == 2:
                    output_grid[r_idx, c_idx] = 8

    return output_grid
```
