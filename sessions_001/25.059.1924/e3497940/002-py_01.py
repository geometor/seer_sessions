"""
The transformation removes a vertical grey line (value 5) from the input grid. 
It then retains the colored objects (contiguous non-grey, non-white pixels) present on either side of the line.
The output grid has fewer columns, and the relative positions of colored objects from the input are lost;
only their shape and colors, are preserved. The grey line is completely removed.
"""

import numpy as np

def find_vertical_line(grid):
    # Find the vertical line of grey (5) pixels.
    for j in range(grid.shape[1]):
        if all(grid[:, j] == 5):
            return j
    return -1  # Should not happen, based on problem definition

def get_objects(grid, exclude_colors=[0,5]):
    # Get contiguous colored objects, excluding specified colors
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(i, j, color, obj_coords):
      # recursive depth first search to mark contiguous colors
        if (
            i < 0
            or i >= grid.shape[0]
            or j < 0
            or j >= grid.shape[1]
            or visited[i, j]
            or grid[i, j] != color
        ):
            return
        visited[i, j] = True
        obj_coords.append((i, j))
        dfs(i + 1, j, color, obj_coords)
        dfs(i - 1, j, color, obj_coords)
        dfs(i, j + 1, color, obj_coords)
        dfs(i, j - 1, color, obj_coords)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i, j] not in exclude_colors:
                color = grid[i, j]
                obj_coords = []
                dfs(i, j, color, obj_coords)
                objects.append((color, obj_coords))
    return objects

def transform(input_grid):
    # Find the index of the vertical grey line
    grey_line_index = find_vertical_line(input_grid)

    # Get all objects, excluding white and grey
    objects = get_objects(input_grid)

    # Calculate the output grid size. The new width will exclude grey line column
    output_width = input_grid.shape[1] - 1
    output_height = input_grid.shape[0]
   
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy the objects to the output grid. Adjust column indices based on grey line removal
    for color, obj_coords in objects:
        for i, j in obj_coords:
            new_j = j if j < grey_line_index else j - 1 # copy index if left of grey, reduce index by 1 if right of grey
            output_grid[i, new_j] = color
    
    return output_grid