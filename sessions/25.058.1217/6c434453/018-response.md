# 6c434453 • 018 • refine_coder

---
```python
"""
1.  **Identify Blue Objects:** Find all contiguous regions (objects) of blue (1) pixels in the input grid.

2.  **Group Objects:**
    *   **Group A:** The blue object with the most top-left corner belongs to Group A.
    *   **Group B:** All other blue objects belong to Group B.

3.  **Transform Objects:**
    *   **Group A:** Move the object one cell diagonally up and to the left, and change its color to red (2).
    *   **Group B:**
        *   If any objects within Group B are horizontally adjacent to each other, move *all* objects in Group B one cell diagonally down and to the right, and change their color to red (2).
        *   Otherwise (if no Group B objects are horizontally adjacent), move each object in Group B one cell down and one cell to the left, and change their color to red (2).

4.  **Clear original blue pixels** Clear all blue pixels from the input.

5.  **Output:** Create the output grid with the transformed objects, leaving other pixels from the input grid unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of the specified color in the grid."""
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

def find_top_left(obj):
    """Returns the top-left coordinate of an object."""
    return min(obj, key=lambda p: (p[0], p[1]))

def are_horizontally_adjacent(obj1, obj2):
    """Checks if two objects are horizontally adjacent."""
    for r1, c1 in obj1:
        for r2, c2 in obj2:
            if abs(r1 - r2) <= 1 and abs(c1 - c2) == 1:
                return True
    return False

def move_object(object_pixels, row_shift, col_shift, grid_shape):
    """Shifts the object pixels by the specified row and column offsets, handling bounds."""
    moved_pixels = []
    for row, col in object_pixels:
        new_row = row + row_shift
        new_col = col + col_shift
        if 0 <= new_row < grid_shape[0] and 0 <= new_col < grid_shape[1]:
            moved_pixels.append((new_row, new_col))
    return moved_pixels

def transform(input_grid):
    # Initialize output_grid with the same values as the input_grid
    output_grid = np.copy(input_grid)
    grid_shape = input_grid.shape

    # 1. Identify Objects
    blue_objects = find_objects(input_grid, 1)

    # 2. Group Objects
    if not blue_objects:
        return output_grid  # No blue objects to transform

    if len(blue_objects) == 1:
        group_a = blue_objects[0]
        group_b = []
    else:
        # Find top-left-most object for Group A
        top_left_coords = [find_top_left(obj) for obj in blue_objects]
        group_a_index = top_left_coords.index(min(top_left_coords))
        group_a = blue_objects[group_a_index]
        group_b = [obj for i, obj in enumerate(blue_objects) if i != group_a_index]

    # 3. Transform Objects
    #   - Group A
    moved_group_a = move_object(group_a, -1, -1, grid_shape)
    for row, col in moved_group_a:
        output_grid[row, col] = 2
    for row, col in group_a: # Clear original Group A pixels
        output_grid[row,col] = 0


    #   - Group B
    if len(group_b) > 0:
        horizontally_adjacent = False

        if len(group_b) > 1 :
            for i in range(len(group_b)):
                for j in range(i + 1, len(group_b)):
                    if are_horizontally_adjacent(group_b[i], group_b[j]):
                        horizontally_adjacent = True
                        break  # Optimization, any adjacency is enough
                if horizontally_adjacent:
                  break


        for obj in group_b:
            if horizontally_adjacent:
              moved_group_b = move_object(obj, 1, 1, grid_shape) # All to (1,1)
            else:
              moved_group_b = move_object(obj, 1, -1, grid_shape) # All to (1,-1)
            for row, col in moved_group_b:
                output_grid[row, col] = 2
            for row, col in obj: # Clear original Group B pixels
                output_grid[row,col] = 0

    return output_grid
```
