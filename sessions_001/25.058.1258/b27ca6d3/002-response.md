# b27ca6d3 • 002 • example_2 • investigate_coder

---
```python
"""
The transformation rule identifies red pixels (value 2) in the input grid. For each red pixel, it checks if a 3x3 green (value 3) block centered on the red pixel can be placed without going out of bounds and without intersecting or being adjacent (except to the original red) with other non-white pixels. If these conditions are met, the 3x3 green block is created in the output grid. All other pixels remain unchanged.
"""

import numpy as np

def get_objects(grid, color):
    """Finds coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def is_valid_position(grid, r, c):
    """Checks if the row and column are within the grid bounds."""
    rows, cols = grid.shape
    return 0 <= r < rows and 0 <= c < cols

def can_place_3x3(grid, r, c, ignore_color):
    """
    Checks if a 3x3 block centered at (r, c) can be placed without going out of bounds and without intersecting or being adjacent to pixels of colors other than ignore_color and 0.
    """
    rows, cols = grid.shape

    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            if not is_valid_position(grid, i, j):
                return False  # Out of bounds
            if grid[i, j] != 0 and grid[i,j] != ignore_color:
                if (i != r or j != c):
                    return False # intersects different color than the ignored
    
    # check all adjacent positions to the 9 positions to make sure not adjacent to other colors
    for i in range(r - 2, r + 3):
        for j in range(c - 2, c + 3):
           if abs(i-r) == 2 or abs(j-c) == 2:
              if is_valid_position(grid, i, j):
                 if grid[i,j] != 0:
                     return False

    return True

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.copy(input_grid)
    red_pixels = get_objects(input_grid, 2)

    # Iterate through red pixels
    for r, c in red_pixels:
        # Check if a 3x3 green block can be placed
        if can_place_3x3(output_grid, r, c, 2):
            # Place the 3x3 green block
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    output_grid[i, j] = 3

    return output_grid
```
