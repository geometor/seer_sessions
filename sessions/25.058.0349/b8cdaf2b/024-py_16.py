"""
Identify yellow (4) pixels in the bottom row. Move the entire yellow block two rows up only if all target positions two rows above are blank (0). If any target position is non-blank, the yellow block does not move.
"""

import numpy as np

def get_yellow_block(grid):
    """Finds the coordinates of yellow (4) pixels in the bottom row."""
    yellow_pixels = []
    rows, cols = grid.shape
    for x in range(cols):
        if grid[rows - 1, x] == 4:
            yellow_pixels.append((rows - 1, x))
    return yellow_pixels

def check_obstruction(grid, yellow_pixels):
    """Checks if any target position two rows above is non-blank."""
    for row, col in yellow_pixels:
        if grid[row - 2, col] != 0:
            return True  # Obstruction found
    return False  # No obstruction

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get yellow pixels in bottom row
    yellow_pixels = get_yellow_block(input_grid)

    # check obstruction
    if not yellow_pixels:
       return output_grid
    
    if check_obstruction(output_grid, yellow_pixels):
        return output_grid # Return original grid if obstructed
    
    # move if no obstruction
    for r, c in yellow_pixels:
        output_grid[r-2,c] = 4
        output_grid[r,c] = 0
    
    return output_grid