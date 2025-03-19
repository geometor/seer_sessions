"""
1.  **Identify Objects:** Locate all connected regions (objects) of non-background colored pixels within the input grid. The background appears to be the color filling the perimeter.
2.  **Check for a object at the bottom:** Check for the presence of an object on the penultimate row from the bottom (row index `height - 2`).
3.  **Conditional Row Deletion:** If an object is found with its bottom edge on row index `height - 2`
    then do not transform and return the input grid
    otherwise
    if an object is found with its bottom edge *not* on row index `height - 2`, then delete the row immediately below the bottom edge of this object.
"""

import numpy as np

def find_objects(grid):
    """Finds connected components of non-background pixels."""
    background_color = grid[0, 0]
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] == background_color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)  # Diagonal
        dfs(row - 1, col - 1, current_object)  # Diagonal
        dfs(row + 1, col - 1, current_object)
        dfs(row -1, col + 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != background_color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_object_bottom(object_pixels):
    """Returns the bottom-most row index of an object."""
    return max(row for row, _ in object_pixels)

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Get grid height
    height = input_grid.shape[0]

    # Check condition for row deletion
    delete_row = False
    row_to_delete = -1

    for obj in objects:
        bottom_row = get_object_bottom(obj)
        if bottom_row != height - 2:
            delete_row = True
            row_to_delete = bottom_row + 1
            break  # only need to find one

    # Perform transformation based on the condition
    if not delete_row:
        return input_grid
    else:
        # Delete the specified row
        output_grid = np.delete(input_grid, row_to_delete, axis=0)
        return output_grid