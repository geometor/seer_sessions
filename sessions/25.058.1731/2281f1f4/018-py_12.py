"""
1.  **Identify the Border:** Find all pixels along the edges (top, bottom, left, and right) of the input grid that have a non-zero color. These pixels constitute the "border."
2. **Check for solid border and infill:** If and only if the border is a solid gray (color 5) border that extends around the entire perimeter of the grid, then infill one step diagonally up and to the right of the bottom-left corner with blue color(1). If there isn't a solid border, do not perform any actions.
"""

import numpy as np

def is_solid_border(grid, border_color):
    """
    Checks if the grid has a solid border of the specified color.
    """
    rows, cols = grid.shape

    # Check top and bottom rows
    for col in range(cols):
        if grid[0, col] != border_color:
            return False
        if grid[rows - 1, col] != border_color:
            return False

    # Check left and right columns
    for row in range(1, rows - 1):
        if grid[row, 0] != border_color:
            return False
        if grid[row, cols - 1] != border_color:
            return False

    return True
    
def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check for solid gray border
    if is_solid_border(input_grid, 5):
        # Infill one step diagonally up and to the right of the bottom-left corner.
        if rows > 1 and cols > 1: #make sure not out of bounds
            output_grid[rows - 2, 1] = 1

    return output_grid