"""
1.  **Identify Two Rectangular Shapes:** Scan the input grid to locate two primary rectangular shapes.
    *   `Shape1`: A rectangle, potentially containing an inner, differently-colored rectangular region.
    *   `Shape2`: A rectangle filled with azure (color 8). This shape may contain empty spaces (color 0) in its interior.

2.  **Extract Inner Shape (from Shape1):** If `Shape1` contains an inner region with a different color than its outer border, extract this inner region as a separate rectangular shape.

3. **Create output grid**: Initialize a new grid by copying `Shape2`.

4.  **Overlay Inner Shape:** If an inner shape was extracted from `Shape1`, overlay it onto the center of `Shape2` in the output grid. Calculate the center position for the overlay by:
    *   Finding the height and width of both `Shape2` and the inner shape.
    *   Centering based on:
        *   `center_row = shape2_top_row + (shape2_height - inner_shape_height) // 2`
        *   `center_col = shape2_left_col + (shape2_width - inner_shape_width) // 2`

5. **Return**: return the output grid
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
    """Transforms the input grid by overlaying the inner part of shape1 on shape2."""
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Identify shape1 and shape2.  shape 2 is color 8, shape 1 is not
    shape1 = None
    shape2 = None
    for obj in objects:
        if obj['color'] == 8:
            shape2 = obj
        else:
            shape1 = obj
    
    # Create the output grid by by copying shape2 and filling with background
    if shape2:
        output_grid = np.zeros_like(input_grid)
        for r in range(shape2['min_r'], shape2['max_r']+1):
             for c in range(shape2['min_c'], shape2['max_c'] + 1):
                output_grid[r,c] = input_grid[r,c]
    else:
        return input_grid  # If shape2 is not found, return the original grid, there could be a test case like this

    # Extract inner shape
    if shape1:
        inner_shape = extract_inner_shape(input_grid, shape1)
        # Overlay inner shape onto shape2
        if inner_shape and shape2:
             height_inner = inner_shape['max_r'] - inner_shape['min_r'] + 1
             width_inner = inner_shape['max_c'] - inner_shape['min_c'] + 1

             height_outer = shape2['max_r'] - shape2['min_r'] + 1
             width_outer = shape2['max_c'] - shape2['min_c'] + 1

             center_r = shape2['min_r'] + (height_outer - height_inner) // 2
             center_c = shape2['min_c'] + (width_outer - width_inner) // 2

             for r in range(height_inner):
                for c in range(width_inner):
                    output_grid[center_r + r, center_c + c] = input_grid[inner_shape['min_r'] + r, inner_shape['min_c'] + c]


    return output_grid