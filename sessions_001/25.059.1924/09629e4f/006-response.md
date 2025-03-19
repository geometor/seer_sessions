# 09629e4f • 006 • refine_coder

---
```python
"""
Transforms the input grid by:
1. Dividing it into three regions (top, middle, bottom) based on grey (5) horizontal lines.
2. Top Region: Creates a 3x3 red block on the left and clears the rest.
3. Middle Region: Creates a vertical black line on the left edge, keeps grey objects, and clears others.
4. Bottom Region: Creates a 3x3 magenta block on the left and clears the rest.
"""

import numpy as np

def get_regions(grid):
    """
    Divides the grid into three regions based on grey (5) horizontal lines.
    Assumes there are always two such lines.
    """
    grey_rows = np.where((grid == 5).all(axis=1))[0]
    top_region = grid[:grey_rows[0], :]
    middle_region = grid[grey_rows[0] + 1:grey_rows[1], :]
    bottom_region = grid[grey_rows[1] + 1:, :]
    return top_region, middle_region, bottom_region, grey_rows

def find_objects(grid, color):
    """
    Finds objects of a specified color in a grid. Returns a list of coordinates.
    """
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Get regions and divider row indices
    top_region, middle_region, bottom_region, grey_rows = get_regions(input_grid)

    # Transform Top Region
    output_grid[:grey_rows[0], :3] = 2  # 3x3 red block
    output_grid[:grey_rows[0], 3:] = 0 #clear area

    # Transform Middle Region
    output_grid[grey_rows[0] + 1:grey_rows[1], 0] = 0  # Vertical black line
    # Keep grey (5) objects, clear others.
    for r in range(grey_rows[0] + 1, grey_rows[1]):
        for c in range(output_grid.shape[1]):
          if output_grid[r,c] != 5:
            output_grid[r,c] = 0

    # Transform Bottom Region
    output_grid[grey_rows[1] + 1:, :3] = 6  # 3x3 magenta block
    output_grid[grey_rows[1] + 1:, 3:] = 0  # Clear the rest

    return output_grid
```
