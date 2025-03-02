# a3325580 • 014 • example_2 • investigate_coder

---
```python
"""
Transforms a grid by extracting the leftmost and rightmost non-background colors,
and creating a two-column output grid where the first column is filled with the leftmost color
and the second column is filled with the rightmost color. The output grid has the same height as the original grid.
"""

import numpy as np

def get_leftmost_non_background_color(grid):
    """Finds the leftmost non-background (non-zero) color in the grid."""
    for x in range(grid.shape[1]):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
    return 0  # Should not be reached for non empty grids

def get_rightmost_non_background_color(grid):
     """Finds the rightmost non-background (non-zero) color in the grid."""
     for x in range(grid.shape[1]-1,-1,-1):
        for y in range(grid.shape[0]):
            if grid[y, x] != 0:
                return grid[y, x]
     return 0

def transform(input_grid):
    # Find the leftmost and rightmost non-background colors
    leftmost_color = get_leftmost_non_background_color(input_grid)
    rightmost_color = get_rightmost_non_background_color(input_grid)

    # Determine the height of original and output grid (same height)
    # original height, less 1 when the bottom line is all zeros.
    
    height = input_grid.shape[0]
    if(np.all(input_grid[-1] == 0)):
        height -= 1

    # Initialize the output grid with two columns and the determined height
    output_grid = np.zeros((height, 2), dtype=int)

    # Fill the first column with the leftmost color
    output_grid[:, 0] = leftmost_color

    # Fill the second column with the rightmost color
    output_grid[:, 1] = rightmost_color

    return output_grid
```
