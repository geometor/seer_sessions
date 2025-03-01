# cbded52d • 012 • refine_coder

---
```python
"""
The transformation rule involves moving all green pixels (value 3) to the bottom of their respective columns, while leaving all other pixels (non-green) unaltered.
"""

import numpy as np

def find_green_pixels(grid):
    """Finds the positions of all green pixels in the grid."""
    green_positions = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                green_positions.append((r, c))
    return green_positions

def move_greens_to_bottom(grid):
    """Moves all green pixels to the bottom of their respective columns."""
    rows, cols = grid.shape
    new_grid = np.copy(grid)  # Work on a copy to avoid modifying original during iteration

    green_positions = find_green_pixels(new_grid)

    # Iterate by column, since that is the movement rule
    for c in range(cols):
      #collect the green pixels in this col
      col_green_pixels = []
      for r in range(rows):
        if new_grid[r,c] == 3:
          col_green_pixels.append((r,c))

      # Move green pixels down in the current column
      if len(col_green_pixels) > 0: #if greens in this col
        num_greens = len(col_green_pixels)
        #clear existing green positions
        for (r,c) in col_green_pixels:
            new_grid[r,c] = 0

        #fill in new green postions at bottom
        for i in range(num_greens):
          new_grid[rows - num_greens + i, c] = 3

    return new_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Move green pixels to the bottom
    output_grid = move_greens_to_bottom(output_grid)

    return output_grid
```
