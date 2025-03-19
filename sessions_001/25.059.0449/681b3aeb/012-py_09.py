"""
Identify all contiguous regions (objects) of non-black pixels within the input grid. If the bounding box containing all objects has the same dimensions as the input grid, the output is identical to the input. Otherwise, create a new grid with dimensions based on the bounding box of all objects. Copy all objects from the input grid to the new grid, maintaining the relative positions of the objects, and translate the objects to the top-left of the output grid.
"""

import numpy as np

def find_objects(grid):
    # Find all contiguous regions of non-zero color in the grid.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append(obj_pixels)
    return objects

def get_bounding_box(objects):
    # Determine bounding box that encompasses all objects
    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for obj in objects:
      for r,c in obj:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c), (max_r, max_c)
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    # Find all contiguous regions (objects) of non-zero color.
    objects = find_objects(input_grid)
    
    # get the bounding box
    (min_r, min_c), (max_r, max_c) = get_bounding_box(objects)
    bounding_box_height = max_r - min_r + 1
    bounding_box_width = max_c - min_c + 1
    
    # Check if bounding box fills the entire input grid
    if (bounding_box_height == input_grid.shape[0] and
        bounding_box_width == input_grid.shape[1]):
        return input_grid
    
    # initialize output_grid
    output_grid = np.zeros((bounding_box_height, bounding_box_width), dtype=int)
    
    # Place objects in output grid, removing empty space.
    for obj_pixels in objects:
        # sort the current obj_pixels 
        obj_pixels.sort()
        # get the current object color from the original grid
        color = input_grid[obj_pixels[0]]
        
        for r, c in obj_pixels:
            # translate the object to the top-left of the output_grid
            output_grid[r - min_r, c - min_c] = color

    return output_grid