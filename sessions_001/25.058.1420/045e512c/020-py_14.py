"""
1.  **Identify Objects:** Find all contiguous blocks of non-zero pixels. Each block is an object, and we note its color.
2.  **Gray Object Rule:** Objects composed of gray (5) pixels remain unchanged.
3. **Azure Object Rule:**
    *   Locate objects of azure (1) pixels.
    *   For each azure object, create a new object of the same color by extending each pixel of the base object down and to the right by one pixel.
4.  **Magenta Object Rule:**
      * Locate objects of magenta (6) pixels.
      * For each magenta object, create a new object by extending each pixel of the base object by one pixel down and to the left.
5. **Combine:** Combine new objects with any unchanged objects.
6.  **Output:** The output grid consists of the combined objects and background (0).
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1),(r+1,c+1),(r-1,c-1),(r+1,c-1),(r-1,c+1)]
        for nr, nc in neighbors:
            dfs(nr, nc, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append((grid[r,c],current_object)) #store the color and object
    return objects

def extend_object(object_pixels, color, direction):
    """
    Extends the object in the specified direction.

    Args:
      object_pixels: List of (row, col) tuples representing the object.
      color:  Color of the object.
      direction: tuple (row_offset, col_offset)

    Returns
      list of extended objects
    """
    extended_object = []

    row_offset, col_offset = direction

    for r, c in object_pixels:
        extended_object.append((r + row_offset, c + col_offset))

    return [(color, extended_object)]

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # change output pixels based on rules
    for color, object_pixels in objects:
        if color == 5: #gray
            continue #do nothing
        elif color == 1:  #azure
            extended_objects = extend_object(object_pixels, color, (1,1)) #down-right

            # Add extended object to the output
            for ext_color, ext_pixels in extended_objects:
               for r, c in ext_pixels:
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = ext_color
        elif color == 6:  #magenta
            extended_objects = extend_object(object_pixels, color, (1,-1)) #down-left

            # Add extended object to the output
            for ext_color, ext_pixels in extended_objects:
               for r, c in ext_pixels:
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                      output_grid[r,c] = ext_color

    return output_grid