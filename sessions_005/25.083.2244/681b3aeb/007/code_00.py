"""
1.  **Identify Objects:** Find all contiguous blocks of non-zero pixels in the input grid. Each block represents an object. Record the shape, color, size, and relative position of each object.

2.  **Order Objects and Rotate:** The objects found in the input are re-arranged to form a 3x3 grid for the output.
    - find cross shape - it always becomes the top row
    - find vertical bar - it always becomes the left most column
    - find L shape - place remaining pixels

3. **Z Order:** objects are ordered in the output by placing the top row first, then the left column, then any additional objects.

4.  **Output Grid:** The output grid is always 3x3, if there are not enough pixels, they will be arranged at the top left, if there are too many, some may be discarded.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies contiguous blocks of non-zero pixels as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj_pixels = []
                dfs(row, col, grid[row, col], obj_pixels)
                objects.append(obj_pixels)
    return objects

def get_object_shape(grid, obj_pixels):
    rows, cols = zip(*obj_pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    shape = []
    for r in range(min_row, max_row + 1):
        row_shape = []
        for c in range(min_col, max_col + 1):
            if (r, c) in obj_pixels:
                row_shape.append(grid[r,c])
            else:
                row_shape.append(0)
        shape.append(row_shape)

    return np.array(shape)


def is_cross_shape(obj_pixels, grid):
    if len(obj_pixels) != 5:
      return False

    # get the object and shape
    obj = get_object_shape(grid, obj_pixels)

    # check if it's a cross shape, either horizontal or vertical
    return (np.array_equal(obj, [[0,1,0],[1,1,1],[0,1,0]]) or
            np.array_equal(obj, [[1,0,0],[1,1,1]]) or
            np.array_equal(obj, [[0,0,1],[1,1,1]]) or
            np.array_equal(obj, [[1,1,1],[0,0,1]]) or
            np.array_equal(obj, [[1,1,1],[1,0,0]]))

def is_vertical_bar_shape(obj_pixels, grid):

    # get the shape
    obj = get_object_shape(grid, obj_pixels)

    if len(obj_pixels) < 2:
        return False

    # Check if it's a vertical bar of any length
    rows, cols = obj.shape
    if cols == 1 and rows > 1:
        return True

    # check for slight curve by comparing with a 2x2 square - all bits must be set
    if rows == 2 and cols == 2:
      return np.array_equal(obj,[[1,1],[1,1]])

    return False;

def is_l_shape(obj_pixels, grid):

    if len(obj_pixels) < 3:
        return False

    # get the shape
    obj = get_object_shape(grid, obj_pixels)

    rows, cols = obj.shape

    # 2x3, 3x2 cases
    if (rows == 2 and cols == 3) or (rows == 3 and cols == 2):
        if np.count_nonzero(obj) < 6:
          return True

    # additional sizes
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # find objects
    objects = find_objects(input_grid)

    # find cross, vertical bar, and L-shapes
    cross_object = None
    vertical_bar_object = None
    l_shape_object = None

    for obj_pixels in objects:
        if is_cross_shape(obj_pixels, input_grid):
            cross_object = obj_pixels
        elif is_vertical_bar_shape(obj_pixels, input_grid):
            vertical_bar_object = obj_pixels
        elif is_l_shape(obj_pixels, input_grid):
            l_shape_object = obj_pixels


    # Place cross object (top row)
    if cross_object:
        color = input_grid[cross_object[0]]
        output_grid[0,:] = color


    # Place vertical bar object (left column)
    if vertical_bar_object:
      color = input_grid[vertical_bar_object[0]]
      output_grid[:,0] = color

    # place remaining object
    if l_shape_object:
      for r, c in l_shape_object:
        obj_shape = get_object_shape(input_grid, l_shape_object)
        # find location in local object
        min_row = min([row for row, _ in l_shape_object])
        min_col = min([col for _, col in l_shape_object])
        local_r = r - min_row
        local_c = c - min_col

        # skip if we can't place it
        if local_r >= 3 or local_c >= 3:
          continue

        # only set if not already set
        if output_grid[local_r, local_c] == 0:
          output_grid[local_r, local_c] = input_grid[r,c]

    return output_grid