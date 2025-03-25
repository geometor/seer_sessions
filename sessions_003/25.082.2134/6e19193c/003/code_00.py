"""
1.  **Object Identification:** Identify all contiguous blocks of non-zero pixels in the input grid. Each block is considered a separate object, and its color and pixel positions are recorded.

2.  **Vertical Center Line:** Define a vertical center line down the middle of the grid (between columns 5 and 6 for a 10x10 grid).

3.  **Horizontal Center Line:** Define a horizontal center line down the middle of the grid (between rows 5 and 6 for a 10x10 grid).

4.  **Object Transformation - Left Side:** Any object entirely to the left of the vertical center line is moved to the vertical center line. The top most pixel of the moved object retains it's original row.

5. **Object Transformation - Right side**: Any object to the right of the center line is moved to create a diagonal line from top right to bottom left.

6.  **Object Transformation - Horizontal Center:** Any object crossing or touching the horizontal center line is mirrored to other side of the grid, right most pixel becomes left most and vice versa.

7.  **Output Grid:** Create a new grid (10x10, initialized with 0/white). Place the transformed objects onto this grid based on the transformation rules.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != obj_color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, obj_color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r,c], current_object))  # Store color and object
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    vertical_center = cols // 2
    horizontal_center = rows // 2

    # Find objects
    objects = find_objects(input_grid)
    
    #change output pixels
    for color, obj in objects:
        #find top most pixel of object
        top_row = min(r for r, c in obj)
        
        # --- Left Side Transformation ---
        if all(c < vertical_center for r, c in obj):
            #find left most column of this object
            
            # Move to vertical center, same row
            for r,c in obj:
              output_grid[r,vertical_center - (c - min(c_temp for r_temp, c_temp in obj))] = color
              

        # --- Right Side Transformation ---        
        elif all(c >= vertical_center for r, c in obj):
            # objects to right of vertical center
            
            # find distance from vertical center
            #dist = obj[0][1] - vertical_center #using first point of object
            
            # get a sorted list of coordinates
            sorted_obj = sorted(obj, key=lambda x: (-x[0],x[1])) #sort by largest row first
            
            start_r = sorted_obj[0][0] 
            start_c = sorted_obj[0][1]
            dist =  start_c-vertical_center
            
            
            #move first pixel
            new_r = start_r + dist
            new_c = start_c - dist - dist #go left by amount it was to the right
            
            if new_r < rows and new_c >=0:
                output_grid[new_r, new_c] = color
            
            #move other pixels in object based on offset from this new position
            for r,c in sorted_obj[1:]:
              #find offset for other obj
              offset_r = r - start_r
              offset_c = c - start_c
                
              place_r = new_r+offset_r
              place_c = new_c+offset_c #apply same offset
                
              if place_r < rows and place_c >= 0:
                output_grid[place_r,place_c] = color

        # --- Horizontal Center Transformation ---
        if any(r == horizontal_center - 1 or r == horizontal_center for r, _ in obj):
            for r_orig, c_orig in obj:
                output_grid[r_orig, cols - 1 - c_orig] = color

    return output_grid