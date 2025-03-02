"""
1.  **Identify Anchors:** The yellow '4' and orange '7' pixels, which are vertically adjacent, form an anchor group and do not change their relative positions.

2.  **Identify Movers:** The azure '8' and maroon '9' are mover elements.

3.  **Move '8':** Move the azure '8' pixel downward as far as possible within the grid boundaries.

4.  **Move '9':** Move the maroon '9' such that it is positioned to the right of '8', maintain the original row index of the moved '8'. If '8' is already located at the bottom, '9' goes to the bottom right most position.

5.  **Preserve Background:** All other white '0' pixels remain unchanged.
"""

import numpy as np

def find_object(grid, value):
    # Find the coordinates of a specific value in the grid.
    coords = np.argwhere(grid == value)
    return coords[0] if coords.size > 0 else None

def move_element_down(grid, start_coords):
    # Move an element down as far as possible.
    row, col = start_coords
    while row + 1 < grid.shape[0] and grid[row + 1, col] == 0:
        row += 1
    return row, col

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find anchor elements (4 and 7).
    coords_4 = find_object(output_grid, 4)
    coords_7 = find_object(output_grid, 7)

    # Find mover elements (8 and 9).
    coords_8 = find_object(output_grid, 8)
    coords_9 = find_object(output_grid, 9)
    
    if coords_8 is not None:
        # Move '8' down.
        new_coords_8 = move_element_down(output_grid, coords_8)

        # Clear original position of '8'.
        output_grid[coords_8[0], coords_8[1]] = 0
        # Set new position of '8'.
        output_grid[new_coords_8[0], new_coords_8[1]] = 8

    if coords_9 is not None and coords_8 is not None:
        # Move '9' to the right of new '8' position.
        # Clear the orginal '9'
        output_grid[coords_9[0], coords_9[1]] = 0

        # Check to see if '8' is in bottom row
        if new_coords_8[0] == output_grid.shape[0] - 1 :
            output_grid[new_coords_8[0], output_grid.shape[1] - 1] = 9
        else:
            output_grid[new_coords_8[0], new_coords_8[1] + 1] = 9

    return output_grid