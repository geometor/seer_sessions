"""
1.  **Identify Objects:** Find all distinct objects in the input grid. An object is a contiguous block of non-zero pixels.
2.  **Find Single-Pixel Objects:** Identify objects consisting of only one pixel.
3. **Find Multi-Pixel Objects** Identify objects consisting of more than one pixel.
4.  **Transformation based on Object Size:**
    *   If there's both single and multi pixel object - Copy the multi-pixel object to the output grid unchanged. Expand and position an object with matching shape and color, anchored to the location of the single pixel object.
    *  If only single pixel object in the input - no change
    * If only multi pixel objects - no change

5. Mirror the single pixel object using the dimensions and location of the multi pixel object
6. **Construct Output:** Combine the unchanged objects and the transformed single pixel object.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects in the grid.  An object is a group of
    contiguous non-zero pixels.
    Uses depth first search
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, current_object):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] == 0):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, col, current_object)
        dfs(row, col - 1, col, current_object)

    for row in range(rows):
        for col in range(cols):
            if grid[row, col] != 0 and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def bounding_box(object_pixels):
    """
    Find the smallest rectangle enclosing a single object.
    """
    min_row = float('inf')
    max_row = float('-inf')
    min_col = float('inf')
    max_col = float('-inf')

    for row, col in object_pixels:
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    return (min_row, max_row, min_col, max_col)

def mirror_position(point, min_row, max_row, min_col, max_col):
    """
    Mirror a point within the object's bounding box
    """
    center_row = (min_row + max_row) / 2
    center_col = (min_col + max_col) / 2
    mirrored_row = int(2 * center_row - point[0])
    mirrored_col = int(2 * center_col - point[1])
    return (mirrored_row, mirrored_col)
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    single_pixel_objects = [obj for obj in objects if len(obj) == 1]
    multi_pixel_objects = [obj for obj in objects if len(obj) > 1]
    
    if len(single_pixel_objects) > 0 and len(multi_pixel_objects) > 0:
       # get the single pixel object and location
       single_pixel_object = single_pixel_objects[0]
       single_pixel_row, single_pixel_col = single_pixel_object[0]

       #get multi pixel object, and bounding box
       multi_pixel_object = multi_pixel_objects[0]
       min_row, max_row, min_col, max_col = bounding_box(multi_pixel_object)
       
       # remove the original single pixel
       output_grid[single_pixel_row,single_pixel_col] = 0
       
       #get color
       color = input_grid[single_pixel_row,single_pixel_col]

       # create the mirrored object
       height = max_row - min_row + 1
       width = max_col - min_col + 1
       
       new_min_row = single_pixel_row - height // 2
       new_min_col = single_pixel_col - width // 2
       
       # original object
       for r, c in multi_pixel_object:
           mir_row, mir_col = mirror_position((r,c),min_row, max_row, min_col, max_col)
           new_r = mir_row - min_row + new_min_row
           new_c = mir_col - min_col + new_min_col
           if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
               output_grid[new_r,new_c] = input_grid[r,c]

    elif len(single_pixel_objects) > 0 and not multi_pixel_objects:
      output_grid = input_grid
    elif not single_pixel_objects and len(multi_pixel_objects) > 0:
       output_grid = input_grid      
    return output_grid.tolist()