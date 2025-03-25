"""
The transformation rule involves identifying non-blue objects within the input grid. The objects are vertically mirrored. If a 2x2 red block is present, objects below it are mirrored to positions directly above it, preserving relative positioning and overwriting cells if objects overlap. If no red block is present all of the objects are mirrored. When multiple objects are mirrored their relative vertical order and shape is preserved.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 1:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((grid[row, col], current_object))  # Store color and object
    return objects

def find_lowest_red_block(grid):
    """Finds the lowest 2x2 red block's top-left coordinates."""
    for r in range(grid.shape[0] - 1, -1, -1):
        for c in range(grid.shape[1] - 1):
            if (grid[r, c] == 2 and grid[r + 1, c] == 2 and
                grid[r, c + 1] == 2 and grid[r + 1, c + 1] == 2):
                return r, c
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the mirroring rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    output_grid[:] = 1  # Initialize with blue (1)

    objects = find_objects(input_grid)
    red_block_coords = find_lowest_red_block(input_grid)

    if red_block_coords is not None:
        red_row, red_col = red_block_coords
        # Sort objects by their minimum row, so lower objects get priority in the output.
        objects.sort(key=lambda x: min(r for r, _ in x[1]))

        for color, obj in objects:
            min_row = min(r for r, _ in obj)
            max_row = max(r for r, _ in obj)
            
            if max_row >= red_row:
                # Mirror objects that are at or below the red block
                for r, c in obj:
                    dist_to_red = r - red_row
                    new_row = red_row - dist_to_red -1 #shift objects above block

                    if new_row >= 0:
                         output_grid[new_row, c] = color  # Mirrored position
                    
            else:
                #copy all objects that are above the red block - no mirroring
                for r,c in obj:
                    output_grid[r,c] = color

    else:
        # No red block: Mirror all objects relative to grid's vertical center.

        #find the center of all objects to mirror around
        object_rows = []
        for color, obj in objects:
            for r, _ in obj:
                object_rows.append(r)

        if len(object_rows) > 0:
           min_row = min(object_rows)
           max_row = max(object_rows)

           center_row = (min_row + max_row) / 2

        else:
            return input_grid.tolist()

        # Sort objects by lowest y coordinate.
        objects_sorted = sorted(objects, key=lambda item: min(row for row, _ in item[1]))
        
        for color, obj in objects_sorted:
            for r, c in obj:
                
                dist_to_center = r - center_row
                new_row = int(round(center_row - dist_to_center))
                if 0 <= new_row < output_grid.shape[0]:
                     output_grid[new_row, c] = color

    return output_grid.tolist()