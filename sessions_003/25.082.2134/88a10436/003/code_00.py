"""
1. **Identify Objects:** Find all distinct objects in the input grid. An object is a contiguous block of non-zero pixels.
2. **Individual Bounding Boxes:** For *each* object, determine its bounding box (the smallest rectangle enclosing that object).
3. **Mirror Each Object:** For *each* object:
    *   Calculate the center point (midpoint of rows and columns) of its bounding box.
    *   Mirror each pixel of the object across both the horizontal and vertical centerlines of *its* bounding box.
    *   Create a new object at the mirrored position, keeping the original colors.
    * remove the original object
4.  **Construct Output:** The output grid initially starts as a copy of the input grid. Then for each object, remove the original and replace with mirrored pixels. The background (pixels with value 0) remains unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.  An object is a group of
    contiguous non-zero pixels.
    Uses depth first search
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] == 0):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def bounding_box(object_pixels):
    """
    Find the smallest rectangle enclosing a single object.
    """
    min_row = float('inf')
    max_row = float('-inf')
    min_col = float('inf')
    max_col = float('-inf')

    for row, col in object_pixels:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    return (min_row, max_row, min_col, max_col)

def mirror_position(point, min_row, max_row, min_col, max_col):
    """
    Mirror a point within the object's bounding box
    """
    center_row = (min_row + max_row) / 2
    center_col = (min_col + max_col) / 2
    mirrored_row = int(2 * center_row - point[0])
    mirrored_col = int(2 * center_col - point[1])
    return (mirrored_row, mirrored_col)

def transform(input_grid):
    """
    Transforms the input grid according to the mirroring rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Iterate through each object
    for obj in objects:
        # Find the bounding box for the current object
        min_row, max_row, min_col, max_col = bounding_box(obj)

        # remove original object
        for r, c in obj:
          output_grid[r,c] = 0

        # Mirror each pixel of the object within its bounding box
        for row, col in obj:
            mirrored_row, mirrored_col = mirror_position(
                (row, col), min_row, max_row, min_col, max_col
            )
            # Check if the mirrored position is within the grid boundaries
            if 0 <= mirrored_row < output_grid.shape[0] and 0 <= mirrored_col < output_grid.shape[1]:
                output_grid[mirrored_row, mirrored_col] = input_grid[row, col]

    return output_grid.tolist()