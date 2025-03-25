"""
1.  **Object Identification:** Identify all distinct objects within the input grid. An object is defined as a contiguous group of pixels sharing the same non-zero color. Determine the bounding box (the smallest rectangle encompassing the object) for each identified object.

2.  **Object Sorting:** Sort the identified objects based on their position. The primary sorting criterion is the rightmost column of their bounding box, in descending order (objects further to the right are processed first). If objects share the same rightmost column, the secondary sorting criterion is the bottom-most row of their bounding box, also in descending order (lower objects are processed first).

3.  **Output Grid Initialization:** Create a 3x3 output grid filled entirely with zeros.

4.  **Sequential Output Filling:** Iterate through the sorted list of objects. For each object, retrieve its color. Fill the cells of the output grid sequentially with this color. Start at the top-left cell (0, 0) and proceed from left to right. Once a row is complete, move to the next row, starting from the leftmost cell.  Continue this process, overwriting any previously filled cells, until all cells in the output grid are filled, or you complete filling with all object colors.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_coords):
        """Depth-first search to find contiguous pixels."""
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                obj_coords = []
                dfs(r, c, grid[r, c], obj_coords)
                # Calculate bounding box
                min_row = min(obj_coords, key=lambda item: item[0])[0]
                max_row = max(obj_coords, key=lambda item: item[0])[0]
                min_col = min(obj_coords, key=lambda item: item[1])[1]
                max_col = max(obj_coords, key=lambda item: item[1])[1]

                objects.append({
                    'color': grid[r, c],
                    'bounding_box': [[min_row, min_col], [max_row, max_col]]
                })
    return objects

def sort_objects(objects):
    """Sorts objects by rightmost column, then bottom-most row."""
    return sorted(objects, key=lambda obj: (obj['bounding_box'][1][1], obj['bounding_box'][1][0]), reverse=True)

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Sort the objects
    sorted_objects = sort_objects(objects)

    # Initialize a 3x3 output grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Fill the output grid sequentially
    row, col = 0, 0
    for obj in sorted_objects:
        output_grid[row, col] = obj['color']
        col += 1
        if col == 3:
            col = 0
            row += 1
        if row == 3:
            break

    return output_grid