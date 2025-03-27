"""
1.  **Rotation:** Rotate the entire grid by 90 degrees counter-clockwise.
2.  **Reflection:** After rotation, reflect the grid by swapping elements across the *new* vertical axis.  If the rotated grid has dimensions `r x c`, then for a cell at `(i, j)` in the rotated grid, its new position after reflection will be `(i, c - 1 - j)`. In other words, the row index stays the same, while the column index is "flipped" relative to the *rotated* grid's center column.
"""

import numpy as np

def rotate_grid_counter_clockwise(grid):
    """Rotates a grid 90 degrees counter-clockwise."""
    return np.rot90(grid, k=1)

def reflect_grid_vertically_rotated(grid):
    """Reflects the grid across its vertical axis after rotation."""
    rows, cols = grid.shape
    reflected_grid = np.copy(grid)  # Create a copy to avoid modifying the original
    for i in range(rows):
        for j in range(cols):
            reflected_grid[i, j] = grid[i, cols - 1 - j]
    return reflected_grid

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid) # ensure it is a numpy array

    # Rotate the grid 90 degrees counter-clockwise
    rotated_grid = rotate_grid_counter_clockwise(input_grid)
    
    # Reflect the grid vertically relative to the *rotated* dimensions.
    output_grid = reflect_grid_vertically_rotated(rotated_grid)

    return output_grid.tolist() # return to list format