"""
The transformation involves two objects: a red object (color 2) and a blue object (color 8).  The blue object remains stationary and acts as a reference. The red object's position is adjusted relative to the blue object.

1.  **Determine Movement Direction and Offset:**
    *   If the right edge of the red object is to the left of the left edge of the blue object, the red object moves horizontally. The red object's new position will have its right edge one pixel to the left of the blue object's left edge.
    *   If the bottom edge of the red object is above the top edge of the blue object, the red object moves vertically. The red object's new position will have its bottom edge one pixel above the blue object's top edge.
2. **No Overlap:** In cases where both horizontal and vertical movement conditions could apply, only one is selected. Priority is not yet determined.
3. **Object Preservation:** The shape and size of the red object remain constant during movement.
4. **Background:** All other pixels remain unchanged (background, color 0).
5. **No movement:** If neither condition above is met, the red object does not move.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of an object of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_object(grid, color):
    """extracts the contiguous block identified as an object"""
    coords = np.where(grid == color)
    # if the object does not exist, signal with an empty array with correct
    # shape
    if len(coords[0]) == 0:
       return np.array([])
    rows, cols = coords
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    obj = grid[min_row:max_row+1, min_col:max_col+1]
    # return sliced original object from input_grid
    return obj

def move_object(grid, obj, top_left_start, top_left_end):
    # size of object
    h, w = obj.shape
    # current location
    r0, c0 = top_left_start
    # target location
    r1, c1 = top_left_end

    # replace object location with background=0
    grid[r0:r0+h, c0:c0+w] = 0
    # move object into new location
    grid[r1:r1+h, c1:c1+w] = obj

    return grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the red object and blue object
    red_object = get_object(input_grid, 2)
    blue_object = get_object(input_grid, 8)

    # object bounding boxes
    red_box = find_object(input_grid, 2)
    blue_box = find_object(input_grid, 8)

    # if the object is not present, return
    if red_object.size == 0 or blue_object.size == 0:
       return output_grid

    red_top_left, red_bottom_right = red_box
    blue_top_left, blue_bottom_right = blue_box

    # check horizontal move
    if red_bottom_right[1] < blue_top_left[1]:
        # Compute the new position for the red object
        #  The right-most edge of shifted red block maintains a 1-pixel offset from the blue block
        _, red_w = red_object.shape

        # Compute shift, maintaining 1 pixel space before edge
        shift = blue_top_left[1] - red_w - red_top_left[1] - 1
        new_red_top_left = (red_top_left[0], red_top_left[1] + shift)

        # perform move
        output_grid = move_object(output_grid, red_object, red_top_left,
                                  new_red_top_left)
    # check vertical move
    elif red_bottom_right[0] < blue_top_left[0]:
        # Compute the new position for the red object.
        red_h, _ = red_object.shape
        # Compute vertical shift, maintaining 1-pixel space
        shift = blue_top_left[0] - red_h - red_top_left[0] -1
        new_red_top_left = (red_top_left[0] + shift, red_top_left[1])

        # perform move
        output_grid = move_object(output_grid, red_object, red_top_left,
                                    new_red_top_left)
    return output_grid