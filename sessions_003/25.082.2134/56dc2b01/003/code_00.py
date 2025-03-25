"""
The transformation involves identifying connected regions of color 2 (red) and 3 (green) in the input grid.
A rectangular region of color 8 (azure) is created, spanning the width of the combined bounding box of all identified objects.
The original objects are then stacked below the azure region, maintaining their relative horizontal positions, and are stacked
top-to-bottom as they appear in the original grid.
"""

import numpy as np

def find_objects(grid, colors):
    """
    Finds connected regions of specified colors in the grid.
    Returns a list of (object, color) tuples, where each object
    is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] in colors and (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((current_object, grid[row, col]))
    return objects

def get_bounding_box(objects):
    """
    compute the bounding box that contains all objects
    """
    if not objects:
        return None

    min_row = float('inf')
    min_col = float('inf')
    max_row = float('-inf')
    max_col = float('-inf')

    for obj, _ in objects:
      for row,col in obj:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)
    return (min_row, min_col, max_row, max_col)

def get_object_height(obj):
    """Calculates the height of an object."""
    rows = [r for r, _ in obj]
    return max(rows) - min(rows) + 1

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid, [2, 3])

    # 2. Determine Bounding Box for all objects
    bounding_box = get_bounding_box(objects)

    if bounding_box is None:
        return input_grid.tolist() # Return original if no objects of interest

    min_row_all, min_col_all, max_row_all, max_col_all = bounding_box
    azure_width = max_col_all - min_col_all + 1

    # find height of all objects
    total_objects_height = 0
    for obj, _ in objects:
        total_objects_height += get_object_height(obj)

    # top padding in example 3 is 3, so consider this
    top_padding = min_row_all
    
    # 3. Determine Output Grid height
    # use height of color 8 object + object stack + top padding
    output_height = top_padding + 1 + total_objects_height
    output_grid = np.zeros((output_height, azure_width), dtype=int)


    # 4. Create Azure region - height is one row
    azure_row_index = top_padding
    for col in range(azure_width):
        output_grid[azure_row_index, col] = 8

    # 5. stack objects, iterating in original order
    current_row = azure_row_index + 1

    for obj, color in objects: # iterate in original order
        obj_height = get_object_height(obj)
        min_row_obj = min([r for r,_ in obj]) # get original object offset
        for r, c in obj:
            # adjust col based on bounding box
            new_c = c - min_col_all
            # place pixel into stacked output
            output_grid[current_row + (r - min_row_obj) , new_c] = color
        current_row += obj_height
    return output_grid.tolist()