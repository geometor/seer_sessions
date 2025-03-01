"""
1.  Identify the Cross: Locate the yellow pixels in the input grid that form a cross shape. A cross is defined as a central pixel with four "arms" extending outwards in the four cardinal directions (up, down, left, right). The arms can be of any length (including zero, meaning just the center pixel is present). There will only be one cross.
2.  Extend the Arms:**  For each arm of the cross, extend it outwards in its respective direction until it reaches the edge of the input grid. This extension should maintain a straight line and be composed of yellow pixels.
3. **Create the Filled Rectangle:** Create a filled rectangle using yellow (value 4) from the extents of each arm.
4.  **Crop:** Remove any rows or columns on the edges of the grid that are entirely composed of white pixels (value 0).
"""

import numpy as np

def find_cross_center(grid):
    # Find the center pixel of the cross.
    yellow_pixels = np.argwhere(grid == 4)
    if len(yellow_pixels) == 0:
        return None

    # Calculate the centroid of yellow pixels
    center_y = int(np.round(np.mean(yellow_pixels[:, 0])))
    center_x = int(np.round(np.mean(yellow_pixels[:, 1])))

    # Verify it's a valid cross center (check for neighbors in four directions)
    # A very loose definition of a cross, but good enough for this challenge
    if (center_y > 0 and grid[center_y - 1, center_x] == 4) or \
       (center_y < grid.shape[0] - 1 and grid[center_y + 1, center_x] == 4) or\
       (center_x > 0 and grid[center_y, center_x - 1] == 4) or \
       (center_x < grid.shape[1] - 1 and grid[center_y, center_x + 1] == 4):
        return (center_y, center_x)
    return None

def extend_arms(grid, center):
    # Extend the arms of the cross to the edges of the grid.
    if center is None:
        return None
    
    center_y, center_x = center
    grid_height, grid_width = grid.shape
    
    # Create a new grid filled with yellow within the bounds, copy existing pixels
    extended_grid = np.zeros_like(grid)

    # Find the extents of the cross arms
    min_y, max_y = center_y, center_y
    min_x, max_x = center_x, center_x

    # Extend up
    for y in range(center_y, -1, -1):
        if grid[y, center_x] == 4:
           min_y = y
        else:
            break

    # Extend down
    for y in range(center_y, grid_height):
        if grid[y, center_x] == 4:
           max_y = y
        else:
            break

    # Extend left
    for x in range(center_x, -1, -1):
        if grid[center_y, x] == 4:
            min_x = x
        else:
            break

    # Extend right
    for x in range(center_x, grid_width):
        if grid[center_y, x] == 4:
            max_x = x
        else:
            break

    #fill extents with yellow
    extended_grid[min_y:max_y+1, min_x:max_x+1] = 4

    return extended_grid

def crop_grid(grid):
    # Crop empty (all zero) rows and cols
    rows_to_keep = np.any(grid != 0, axis=1)
    cols_to_keep = np.any(grid != 0, axis=0)
    cropped_grid = grid[rows_to_keep][:, cols_to_keep]
    return cropped_grid

def transform(input_grid):
    # Convert input grid to a NumPy array.
    input_grid = np.array(input_grid)

    # Find the center of the cross.
    cross_center = find_cross_center(input_grid)

    # Extend the arms of the cross.
    extended_grid = extend_arms(input_grid, cross_center)
    
    if extended_grid is None:
        return np.array([])

    # Crop the grid.
    output_grid = crop_grid(extended_grid)
    
    return output_grid