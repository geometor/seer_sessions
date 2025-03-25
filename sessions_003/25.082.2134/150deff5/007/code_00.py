"""
1.  **Identify Gray Objects:** Locate all distinct, contiguous regions (objects) of gray (color 5) pixels within the input grid.
2.  **Border Replacement:** For each identified gray object:
    *   Find the border pixels. A border pixel is any gray pixel that has at least one immediate neighbor (up, down, left, or right) that is *not* a gray pixel.
    *   Replace all border pixels of the gray object with azure (color 8).
3. **Midline Replacement:** For each identified gray object:
    * find the vertical center:
      * Find the minimum and maximum column indices occupied by gray pixels within the object.
      * Calculate the midline column index: `mid_col = (min_col + max_col) // 2`.
      * replace pixels on the vertical center with red (color 2)
        * If there are gray pixels in the object at that `mid_col` index, and if there are an *odd* number of columns in the object:
          * Replace all gray pixels within the object that fall on the midline column (`mid_col`) with red (color 2).
        * If there are an even number of columns:
           * replace *all* gray pixels in columns `mid_col` AND `mid_col + 1`
4.  **Output:** Create a new output grid, initially a copy of the input grid. Apply the border and midline replacements to this new grid. Pixels that were not gray in the input grid remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Find contiguous objects of a given color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        """Depth-first search to find contiguous pixels."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_object_border(object_pixels, grid_shape):
    """Get the border pixels of an object."""
    border_pixels = []
    for r, c in object_pixels:
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        for nr, nc in neighbors:
            if (nr < 0 or nr >= grid_shape[0] or nc < 0 or nc >= grid_shape[1] or (nr, nc) not in object_pixels):
                border_pixels.append((r,c))
                break #pixel is a border if one neighbor isn't the right color
    return list(set(border_pixels))  # Remove duplicates


def get_vertical_midline_pixels(object_pixels):
    """Get all pixels on the vertical midline of an object."""
    cols = [c for r, c in object_pixels]
    min_col = min(cols)
    max_col = max(cols)
    mid_col = (min_col + max_col) // 2
    width = max_col - min_col + 1
    if width % 2 == 1:
      return [(r, c) for r, c in object_pixels if c == mid_col]
    else:
      return [(r,c) for r, c in object_pixels if c == mid_col or c == mid_col + 1]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # find grey objects
    gray_objects = find_objects(input_grid, 5)

    # replace gray pixels at object borders with azure
    for obj in gray_objects:
        border = get_object_border(obj, grid_shape)
        for r, c in border:
            output_grid[r, c] = 8
    
    # replace gray pixels at vertical middle with red
    for obj in gray_objects:
        middle_pixels = get_vertical_midline_pixels(obj)
        for r, c in middle_pixels:
            output_grid[r, c] = 2
    
    return output_grid