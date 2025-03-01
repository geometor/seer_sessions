"""
1.  **Object Detection:** Find "L-shaped" objects. An L-shaped object is defined as a 2x2 block of pixels with the same, non-zero color, with one additional pixel of that same color connected to any of the corner.
2. **Object Position:** The position of output is based on the corner of the 2x2 block.
3.  **Transformation:** Create a 3x3 block of pixels at the same position of the 2x2 corner identified. The central pixel will be color '3', and the surrounding pixels will be '2'. All other cells will be '0'.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in a grid.  An object is a set of connected pixels of the same color.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, object_id):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        objects[object_id]['pixels'].append((r, c))
        dfs(r + 1, c, color, object_id)
        dfs(r - 1, c, color, object_id)
        dfs(r, c + 1, color, object_id)
        dfs(r, c - 1, color, object_id)

    object_id = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                objects[object_id] = {'color': grid[r, c], 'pixels': []}
                dfs(r, c, grid[r, c], object_id)
                object_id += 1

    return objects

def detect_l_shape(grid, objects):
    """Detects L-shaped objects within the grid."""
    l_shapes = []
    rows, cols = grid.shape

    for obj_id, obj_data in objects.items():
        pixels = obj_data['pixels']
        color = obj_data['color']
        
        # Check for 2x2 blocks
        for r in range(rows - 1):
            for c in range(cols - 1):
                if (grid[r,c] == color and grid[r+1,c] == color and
                    grid[r,c+1] == color and grid[r+1,c+1] == color):
                    #check for a fifth pixel
                    corners = [(r-1,c),(r-1,c+1),(r-1,c+2),(r,c+2),(r+1,c+2),(r+2,c+2),
                               (r+2,c+1),(r+2,c),(r+1,c-1),(r,c-1)]
                    for cr,cc in corners:
                        if 0 <= cr < rows and 0 <= cc < cols and grid[cr,cc] == color:
                            l_shapes.append({'color': color, 'corner':(r,c)}) #corner of 2x2
                            break #found l shape
    return l_shapes

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    
    # find objects
    input_objects = find_objects(input_grid)
    
    # detect l shapes, get corner
    l_shapes = detect_l_shape(input_grid, input_objects)
    
    # fill based on l_shape corner
    for l_shape in l_shapes:
        r,c = l_shape['corner']
        for dr in range(3):
            for dc in range(3):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if dr == 1 and dc == 1:
                        output_grid[nr,nc] = 3
                    else:
                        output_grid[nr,nc] = 2

    return output_grid