"""
1.  **Identify Objects:** Find two primary rectangular objects, `shape1_outer` and `shape2_outer`.
    *   `shape1_outer`: A rectangle in the upper portion of the grid. Its border color defines the outer shape, and it contains an inner rectangular shape, `shape1_inner`.
    *   `shape2_outer`: A rectangle filled with azure (color 8) in the lower portion, containing another rectangle, `shape2_inner`.
2. **Extract Inner Shape:** Use depth first search (DFS) to get the `shape1_inner` from shape1 by finding a contiguous rectangle inside `shape1_outer` that excludes the border pixels.
3. **Extract Inner Shape:** Use depth first search (DFS) to get the shape2_inner from shape2 by finding a contiguous rectangle inside shape2_outer, filled with color 0.
4.  **Overlay:** Overlay the extracted `shape1_inner` onto the center of `shape2_outer` in the output grid. Center it based on the dimensions of `shape2_outer` and `shape1_inner`, replacing `shape2_inner`.
5. **Copy Remainder:** The non-object pixels of the input are copied into the output.
"""

import numpy as np

def find_objects(grid):
    """Finds rectangular objects in the grid and their inner shapes."""
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
                        outer_shape = {
                            "color": grid[r, c],
                            "coords": object_coords,
                            "min_r": min_r,
                            "max_r": max_r,
                            "min_c": min_c,
                            "max_c": max_c
                        }

                        inner_shape = extract_inner_shape(grid, outer_shape, visited)
                        outer_shape['inner_shape'] = inner_shape
                        objects.append(outer_shape)
    return objects

def extract_inner_shape(grid, outer_shape, visited):
    """Extracts the inner shape from a given outer shape using DFS."""
    outer_color = outer_shape['color']
    inner_coords = []

    # Create a local visited array to track visited cells within this function
    local_visited = np.copy(visited)

    def is_valid(r, c):
        return (outer_shape['min_r'] <= r <= outer_shape['max_r'] and
                outer_shape['min_c'] <= c <= outer_shape['max_c'])

    def dfs_inner(r, c, color):
        if not is_valid(r, c) or local_visited[r, c] or grid[r, c] != color:
            return
        local_visited[r, c] = True
        inner_coords.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs_inner(r + dr, c + dc, color)
    
    #Find a starting point for inner shape, skip the border
    for r in range(outer_shape['min_r'] + 1, outer_shape['max_r']):
        for c in range(outer_shape['min_c'] + 1, outer_shape['max_c']):
            if grid[r,c] != outer_color:
                dfs_inner(r,c,grid[r,c])
                break #exit after the first inner shape is found
        if inner_coords:
            break

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
        'max_c': max_c,
        'color' : grid[inner_coords[0]]
    }

    return inner_shape

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find objects
    objects = find_objects(input_grid)
    
    #identify shape1 and shape2 by color
    shape1_outer = None
    shape2_outer = None

    for obj in objects:
        if obj['color'] == 8:
            shape2_outer = obj
        else:
            shape1_outer = obj

    # Overlay inner shape onto shape2
    if shape1_outer and shape1_outer['inner_shape'] and shape2_outer:
        inner_shape = shape1_outer['inner_shape']
        height_inner = inner_shape['max_r'] - inner_shape['min_r'] + 1
        width_inner = inner_shape['max_c'] - inner_shape['min_c'] + 1
        
        height_outer = shape2_outer['max_r'] - shape2_outer['min_r'] + 1
        width_outer = shape2_outer['max_c'] - shape2_outer['min_c'] + 1
        
        #find center start row
        center_r = shape2_outer['min_r'] + (height_outer - height_inner) // 2
        #find center start column
        center_c = shape2_outer['min_c'] + (width_outer - width_inner) // 2
        
        for r in range(height_inner):
            for c in range(width_inner):
                output_grid[center_r+r,center_c+c] = input_grid[inner_shape['min_r'] + r, inner_shape['min_c'] +c]
    

    return output_grid