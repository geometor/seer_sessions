# bda2d7a6 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation swaps the colors of the outer border and the inner square, leaving the background (white pixels) unchanged. The positions and shapes of the objects remain constant.
"""

import numpy as np

def find_outer_border(grid):
    # Get the dimensions of the grid
    rows, cols = grid.shape

    # Create a mask for the outer border
    border_mask = np.zeros((rows, cols), dtype=bool)
    border_mask[0, :] = True
    border_mask[-1, :] = True
    border_mask[:, 0] = True
    border_mask[:, -1] = True

    return border_mask

def find_inner_square(grid, border_mask):
    # Find pixels that are not part of the border and not white (0)
    inner_mask = (~border_mask) & (grid != 0)
    
    # Find the color of first non-zero, non-border element.
    # extract the coords first
    coords = np.argwhere(inner_mask)

    if len(coords) == 0:
      return None, None
    
    first_coord = coords[0]
    inner_color = grid[first_coord[0], first_coord[1]]

    # ensure we only select the connected object
    inner_square_mask = (grid == inner_color) & (~border_mask)
    return inner_square_mask, inner_color

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid
    output_grid = np.copy(input_grid)

    # Find the outer border
    border_mask = find_outer_border(output_grid)
    outer_border_color = output_grid[0,0] # could improve this

    # Find the inner square
    inner_square_mask, inner_square_color = find_inner_square(output_grid, border_mask)

    if inner_square_mask is not None:
        # Swap colors between border and center
        output_grid[border_mask] = inner_square_color
        output_grid[inner_square_mask] = outer_border_color
    
    return output_grid
```
