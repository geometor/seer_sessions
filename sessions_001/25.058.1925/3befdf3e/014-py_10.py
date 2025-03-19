"""
1.  **Identify** the largest red square (color 2) in the input grid.
2.  **Identify** the single orange pixel (color 7) within the red square.
3.  **Maintain or Expand** the red square.
   - If expanding, The red square expands so the orange object is horizontally centered inside the red square.
4.  **Modify** the orange pixel: Create a horizontal sequence of pixels: orange, red, orange ([7, 2, 7]). This replaces the original single orange pixel.
5.  **Combine:** The (potentially expanded) red square and the modified orange sequence maintains the relative positions from the input.
6. **Preserve Background:** Pixels not part of the original red square or the original orange pixel remain unchanged (copied from input).
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Handle cases with no object of given color
    # Calculate the bounding box
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    return min_row, max_row, min_col, max_col

def modify_orange_pixel(grid, row, col):
    # modify the orange pixel to horizontal [7,2,7]
    modified_grid = grid.copy()

    modified_grid[row, col -1] = 7
    modified_grid[row, col] = 2
    modified_grid[row, col + 1] = 7

    return modified_grid

def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find the red square
    red_min_row, red_max_row, red_min_col, red_max_col = find_object(input_grid, 2)

    if red_min_row is None:
        return output_grid

    # Find the orange square
    orange_min_row, orange_max_row, orange_min_col, orange_max_col = find_object(input_grid, 7)

    if orange_min_row is None:
      return output_grid
    
    # calculate width of red square
    red_width = red_max_col - red_min_col + 1

    # expand red square, centering orange pixel
    new_red_min_col = orange_min_col - 1
    new_red_max_col = orange_min_col + 1
    new_red_min_row = red_min_row

    if new_red_max_col - new_red_min_col + 1 > red_width:
      # expand top
      output_grid[red_min_row - 1, new_red_min_col:new_red_max_col + 1] = 2
      new_red_min_row -=1

    # set all red square
    output_grid[new_red_min_row:red_max_row + 1, new_red_min_col:new_red_max_col + 1] = 2

    # modify orange object, relative to original position
    output_grid = modify_orange_pixel(output_grid, orange_min_row , orange_min_col)

    return output_grid