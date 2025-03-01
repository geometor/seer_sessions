"""
1.  **Identify the Target Object:** Find the largest contiguous vertical line of pixels of the same color in the input grid. A vertical line is defined as an object where the height is greater than 1 and the width is exactly 1.
2. **Determine Bounding Box:** Get the bounding box of that vertical line of pixels. The bounding box consists of the starting row, starting column, ending row, and ending column of the object.
3.  **Create the Output Grid:** Create a new grid that is a subgrid of the original input grid defined by the bounding box of the target object. The output grid is created by cropping input grid to the target object bounds.
"""

import numpy as np

def get_objects(grid):
    """
    Identify contiguous blocks of the same color as objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj:
                    objects.append(obj)
    return objects

def get_bounding_box(obj):
    """
    Calculates the bounding box of a given object.
    """
    rows = [r for r, _ in obj]
    cols = [c for _, c in obj]
    return min(rows), min(cols), max(rows), max(cols)

def is_vertical_line(obj):
    """
    Checks if an object is a vertical line (height > 1, width == 1).
    """
    if not obj:
        return False
    row_start, col_start, row_end, col_end = get_bounding_box(obj)
    height = row_end - row_start + 1
    width = col_end - col_start + 1
    return height > 1 and width == 1

def transform(input_grid):
    """
    Transforms the input grid by identifying a vertical line and extracting it.
    """
    # Find objects in the input grid
    objects = get_objects(input_grid)

    # Find the target object (largest vertical line)
    target_object = None
    for obj in objects:
        if is_vertical_line(obj):
          if target_object is None:
            target_object = obj
          else:
            #compare height
            if len(obj) > len(target_object):
              target_object = obj

    # If no vertical line is found, return an empty grid (or a default value,
    # based on task constraints)
    if target_object is None:
        return np.zeros((0, 0), dtype=int)  # Or any other appropriate default

    # Get the bounding box of the target object
    row_start, col_start, row_end, col_end = get_bounding_box(target_object)

    # Create the output grid by cropping the input grid
    output_grid = input_grid[row_start:row_end+1, col_start:col_end+1]

    return output_grid