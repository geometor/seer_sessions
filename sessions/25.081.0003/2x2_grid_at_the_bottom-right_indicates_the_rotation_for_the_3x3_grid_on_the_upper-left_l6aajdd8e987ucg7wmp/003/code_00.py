"""
1.  **Identify Objects:** Find all contiguous blocks (objects) of green (color 3), blue (color 1), and yellow (color 4) pixels.
2.  **Green Object Transformation:**
    *   Identify all separate green objects.
    *   Place the first identified green object at the top-left corner (0,0). If it has more than one pixel arrange as a horizontal line.
    *   Place second identified object at (x,y) = (0,1). If it has more than one pixel arrange as a horizontal line.
    *    Place third and further objects vertically.
3.  **Blue and Yellow Object Removal:** Remove all blue (color 1) and yellow (color 4) objects from the grid.
4.  **Output:** The final grid should only contain the transformed green objects, with all other cells set to black (color 0). The overall grid dimensions remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    input_grid_copy = np.copy(input_grid)

    # Find object-3 (green)
    object_3_list = find_objects(input_grid_copy, 3)

    # Green Object Transformation
    row_index = 0
    col_index = 0
    for i, obj in enumerate(object_3_list):
        if i == 0: # First object, place at top-left
            for j, (r, c) in enumerate(obj):
              output_grid[0, j] = 3
            row_index = 1

        elif i == 1:
            for j, (r,c) in enumerate(obj):
              output_grid[row_index,j] = 3

        else:
            for j,(r,c) in enumerate(obj):
                output_grid[row_index,0] = 3
                row_index += 1

    # Find object-1 (blue) and object-4 (yellow) - for removal
    object_1_list = find_objects(input_grid_copy, 1)
    object_4_list = find_objects(input_grid_copy, 4)

    # Remove blue and yellow objects
    for obj in object_1_list:
        for r, c in obj:
            input_grid_copy[r, c] = 0  # Set to background (0)

    for obj in object_4_list:
        for r, c in obj:
            input_grid_copy[r, c] = 0  # Set to background (0)


    return output_grid