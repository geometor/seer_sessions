"""
The transformation rule involves identifying a red rectangle and a yellow object in the input grid. The yellow object is then reshaped into a 1-pixel wide column with the same height as the red rectangle. This new yellow column is placed directly above the red rectangle, aligned by their left edges.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None
    # Calculate top-left and bottom-right coordinates
    min_y, min_x = coords.min(axis=0)
    max_y, max_x = coords.max(axis=0)
    # Extract the object's shape
    shape = grid[min_y:max_y+1, min_x:max_x+1]
    return (min_x, min_y), shape, (min_x, min_y)

def move_object(output_grid, shape, new_position):
    # Place the shape onto the output grid at the new position
    x, y = new_position
    height, width = shape.shape
    output_grid[y:y+height, x:x+width] = shape
    return output_grid

def clear_color(grid, color):
    #set all pixels of the color to zero
    grid[grid == color] = 0
    return grid

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find the red rectangle
    red_top_left, red_shape, _ = find_object(input_grid, 2)
    if red_top_left is None:  # Handle cases where there's no red object.
        return output_grid

    # Find the yellow shape
    yellow_top_left, yellow_shape, yellow_origin = find_object(input_grid, 4)
    if yellow_top_left is None:  # Handle cases where there's no yellow object.
        return output_grid

    # Create the reshaped yellow object: 1-pixel wide, height of red rectangle
    new_yellow_shape = np.full((red_shape.shape[0], 1), 4)

    # Determine the new position for the yellow shape: above red, left-aligned
    new_yellow_position = (red_top_left[0] - red_shape.shape[0], red_top_left[1])

    # Clear the original yellow pixels from the output grid
    output_grid = clear_color(output_grid, 4)

    # Move the reshaped yellow shape to its new position
    output_grid = move_object(output_grid, new_yellow_shape, new_yellow_position)

    return output_grid