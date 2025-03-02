"""
The transformation identifies the largest yellow "plus" shape in the input grid and reconstructs it in the output grid. The output grid has a size determined by the size of the plus: output_size = 2 * plus_size - 1. The background of the input is also the background of the output.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a dictionary of objects, keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
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
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects


def get_plus_extent(pixels):
    """Calculates a bounding box, assuming a plus shape"""
    min_row = min(p[0] for p in pixels)
    max_row = max(p[0] for p in pixels)
    min_col = min(p[1] for p in pixels)
    max_col = max(p[1] for p in pixels)
    return max_row - min_row + 1, max_col-min_col + 1

def transform(input_grid):
    # Find all objects in the grid
    objects = find_objects(input_grid)

    # Select the largest yellow plus shape (color 4)
    yellow_objects = objects.get(4)
    target_object = None

    #iterate to find largest plus
    for obj in yellow_objects:
        h, w = get_plus_extent(obj)
        if h == w and h % 2 == 1:
            if target_object is None or h > get_plus_extent(target_object)[0]:
                target_object = obj

    # Get extent of target object, h,w
    height, width = get_plus_extent(target_object)

    # Determine the output grid size and background color
    output_size = 2 * height - 1
    background_color = input_grid[0,0] #assume background is top-left pixel
    output_grid = np.full((output_size, output_size), background_color, dtype=int)

    # recreate the yellow plus in center of output
    center = output_size // 2

    for r_offset in range(-(height//2), height//2 + 1):
        output_grid[center+r_offset,center] = 4
    for c_offset in range(-(width//2), width//2 + 1):
        output_grid[center,center+c_offset] = 4
   

    return output_grid