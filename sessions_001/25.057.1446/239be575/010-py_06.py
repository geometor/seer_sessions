"""
Identifies all objects in the input grid, scales them down by a factor, and places them in the output grid, maintaining their relative positions.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
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
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:  # Ensure object is not empty
                  objects.append(current_object)
    return objects

def scale_object(obj, scale_factor):
    """
    Scales down an object by a given factor.  Averages positions to determine
    new pixel locations.  This is a very rough approximation of scaling and
    will likely need refinement.
    """
    if not obj:
        return []

    # Calculate the centroid of the original object.
    centroid_row = sum(p[0] for p in obj) / len(obj)
    centroid_col = sum(p[1] for p in obj) / len(obj)

    scaled_object = []
    # very simple approximation - we're just dividing row and column
    # coordinates by the scale factor.  This works poorly for non-square
    # objects.  We're calculating the *projected* scaled points here,
    # but we're not filling in any gaps.
    
    for row, col in obj:
        new_row = int((row - centroid_row) / scale_factor + centroid_row)
        new_col = int((col - centroid_col) / scale_factor + centroid_col)
        scaled_object.append((new_row,new_col))

    # remove duplicates
    scaled_object = list(set(scaled_object))

    return scaled_object



def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects
    objects = get_objects(input_grid)

    # Scale factor
    scale_factor = 3  #  empirical guess based on examples

    # Scale objects
    scaled_objects = []
    for obj in objects:
      scaled_objects.append((obj[0],scale_object(obj, scale_factor)))

    # change output pixels
    for _, scaled_obj in scaled_objects:
        color = input_grid[scaled_obj[0][0], scaled_obj[0][1]] # get the color from input grid
        for row, col in scaled_obj:
          if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
            output_grid[row, col] = color # assign color to scaled obj

    return output_grid