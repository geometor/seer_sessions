"""
The transformation rule can be described as follows:

1.  **Grid Scaling:** The output grid's dimensions are half the size of the input grid's dimensions in both height and width. Integer division is used, so any fractional part is discarded.

2.  **Object Scaling:** Each object within the input grid is scaled down proportionally. An object's width and height in the output grid are calculated by dividing its original width and height by two. If the result has decimal, round up to the largest integer (e.g. 3 / 2 = 1.5 -> 2). The color of each object is preserved.

3. **Object Placement** Objects maintain their relative positions within the grid.

4.  **Identity Transform as a Special Case**: If scaling down, then back up by the scaling factor, results in an identical grid, keep the original, otherwise, scale down.
"""

import numpy as np
import math

def find_objects(grid):
    """Finds non-white objects in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_id, color):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return []

        visited.add((r, c))
        object_pixels = [(r, c)]

        # Check adjacent pixels (horizontal and vertical)
        neighbors = [(r, c + 1), (r, c - 1), (r+1, c), (r-1, c)]
        for nr, nc in neighbors:
             object_pixels.extend(dfs(nr, nc, obj_id, color))

        return object_pixels

    obj_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_pixels = dfs(r, c, obj_id_counter, grid[r, c])
                if obj_pixels:
                    objects.append({
                        "id": obj_id_counter,
                        "color": grid[r, c],
                        "pixels": obj_pixels
                    })
                    obj_id_counter += 1

    return objects

def get_object_dimensions(obj):
    """Calculates the width and height of an object."""
    pixels = np.array(obj["pixels"])
    min_row, min_col = np.min(pixels, axis=0)
    max_row, max_col = np.max(pixels, axis=0)
    width = max_col - min_col + 1
    height = max_row - min_row + 1
    return width, height, min_row, min_col

def scale_object(obj, scale_factor=2):
    """Scales down an object's dimensions."""
    width, height, _, _ = get_object_dimensions(obj)
    new_width = math.ceil(width / scale_factor)
    new_height = math.ceil(height / scale_factor)
    return new_width, new_height

def transform(input_grid):
    # Grid Scaling
    input_rows, input_cols = input_grid.shape
    output_rows = input_rows // 2
    output_cols = input_cols // 2

    # Check for Identity Transform
    if input_rows == output_rows * 2 and input_cols == output_cols * 2:
       
        # Find objects and their scaled dimensions
        objects = find_objects(input_grid)
        all_scaled_objects = []
        
        for obj in objects:
            scaled_width, scaled_height = scale_object(obj)
            all_scaled_objects.append((scaled_width * 2, scaled_height * 2))

        # if all the scaled objects fit within a 2x2 of original grid, then return copy of the input
        if all((w,h) == (2,2) or (w,h) == (1,2) or (w,h) == (2,1) or (w,h) == (1,1) for w, h in all_scaled_objects):
            return input_grid.copy()

    # Initialize output grid
    output_grid = np.zeros((output_rows, output_cols), dtype=int)


    # Find and Scale Objects
    objects = find_objects(input_grid)
    for obj in objects:
        # Object Scaling
        new_width, new_height = scale_object(obj)

        # Object Placement (maintain relative position)
        _, _, min_row, min_col = get_object_dimensions(obj)
        new_min_row = min_row // 2
        new_min_col = min_col // 2

        # Fill output grid with scaled object
        for r in range(new_height):
            for c in range(new_width):
                if new_min_row + r < output_rows and new_min_col + c < output_cols:
                  output_grid[new_min_row + r, new_min_col + c] = obj["color"]

    return output_grid