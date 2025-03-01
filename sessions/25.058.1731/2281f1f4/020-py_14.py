"""
1.  **Identify the Border:** Examine the input grid to determine if it has a solid border. A solid border is defined as all pixels on the edges (top, bottom, left, and right) having the same color.
2.  **Check Border and Infill:** If a solid border exists, check its color.
3.  **Conditional Infill:**
    *   If the border is solid gray (color 5) *or* solid black (color 0), infill the cell one step diagonally up and to the right of the bottom-left corner with blue (color 1).
    *   Otherwise, do not modify the grid.
4.  If there is no solid border do not modify the grid.
"""

import numpy as np

def has_solid_border(grid):
    """
    Checks if the grid has a solid border of any color.
    Returns the border color if solid, otherwise None.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:  # Handle empty grids
        return None

    # Check top and bottom rows
    top_row_color = grid[0, 0]
    bottom_row_color = grid[rows - 1, 0]
    if not (all(grid[0, col] == top_row_color for col in range(cols)) and
            all(grid[rows - 1, col] == bottom_row_color for col in range(cols))):
        return None

    # Check left and right columns
    left_col_color = grid[0, 0]
    right_col_color = grid[0, cols - 1]
    if not (all(grid[row, 0] == left_col_color for row in range(rows)) and
            all(grid[row, cols - 1] == right_col_color for row in range(rows))):
        return None
    
    if top_row_color == bottom_row_color and top_row_color == left_col_color and top_row_color == right_col_color:
        return top_row_color
    else:
        return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check for solid border and get its color
    border_color = has_solid_border(input_grid)

    # Conditional infill based on border color
    if border_color == 5 or border_color == 0:  # Gray or Black
        if rows > 1 and cols > 1:  # Ensure not out of bounds
            output_grid[rows - 2, 1] = 1  # Infill with blue

    return output_grid