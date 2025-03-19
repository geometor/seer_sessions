"""
1. Identify Objects: Find all contiguous vertical lines of a single color (excluding black/background) within the input grid.
2. Select Largest, If Multiple: If the input contains more than one object, select the object with the greatest number of pixels.
3. Select Top Pixel: From the identified object (the line), select the pixel in the highest row (smallest row index, which is the topmost pixel).
4. Create Output: Create an output grid filled with background color (black/0).
5. Place Pixel: Place the selected pixel in the output grid at the top row (row 0) and the same column it occupied in the input grid.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies distinct objects within a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

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
            if not visited[row, col]:
                color = grid[row, col]
                if color != 0:  # Ignore background
                    obj_coords = []
                    dfs(row, col, color, obj_coords)
                    if obj_coords:
                        objects.append({
                            'color': color,
                            'coords': obj_coords,
                            'size': len(obj_coords)
                        })
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    #get objects
    objects = get_objects(input_grid)

    #find largest object
    largest_object = None
    max_size = 0

    for obj in objects:
        if obj['size'] > max_size:
            largest_object = obj
            max_size = obj['size']
    
    #if no objects, return input grid
    if largest_object is None:
        return output_grid

    #get coords of the largest object
    coords = largest_object.get('coords')
    
    if coords:
      #find the top most pixel (smallest row index)
      top_pixel = min(coords, key=lambda item: item[0])

      #Place pixel in output at row 0, same column
      output_grid[0, top_pixel[1]] = largest_object['color']

    return output_grid