"""
1. Identify the Blue Object: Find the largest contiguous block of blue (color 1) pixels in the input grid.
2. Determine Bounding Box: Calculate the bounding box of this blue object (min_row, max_row, min_col, max_col).
3. Extract Subgrid: Create a new grid that is a subgrid of the original input grid, defined by the blue object's bounding box.
4. Return the extracted subgrid.
"""

import numpy as np

def find_blue_object(grid):
    """
    Finds the bounding box of the largest contiguous blue (color 1) object.
    """
    grid_array = np.array(grid)
    height, width = grid_array.shape
    visited = np.zeros((height, width), dtype=bool)
    blue_objects = []

    def is_valid(row, col):
        return 0 <= row < height and 0 <= col < width

    def dfs(row, col, current_object):
        if not is_valid(row, col) or visited[row, col] or grid_array[row, col] != 1:
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(height):
        for c in range(width):
            if not visited[r, c] and grid_array[r, c] == 1:
                current_object = []
                dfs(r, c, current_object)
                blue_objects.append(current_object)

    if not blue_objects:
        return None  # No blue object found

    # Find the largest blue object
    largest_object = max(blue_objects, key=len)

    # Calculate bounding box
    min_row = min(p[0] for p in largest_object)
    max_row = max(p[0] for p in largest_object)
    min_col = min(p[1] for p in largest_object)
    max_col = max(p[1] for p in largest_object)

    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Extracts the subgrid corresponding to the bounding box of the largest blue object.
    """
    # Find the bounding box of the blue object
    bounding_box = find_blue_object(input_grid)

    if bounding_box is None:
        return [] # Return empty grid if no blue object

    min_row, max_row, min_col, max_col = bounding_box

    # Extract the subgrid
    input_grid_np = np.array(input_grid)
    output_grid = input_grid_np[min_row:max_row+1, min_col:max_col+1].tolist()

    return output_grid