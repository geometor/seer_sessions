```python
"""
1.  **Identify Objects:** Find two rectangular objects in the input grid. `shape1` is the rectangle located in the upper portion of the grid. `shape2` is the rectangle located in the lower portion of the grid.
2.  **Extract Inner Shape:** From `shape1`, extract the contiguous inner region. The inner region may contain pixels of a different color than the border of `shape1`, or be empty (color 0).
3.  **Create Output:** Create an output grid of the same dimensions as the input grid, initially empty (filled with color 0).
4.  **Copy Shape2:** Copy `shape2` to the output grid in the same position it was in the input grid.
5.  **Overlay Inner Shape:** Copy the extracted inner shape (from step 2) onto the output grid. Center the inner shape within the boundaries of `shape2`, based on their respective widths and heights.
"""

import numpy as np

def find_objects_by_position(grid):
    """Finds rectangular objects in the grid and identifies them by position."""
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

    # Identify shape1 and shape2 by position (top and bottom)
    if len(objects) >= 2:  # Ensure at least two objects for comparison
        # Sort by top-left row (min_r), then top-left col (min_c)
        objects.sort(key=lambda obj: (obj['min_r'], obj['min_c']))
        shape1 = objects[0]  # Topmost object
        shape2 = objects[-1]  # Bottommost object
        return shape1, shape2
    elif len(objects) == 1:
        return objects[0],None #only one shape found
    else:
        return None, None  # No objects found

def extract_inner_shape(grid, outer_shape):
    """Extracts the inner shape from a given outer shape."""
    if not outer_shape:
        return None
    outer_color = outer_shape['color']
    inner_coords = []
    for r in range(outer_shape['min_r'] + 1, outer_shape['max_r']):
        for c in range(outer_shape['min_c'] + 1, outer_shape['max_c']):
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

     # get the colors from the input grid
    inner_colors = []
    for r,c in inner_coords:
        inner_colors.append(grid[r,c])
    inner_shape['colors'] = inner_colors
    return inner_shape

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Find objects
    shape1, shape2 = find_objects_by_position(input_grid)

    # Extract inner shape
    inner_shape = extract_inner_shape(input_grid, shape1)

    # Copy shape2 to output
    if shape2:
        for r in range(shape2['min_r'], shape2['max_r'] + 1):
            for c in range(shape2['min_c'], shape2['max_c'] + 1):
                output_grid[r, c] = input_grid[r, c]

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

        for i, (r,c) in enumerate(inner_shape['coords']):
            output_grid[center_r + (r - inner_shape['min_r']), center_c + (c - inner_shape['min_c'])] = inner_shape['colors'][i]

    return output_grid
```