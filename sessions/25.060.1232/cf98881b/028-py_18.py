"""
Select a 4x4 subsection of input composed of yellow, blue and white pixels.
"""

import numpy as np

def find_subgrid_start(grid, subgrid_height, subgrid_width):
    # Iterate through the grid to find a suitable starting position for the subgrid.
    grid_height, grid_width = grid.shape
    for row in range(grid_height - subgrid_height + 1):
        for col in range(grid_width - subgrid_width + 1):
            if grid[row,col] == 4:
                return (row, col)  # return immediately on first match
    return None  # No suitable starting position found


def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)
   
    # Define height and width of sub grid
    sub_grid_height = 4
    sub_grid_width = 4
   
    # Find the top-left corner starting coordinates for the subgrid.
    start_coords = find_subgrid_start(input_grid, sub_grid_height, sub_grid_width)

    if start_coords:
        # initialize output
        output_grid = np.zeros((sub_grid_height, sub_grid_width), dtype=int)

        # Extract subgrid
        start_row, start_col = start_coords
        output_grid = input_grid[start_row:start_row + sub_grid_height,
                                   start_col:start_col + sub_grid_width]
    else: return None
    return output_grid.tolist()