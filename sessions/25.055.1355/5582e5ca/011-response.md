# 5582e5ca • 011 • refine_coder

---
```python
"""
The transformation rule is to replace the uniform color of the input grid with color 9 (maroon). If a grid consists only of a single color, replace all pixels of that color with color 9.  If the grid has a border, replace the border color with color 9.
"""

import numpy as np

def get_border_and_inside_colors(grid):
    """
    Identifies the border and inside colors of a grid.
    Returns None for inside_color if the grid isn't a simple border/inside structure.
    """
    rows, cols = grid.shape
    border_color = grid[0, 0]
    inside_color = None

    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
                if grid[r,c] != border_color:
                  return border_color, None #not a simple border
            elif inside_color is None:
                inside_color = grid[r, c]
            elif grid[r,c] != inside_color:
                return border_color, None # Not a simple border and fill

    return border_color, inside_color
def is_uniform(grid):
    """Checks if a grid is of uniform color."""
    first_color = grid[0, 0]
    return np.all(grid == first_color)

def transform(input_grid):
    """Transforms the input grid by replacing its uniform color with maroon (color 9)."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)  # Start with a copy
    rows, cols = input_grid.shape
    border_color, inside_color = get_border_and_inside_colors(input_grid)
    if inside_color is None and border_color is not None:
        # Not uniform, but might still be a border of a single color

      if is_uniform(input_grid):
          output_grid[:] = 9
      else: #not a border and fill
          return output_grid # No change if it's not a simple border/fill
    elif inside_color is not None: #we have border and fill:
        for r in range(rows):
          for c in range(cols):
              if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1):
                  output_grid[r,c] = 9 #replace with maroon
    else: #uniform
      output_grid[:] = 9  # Replace all with maroon

    return output_grid
```
