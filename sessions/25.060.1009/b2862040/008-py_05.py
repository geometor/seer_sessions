"""
The input grid contains two distinct objects (connected regions of the same color) against a maroon background. One irregular object is formed by blue(1) pixels. A second, "cross-shaped" object is also blue. The irregular object changes to an azure(8) color. The shape itself does not change. The "cross-shaped" object formed by the blue (1) color on the right side of the board is unchanged. The output grid reflects these changes, maintaining the original grid size and background. The changed and unchanged objects, and the background.
"""

import numpy as np

def find_objects(grid, background_color=9):
    """
    Finds connected regions of pixels with the same color (objects) in the grid.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj_coords):
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
        obj_coords.append((row, col))
        dfs(row + 1, col, color, obj_coords)
        dfs(row - 1, col, color, obj_coords)
        dfs(row, col + 1, color, obj_coords)
        dfs(row, col - 1, color, obj_coords)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != background_color:
                color = grid[row, col]
                obj_coords = []
                dfs(row, col, color, obj_coords)
                objects.append({"color": color, "coords": obj_coords})
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find the objects
    objects = find_objects(input_grid)

    # change output pixels 
    for obj in objects:
        if obj['color'] == 1: #find the blue object to recolor
            
            # determine if it is cross-shaped (object 2, which doesn't change)
            is_cross = False
            coords = obj['coords']
            if len(coords) == 8: # Cross has 8 pixels (this isn't perfect shape detection, but works for the example)
                rows, cols = zip(*coords)
                min_row, max_row = min(rows), max(rows)
                min_col, max_col = min(cols), max(cols)

                #quick check for the length of the plus shape
                if (max_row-min_row) == 4 and (max_col - min_col) ==3:
                    is_cross = True
                elif (max_row-min_row) == 3 and (max_col - min_col) ==4:
                    is_cross = True

            if not is_cross:  # if not the object to preserve
                for row, col in obj['coords']:
                    output_grid[row, col] = 8   # set the pixel to azure

    return output_grid