"""
The transformation involves identifying connected regions of color 3 (green) and 2 (red) in the input grid. 
A shape of color 8 with the same dimensions of all other shapes together is inserted, and then other shapes
are moved to the bottom of the newly created shape.
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


def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation

    # 1. Identify Objects
    objects = find_objects(input_grid, [2, 3])

    # 2. insert background
    bounding_box = get_bounding_box(objects)
    if bounding_box is not None:
        min_row, min_col, max_row, max_col = bounding_box
        output_grid = np.zeros((max_row - min_row+9 , max_col - min_col+1), dtype=int)
        # Fill bounding box area with 8
        for row in range(output_grid.shape[0]-8):
            for col in range(output_grid.shape[1]):
                output_grid[row,col] = 8
    else:
        output_grid = np.copy(input_grid)

    # 3. Move to bottom and stack
    if objects:
        # find dimensions of inserted shape
        insert_height = output_grid.shape[0]-8
        insert_width = output_grid.shape[1]

        current_row = insert_height
        for obj, color in reversed(objects): #reversed because of examples
            # compute original object height
            obj_rows = [r for r, _ in obj]
            obj_height = max(obj_rows) - min(obj_rows) + 1
            for r, c in obj:
                # adjust col based on bounding box
                new_c = c-min_col
                # copy pixel to bottom of output
                output_grid[current_row + (r-min(obj_rows)), new_c] = color
            current_row += obj_height

    return output_grid.tolist()
