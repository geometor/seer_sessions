"""
1.  **Identify Objects:** Find all contiguous regions of red (2) pixels and grey (5) pixels in the input grid. These are treated as separate objects.

2.  **Red Bounding Box:** Determine the minimum bounding box that encloses the red object.

3. **Preserve Red:** Copy the red object from the input to the output

4.  **Grey Object Placement:**
    *   Find the bottom edge of the red object's bounding box.
    *   Find the right edge of the red object's bounding box.
    *.  Move the grey object so that it is within the red bounding box
    *.  The grey object's bottom edge aligns with the bottom edge of the red object's bounding box.
    *.  The grey object's right edge aligns with the right edge of the red object's bounding box.

5.  **Background:** All other pixels in the output grid that do not contain the red or grey object are set to white (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return []  # Return empty list if no objects found
    return coords

def bounding_box(coords):
    """Calculates the bounding box of a set of coordinates."""
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_row, max_row, min_col, max_col

def move_object(grid, coords, row_shift, col_shift, color):
    """Moves an object to a new location in the grid, overwriting values"""
    new_coords = []

    # remove old
    for r, c in coords:
        grid[r,c] = 0

    # add new
    for r, c in coords:
      new_coords.append( (r + row_shift, c + col_shift) )
      grid[r + row_shift, c + col_shift] = color

    return new_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects
    red_coords = find_objects(input_grid, 2)
    grey_coords = find_objects(input_grid, 5)

    # Copy red object
    for r, c in red_coords:
        output_grid[r, c] = 2

    # Red Bounding Box
    if red_coords:
        red_min_row, red_max_row, red_min_col, red_max_col = bounding_box(red_coords)

        # Grey Object Placement
        if grey_coords:
            grey_height = bounding_box(grey_coords)[1] - bounding_box(grey_coords)[0] + 1
            grey_width = bounding_box(grey_coords)[3] - bounding_box(grey_coords)[2] + 1
            
            # calculate shifts
            row_shift = red_max_row - (bounding_box(grey_coords)[0] + grey_height -1) 
            col_shift = red_max_col - (bounding_box(grey_coords)[2] + grey_width - 1)
            
            # apply shift
            move_object(output_grid, grey_coords, row_shift, col_shift, 5)

    return output_grid