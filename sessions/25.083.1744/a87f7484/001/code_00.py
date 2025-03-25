"""
1.  **Identify Objects:** Scan the input grid and identify all distinct "objects." An object is defined as a contiguous block of pixels of the same non-zero color.
2.  **Select Object:** Select the final object from the object by last row, then by last column
3.  **Construct Output:** create a 3x3 output grid, filling it according to the arrangement of colors in the selected object. If an object is selected, that object will have one pixel of the value 0 that defines a "background" for the object, relative to it's shape.
"""

import numpy as np

def find_objects(grid):
    objects = []
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_coords):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != color:
            return
        visited.add((r, c))
        obj_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, obj_coords)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r][c] != 0:
                obj_coords = []
                dfs(r, c, grid[r][c], obj_coords)
                objects.append(obj_coords)
    return objects

def get_object_background_relative_position(obj_coords):
    """Finds the relative position of the background (0) pixel within an object."""

    # Convert list of tuples to numpy array for easier manipulation
    obj_coords = np.array(obj_coords)

    min_r = np.min(obj_coords[:, 0])
    max_r = np.max(obj_coords[:, 0])
    min_c = np.min(obj_coords[:, 1])
    max_c = np.max(obj_coords[:, 1])
    
    # background needs to calculate 
    background_r = -1
    background_c = -1

    for r in range(min_r,max_r+1):
        for c in range(min_c, max_c +1):
            found = False
            for coord in obj_coords:
                if r == coord[0] and c == coord[1]:
                    found = True
                    break
            if not found:
                background_r = r
                background_c = c
                break
        if background_r != -1:
            break
            
    if background_r == -1:
        return None
    

    # Calculate relative position
    rel_r = background_r - min_r
    rel_c = background_c - min_c

    return (rel_r, rel_c)
    

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Select Object (last object)
    if not objects:
        return np.zeros((3, 3), dtype=int)  # Return empty grid if no objects
    
    selected_object_coords = objects[-1]
    selected_color = input_grid[selected_object_coords[0][0]][selected_object_coords[0][1]]
    
    object_coords = np.array(selected_object_coords)
    min_row = np.min(object_coords[:, 0])
    min_col = np.min(object_coords[:, 1])

    # Get relative background position
    background_pos = get_object_background_relative_position(selected_object_coords)


    # 3. Construct Output
    output_grid = np.zeros((3, 3), dtype=int)
    if background_pos is not None:
        for r in range(3):
            for c in range(3):
                check_r = min_row + (r-background_pos[0])
                check_c = min_col + (c-background_pos[1])
                
                coord_found = False
                
                for coord in selected_object_coords:
                  if coord[0] == check_r and coord[1] == check_c:
                    coord_found = True
                    output_grid[r,c] = selected_color
                    break

    return output_grid