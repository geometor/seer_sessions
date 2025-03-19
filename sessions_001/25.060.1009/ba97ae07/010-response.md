# ba97ae07 • 010 • example_2 • investigate_coder

---
```python
"""
Change the color of the pixels in the blue stripe to magenta, but *only* where it intersects the magenta vertical stripe.
"""

import numpy as np

def find_stripe(grid, color, orientation):
    # Find a stripe of a given color and orientation.
    if orientation == 'vertical':
        for col in range(grid.shape[1]):
            if all(grid[:, col] == color) or all(grid[:3, col] == color) and all(grid[4:,col] == color) :
                return col
    elif orientation == 'horizontal':
        for row in range(grid.shape[0]):
            if all(grid[row, :] == color):
                return row
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find magenta vertical stripe
    magenta_col = find_stripe(input_grid, 6, 'vertical')

    # find blue horizontal stripe
    blue_row = find_stripe(input_grid, 1, 'horizontal')

   #Change blue cells to magenta at intersection, assuming we've correctly located the row and col
    if blue_row is not None and magenta_col is not None:
       #input grid has a non-contiguous vertical stripe:
       output_grid[blue_row, magenta_col] = 6
       output_grid[blue_row, magenta_col + 1] = 6

    return output_grid
```

