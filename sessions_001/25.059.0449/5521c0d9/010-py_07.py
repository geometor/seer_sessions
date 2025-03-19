"""
1.  **Move the yellow rectangle:** Move the top edge of the yellow rectangle up by six rows, keeping its original width.
2.  **Move the red rectangle**: Move the top of the red rectangle up 5 rows. Decrease red rectangle height by 1.
3.  **Move the blue rectangle:** Move the top of the blue rectangle up 2 rows.
4.  **Delete some rows and columns:** Delete white rows above and below colored blocks and shift the remaining blocks upwards, compacting the non-zero elements vertically.
"""

import numpy as np

def find_object(grid, color):
    """Finds the top-left and bottom-right coordinates of a colored object."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def get_object_shape(top_left, bottom_right):
    """Calculates the shape of the rectangle."""
    height = bottom_right[0] - top_left[0] + 1
    width = bottom_right[1] - top_left[1] + 1
    return height, width

def move_object(grid, top_left, bottom_right, new_top_left):
    """Moves an object to a new location and returns a new grid."""
   
    color = grid[top_left]
    height, width = get_object_shape(top_left, bottom_right)

    new_grid = np.copy(grid)

    #clear old
    new_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1] = 0    
    #add to new location
    new_grid[new_top_left[0]:new_top_left[0] + height, new_top_left[1]:new_top_left[1] + width] = color
  
    return new_grid

def shrink_object(grid, top_left, bottom_right, axis, amount):
    """Shrinks the object from bottom up. """

    color = grid[top_left]
    height, width = get_object_shape(top_left, bottom_right)

    new_grid = np.copy(grid)

    #clear old
    new_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1] = 0

    new_top_left = top_left
    new_height = height
    
    if axis == 'vertical':
      new_height = height-amount

    #add to new location
    new_grid[new_top_left[0]:new_top_left[0] + new_height, new_top_left[1]:new_top_left[1] + width] = color

    return new_grid

def remove_empty_rows(grid):
    """Removes rows that are entirely filled with 0s."""
    # Find rows that are not all zeros
    non_empty_rows = np.any(grid != 0, axis=1)
    # Filter the grid to keep only non-empty rows
    filtered_grid = grid[non_empty_rows]
    return filtered_grid


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find yellow rectangle
    yellow_top_left, yellow_bottom_right = find_object(output_grid, 4)
    if yellow_top_left is not None:
        new_yellow_top_left = (yellow_top_left[0] - 6, yellow_top_left[1])
        output_grid = move_object(output_grid, yellow_top_left, yellow_bottom_right, new_yellow_top_left)


    # Find and move red rectangle
    red_top_left, red_bottom_right = find_object(output_grid, 2)
    if red_top_left is not None:
        new_red_top_left = (red_top_left[0] - 5, red_top_left[1])
        output_grid = move_object(output_grid, red_top_left, red_bottom_right, new_red_top_left)
        red_top_left, red_bottom_right = find_object(output_grid, 2) #find again after move
        output_grid = shrink_object(output_grid, red_top_left, red_bottom_right, 'vertical', 1)

    # Find and move blue rectangle
    blue_top_left, blue_bottom_right = find_object(output_grid, 1)
    if blue_top_left is not None:
        new_blue_top_left = (blue_top_left[0] - 2, blue_top_left[1])
        output_grid = move_object(output_grid, blue_top_left, blue_bottom_right, new_blue_top_left)

    output_grid = remove_empty_rows(output_grid)
    return output_grid