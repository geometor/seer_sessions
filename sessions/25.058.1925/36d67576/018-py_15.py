"""
1.  **Identify Objects:** Examine the input grid to find all contiguous blocks of pixels with the same color.  Each of these blocks is considered an "object."

2.  **Focus on Yellow Objects:**  Isolate the objects that are yellow (color value 4).

3.  **Apply Transformation Based on Shape:**
    *   If a yellow object consists of a *single pixel* (its height and width are both 1), change its color to green (color value 3).
    *   If a yellow object has a height or width greater than 1 (i.e. it is not a single pixel), change its color entirely to blue (color value 1).

4. **Output Grid**: The final output is a new grid where the yellow objects have been transformed according to the rules above, and all other pixels remain unchanged.
"""

import numpy as np

def find_objects(grid):
    # Find contiguous blocks of non-zero pixels
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append((grid[row, col], current_object))  # (color, [(r,c), ...])
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = find_objects(input_grid)

    # Locate yellow objects
    yellow_objects = [obj for color, obj in objects if color == 4]
    
    # Perform Modification based on shape
    for obj_pixels in yellow_objects:
        rows, cols = zip(*obj_pixels)
        height = max(rows) - min(rows) + 1
        width = max(cols) - min(cols) + 1

        if height == 1 and width == 1:
            # Single pixel, change to green
            output_grid[obj_pixels[0]] = 3
        else:
            # Multi-pixel object, change to blue
            for r, c in obj_pixels:
                output_grid[r, c] = 1

    return output_grid