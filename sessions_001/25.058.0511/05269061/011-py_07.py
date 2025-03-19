"""
The transformation rule is to change the color of a single-pixel object from blue (1) to red (2) if present, and from red (2) to blue (1) if present. If there are multiple single-pixel objects, change only the object located at the lowest row and, if in the same row, the most righ column.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous regions of the same color and labels them as objects.
    Returns a dictionary of objects, keyed by object ID, with properties.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    object_id_counter = 1

    def dfs(row, col, color, object_id):
        """Depth-first search to find contiguous regions."""
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
        objects[object_id]["pixels"].append((row, col))
        dfs(row + 1, col, color, object_id)
        dfs(row - 1, col, color, object_id)
        dfs(row, col + 1, color, object_id)
        dfs(row, col - 1, color, object_id)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                objects[object_id_counter] = {
                    "color": color,
                    "pixels": [],
                }
                dfs(row, col, color, object_id_counter)
                object_id_counter += 1
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    input_objects = find_objects(input_grid)
    
    # Find single pixel objects
    single_pixel_objects = []
    for obj_id, obj_data in input_objects.items():
        if obj_data["color"] == 1 and len(obj_data["pixels"]) == 1:
            single_pixel_objects.append((obj_data["pixels"][0], 1))  # Store position and original color (blue)
        elif obj_data["color"] == 2 and len(obj_data["pixels"]) == 1:
            single_pixel_objects.append((obj_data["pixels"][0], 2)) # Store position and the original color(red)

    # If single-pixel objects exist, change the color of the last one
    if single_pixel_objects:
        single_pixel_objects.sort() #sort by row and then by col
        target_pixel, original_color = single_pixel_objects[-1]
        row, col = target_pixel
        
        # Change color based on the original color
        if original_color == 1: #blue
             output_grid[row, col] = 2  # Change blue (1) to red (2)
        elif original_color == 2:
             output_grid[row,col] = 1

    return output_grid