"""
1.  **Identify the maroon object (color 9).** The object can be a 2x2 square or a 3x2/2x3 L-shape.
2.  **Move the object to the top edge of the grid (row 0).**
3. **Determine Object Orientation and Placement:**
    *   If the object is a 3x2 "L" shape (where the longer part of the L shape is horizontal), position the object at the top-left corner of the grid, such that its top-left pixel is at (0, 0). Maintain the L shape's original orientation.
    * If the object has height 2 and width 3 (where the longer part of the "L" is vertical), position the object such that the "horizontal" portion of the L is at the top edge.
    *   If the object is a 2x2 square, move it to the top-right corner of the grid.
    * if the object is a 3x2 "L", and the object is in the right part of the screen, keep the column.
4. **Maintain the object's shape and orientation** during the move, except as detailed in step 3.
"""

import numpy as np

def get_object(grid, color):
    """Finds the coordinates of an object with a specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return coords, (min_row, min_col), (height, width)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find the object
    object_coords, top_left, dims = get_object(input_grid, 9)
    if object_coords is None:
        return input_grid

    height, width = dims

    # Determine object orientation and target position
    if height == 3 and width == 2:  # 3x2 L (horizontal)
        target_row, target_col = 0, 0
    elif height == 2 and width == 3: #2x3 L
        target_row = 0
        # if in the right part of the screen keep column
        if top_left[1] >= (input_grid.shape[1] // 2):
            target_col = top_left[1]
        else:
            target_col = input_grid.shape[1]-width #align to the right edge
            #find the "horizontal" top part
            horizontal_rows = []
            for r in range(top_left[0], top_left[0]+height):
                count = np.count_nonzero(input_grid[r,:]==9)
                if count > 1:
                   horizontal_rows.append(r)
            row_offset = horizontal_rows[0] - top_left[0]
            target_col = top_left[1] - (top_left[0] - row_offset)
    elif height == 2 and width == 2:  # 2x2 square
        target_row, target_col = 0, input_grid.shape[1] - width
    else: # other shapes, don't move
        return input_grid
    
    # Calculate row and column offsets
    row_offset = top_left[0]
    col_offset = top_left[1]

    # Place object in output grid
    for coord in object_coords:
      if height == 2 and width == 3:
        new_row = coord[0] - row_offset
        new_col = coord[1] - col_offset + target_col
      else: #height == 3 and width == 2 or height == 2 and width == 2:
        new_row = coord[0] - row_offset + target_row
        new_col = coord[1] - col_offset + target_col
      if 0 <= new_row < output_grid.shape[0] and 0 <= new_col < output_grid.shape[1]:
        output_grid[new_row, new_col] = 9

    return output_grid