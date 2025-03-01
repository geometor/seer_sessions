"""
The transformation rule extends an azure shape to the right edge of the grid if a green object is present in the same row and the green object touches the right edge. The extension happens only on rows where both an azure pixel and a right-edge-touching green pixel exist.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def object_touches_right_edge(grid, obj):
    """Checks if an object touches the right edge of the grid."""
    _, cols = grid.shape
    for _, c in obj:
        if c == cols - 1:
            return True
    return False

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure objects
    azure_objects = find_objects(input_grid, 8)
    
    # Find green objects
    green_objects = find_objects(input_grid, 3)

    # Find right-edge-touching green objects
    right_edge_green_objects = [obj for obj in green_objects if object_touches_right_edge(input_grid, obj)]


    # Iterate through each row
    for row_index in range(rows):
        # Check for presence of azure and right-edge-touching green in the current row
        row_has_azure = any(r == row_index for azure_obj in azure_objects for r, _ in azure_obj)
        row_has_right_green = any(r == row_index for green_obj in right_edge_green_objects for r, _ in green_obj )
        
        if row_has_azure and row_has_right_green:
            #get the azure objects in the current row
            azure_objects_in_row = [obj for obj in azure_objects if any(r == row_index for r,_ in obj)]
            for azure_obj in azure_objects_in_row:
                # Find the rightmost azure pixel in the current row within the current azure object
                rightmost_col = max(c for r, c in azure_obj if r == row_index)

                # Extend azure to the right edge in the current row
                for col_index in range(rightmost_col + 1, cols):
                    output_grid[row_index, col_index] = 8

    return output_grid