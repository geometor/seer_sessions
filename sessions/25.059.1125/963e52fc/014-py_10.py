"""
1.  **Identify Objects:** Find all contiguous regions (objects) of non-white pixels in the input grid. A contiguous region is defined as a set of pixels of the same color that are directly adjacent (up, down, left, or right, but *not* diagonally).
2.  **Duplicate Objects:** For each identified object, duplicate it to the right. The duplicated object should be placed immediately to the right of the original object's bounding box, maintaining the original object's shape and color. The horizontal distance between the rightmost pixel in original and leftmost pixel of the copy will be equal to the width of the input.
"""

import numpy as np

def find_contiguous_objects(grid):
    """
    Identifies contiguous objects (blocks of same-colored, non-white pixels).

    Args:
        grid: The input grid.

    Returns:
        A list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(object_coords):
    """
    Calculates the bounding box of an object.

    Args:
        object_coords: List of (row, col) coordinates of the object.

    Returns:
         min_row, max_row, min_col, max_col
    """

    min_row = min(r for r, c in object_coords)
    max_row = max(r for r, c in object_coords)
    min_col = min(c for r, c in object_coords)
    max_col = max(c for r, c in object_coords)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid: double the width, keep height the same
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Find contiguous objects
    objects = find_contiguous_objects(input_grid)

    # Duplicate each object to the right
    for obj in objects:
        # find the bounding box
        min_row, max_row, min_col, max_col = get_bounding_box(obj)

        # calculate offset
        offset = input_grid.shape[1]

        # copy pixels to the output grid
        for row, col in obj:
            output_grid[row, col + offset] = input_grid[row, col]
            output_grid[row,col] = input_grid[row,col] # also set in original position

    return output_grid