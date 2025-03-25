"""
1.  **Identify Objects:** Find all contiguous blocks of non-white (non-zero) pixels. Consider each of these a separate object, regardless of shape.
2.  **Identify Corner/Edge Pixels of Interest:** Find single pixels, that are not part of another object, on the top or bottom row.
3.  **Find target object**: Locate the object with the largest bounding box.
4.  **Reposition:** For each identified pixel from step two, move it to the row directly above target object. Maintain the pixel's original column position. If there are multiple objects, place all other objects above.
"""

import numpy as np

def find_objects(grid):
    """Finds all contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    curr_r, curr_c = stack.pop()
                    obj_pixels.append((curr_r, curr_c, grid[curr_r, curr_c]))

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_r, new_c = curr_r + dr, curr_c + dc
                        if 0 <= new_r < rows and 0 <= new_c < cols and \
                           grid[new_r, new_c] != 0 and not visited[new_r, new_c]:
                            stack.append((new_r, new_c))
                            visited[new_r, new_c] = True
                objects.append(obj_pixels)
    return objects

def find_single_pixels(objects):
    """Finds single-pixel objects."""
    return [obj for obj in objects if len(obj) == 1]

def find_target_object(objects):
    """Finds the object with the largest bounding box."""
    if not objects:
        return None

    largest_object = None
    max_area = -1

    for obj in objects:
        rows, cols = zip(*[(r, c) for r, c, _ in obj])
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)
        area = (max_row - min_row + 1) * (max_col - min_col + 1)
        if area > max_area:
            max_area = area
            largest_object = obj

    return largest_object

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    grid = np.array(input_grid)
    objects = find_objects(grid)
    single_pixels = find_single_pixels(objects)
    other_objects = [obj for obj in objects if len(obj) > 1]
    target_object = find_target_object(other_objects)
    
    #initialize output grid with zeros and same dimensions
    output_grid = np.zeros_like(grid)

    if target_object is None: #handles cases without a target
        return input_grid

    # Get target object top row
    target_rows = [r for r, _, _ in target_object]
    target_top_row = min(target_rows)
    
    #copy target_object into position
    for r, c, val in target_object:
        output_grid[r,c] = val


    # Move single pixels
    for pixel_list in single_pixels:
        for r, c, val in pixel_list:
            new_row = target_top_row -1
            if 0 <= new_row < output_grid.shape[0]: #ensure in grid
              output_grid[new_row, c] = val

    return output_grid.tolist()