"""
The azure L-shaped objects are unchanged. Blue pixels (color 1) are added, if possible, horizontally adjacent (left/right) to azure pixels belonging to an L-shaped structure, where such addition does not change the overall L shape of the object.
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous regions of the same color in the grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def is_l_shape(obj, grid):
    """
    Checks if a given object (list of coordinates) forms an L-shape.
    """
    if len(obj) != 3:
        return False

    # Convert coordinates to numpy array for easier calculations
    coords = np.array(obj)
    
    # Calculate differences between coordinates
    diffs = np.diff(coords, axis=0)

    
    if not (np.all(diffs[:, 0] >= 0) or np.all(diffs[:, 0] <= 0)):
        return False
        
    if not (np.all(diffs[:, 1] >= 0) or np.all(diffs[:,1] <= 0)):
        return False
    
    # check that is an "L" and not a line
    
    d1 = [ obj[1][0] - obj[0][0] , obj[1][1] - obj[0][1] ]
    d2 = [ obj[2][0] - obj[1][0] , obj[2][1] - obj[1][1] ]

    if d1[0] != 0 and d1[1] != 0: return False
    if d2[0] != 0 and d2[1] != 0: return False

    return True
    

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    objects = get_objects(input_grid)

    if 8 in objects:
        for obj in objects[8]:
            if is_l_shape(obj, input_grid):
                #find topleft and bottomright
                obj_coords = np.array(obj)
                top_left_index = np.argmin(obj_coords.sum(axis=1))
                bottom_right_index = np.argmax(obj_coords.sum(axis=1))
                top_left = obj[top_left_index]
                bottom_right = obj[bottom_right_index]
                
                # Add blue pixel to the right of top_left, within bounds.
                if top_left[1] + 1 < cols:
                  output_grid[top_left[0], top_left[1] + 1] = 1
                # Add blue pixel to the left of bottom_right, within bounds
                if bottom_right[1] -1 >= 0:
                  output_grid[bottom_right[0] , bottom_right[1] - 1] = 1
                  

    return output_grid