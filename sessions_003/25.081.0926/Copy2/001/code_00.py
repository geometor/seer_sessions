"""
1.  **Identify Shapes:** Locate two primary rectangular shapes in the input grid. The first shape (`shape1`) is located in the upper portion of the grid and may contain an inner shape with different colors than the outside of `shape1`. The second shape (`shape2`) is in the lower portion and is initially filled with azure (color 8) and may have empty space (color 0) on the interior.
2.  **Extract Inner Shape:** From `shape1`, extract the contiguous inner region that does not have the same color as the outer border of `shape1`.
3.  **Copy Base:** Copy `shape2` from the input grid to the output grid.
4.  **Overlay:** Overlay the inner shape extracted in step 2 onto the center of `shape2` in the output grid. Center it based on the width and height of shape2 and inner shape .
5. **Copy remainder:** Copy other areas of input to output.
"""

import numpy as np

def find_objects(grid):
    """Finds rectangular objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, object_coords):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        object_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, object_coords)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                object_coords = []
                dfs(r, c, grid[r, c], object_coords)
                if object_coords:
                    min_r = min(coord[0] for coord in object_coords)
                    max_r = max(coord[0] for coord in object_coords)
                    min_c = min(coord[1] for coord in object_coords)
                    max_c = max(coord[1] for coord in object_coords)

                    # check if rectangle
                    is_rectangle = True
                    for r_i in range(min_r, max_r + 1):
                        for c_i in range(min_c, max_c+1):
                            if (r_i,c_i) not in object_coords:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break
                    if is_rectangle:
                        objects.append({
                            "color": grid[r, c],
                            "coords": object_coords,
                            "min_r": min_r,
                            "max_r": max_r,
                            "min_c": min_c,
                            "max_c": max_c
                        })
    return objects

def extract_inner_shape(grid, outer_shape):
    """Extracts the inner shape from a given outer shape."""
    outer_color = outer_shape['color']
    inner_coords = []
    for r in range(outer_shape['min_r'] + 1, outer_shape['max_r']):
        for c in range(outer_shape['min_c'] + 1, outer_shape['max_c']):
            if grid[r, c] != outer_color:
                inner_coords.append((r, c))
    
    if not inner_coords:
        return None

    min_r = min(coord[0] for coord in inner_coords)
    max_r = max(coord[0] for coord in inner_coords)
    min_c = min(coord[1] for coord in inner_coords)
    max_c = max(coord[1] for coord in inner_coords)
    
    inner_shape = {
        'coords': inner_coords,
        'min_r': min_r,
        'max_r': max_r,
        'min_c': min_c,
        'max_c': max_c
    }

    #get the color by checking inside the coords
    inner_shape['color'] = grid[inner_shape['coords'][0]]
    return inner_shape

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find objects
    objects = find_objects(input_grid)
    
    #identify shape1 and shape2 by location
    shape1 = None
    shape2 = None

    for obj in objects:
        if obj['color'] == 8:
            shape2 = obj
        else:
            #assume shape 1 is always on top
            shape1 = obj

    # Extract inner shape
    if shape1:
        inner_shape = extract_inner_shape(input_grid, shape1)

        # Overlay inner shape onto shape2
        if inner_shape and shape2:
            height_inner = inner_shape['max_r'] - inner_shape['min_r'] + 1
            width_inner = inner_shape['max_c'] - inner_shape['min_c'] + 1
            
            height_outer = shape2['max_r'] - shape2['min_r'] + 1
            width_outer = shape2['max_c'] - shape2['min_c'] + 1
            
            #find center start row
            center_r = shape2['min_r'] + (height_outer - height_inner) // 2
            #find center start column
            center_c = shape2['min_c'] + (width_outer - width_inner) // 2
            
            for r in range(height_inner):
                for c in range(width_inner):
                   output_grid[center_r+r,center_c+c] = input_grid[inner_shape['min_r'] + r, inner_shape['min_c'] +c]
    

    return output_grid