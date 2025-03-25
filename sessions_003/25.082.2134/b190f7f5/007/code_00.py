"""
1.  **Identify Objects:** Find all connected components (objects) in the input grid. An object is defined as a group of one or more adjacent pixels of the same non-zero color.
2.  **Object Transformations:**
    *   **Duplication and Resizing**: In the output, the objects are recreated and formed into 2xN rectangle where N depends on object position.
    *   **Elimination**: Some object can be completely removed.

3. **Output grid assembly** The duplicated and resized objects are placed on the output at specific coordinates. The placement follows a tiling/mirroring pattern.
4. **Object selection for processing**: not all objects are processed. Object with color 8 are consistently removed.
"""

import numpy as np

def get_objects(grid):
    objects = []
    visited = set()

    def dfs(r, c, color, current_object):
        if (r, c) in visited or r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, color, current_object)
        dfs(r - 1, c, color, current_object)
        dfs(r, c + 1, color, current_object)
        dfs(r, c - 1, color, current_object)
        dfs(r+1, c+1, color, current_object)
        dfs(r-1, c-1, color, current_object)
        dfs(r-1, c+1, color, current_object)
        dfs(r+1, c-1, color, current_object)
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r, c], current_object))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Identify objects in the input grid
    objects = get_objects(input_grid)

    # Determine output dimensions based on input and observed pattern
    output_rows = 0
    output_cols = 0
    
    for color, obj_pixels in objects:
        if color != 8:
            output_rows = max(output_rows, len(obj_pixels) * 3 )
            output_cols = max(output_cols,len(obj_pixels) *3 )
    output_rows = output_rows * (1 if len(objects) <= 2 else 2)
    output_cols = output_cols* (1 if len(objects) <= 2 else 2)
   
    output_grid = np.zeros((int(output_rows), int(output_cols)), dtype=int)
    # Process each object, excluding those with color 8
    object_count = 0

    for color, obj_pixels in objects:

        if color != 8:  # Skip objects of color 8
            # Calculate height and width (assuming a rectangle for simplicity)
            rows, cols = zip(*obj_pixels)
            height = 3 # height of a duplicated object fixed to two
            width =  len(set(cols)) # base the value on number of columns occupied

            #Duplicate and create rectangles
            row_start_index = (object_count // 2) * (height * 2 )
            col_start_index = (object_count % 2) * (2* width*2)


            for i in range(2):
                for j in range(2):

                    for r in range(height):
                         for c in range(width * 2):
                            output_grid[row_start_index +  r + (height* i), col_start_index+ c+ (j*width) ] = color

            object_count +=1


    return output_grid