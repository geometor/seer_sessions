```python
"""
The input grid is rotated 90 degrees clockwise and then the order of rows are inverted to create the output grid.
"""

import numpy as np

def rotate_grid_clockwise(grid):
    """Rotates a grid 90 degrees clockwise."""
    return np.rot90(grid, k=-1).tolist()

def invert_grid_rows(grid):
    """Inverts(reverse) the order of rows in a grid."""
    return grid[::-1]

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise and
    then inverting the order of the rows.
    """
    # Rotate the grid 90 degrees clockwise.
    rotated_grid = rotate_grid_clockwise(input_grid)

    # Invert the order of rows.
    output_grid = invert_grid_rows(rotated_grid)

    return output_grid
```
