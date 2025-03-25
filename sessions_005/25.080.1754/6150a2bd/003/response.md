```python
"""
The transformation rotates counterclockwise by 90 degrees, followed by swapping elements on last column with elements on the first column.

1.  **Rotation:** Rotate the entire grid by 90 degrees counter-clockwise.
2.  **Reflection (partial):** swap the first and last column of the rotated array.
"""

import numpy as np

def rotate_grid_counter_clockwise(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def swap_first_and_last_columns(grid):
    """Swaps the first and last columns of a grid."""
    grid[:, [0, -1]] = grid[:, [-1, 0]]
    return grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid) # ensure it is a numpy array

    # Rotate the grid 90 degrees counter-clockwise
    rotated_grid = rotate_grid_counter_clockwise(input_grid)
    
    # swap the first and last columns.
    output_grid = swap_first_and_last_columns(rotated_grid)

    return output_grid.tolist() # return to list format
```