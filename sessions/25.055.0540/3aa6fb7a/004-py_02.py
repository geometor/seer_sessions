"""
1.  **Identify Azure Objects:** Locate all contiguous blocks of azure (8) pixels within the input grid. A contiguous block is defined as one or more azure pixels that are directly adjacent to each other (horizontally or vertically).
2.  **Topmost Row Identification:** For each identified azure object, determine the topmost row that the object occupies.
3.  **Leftmost Pixel on Topmost Row:** Within each object, identify the leftmost pixel among those pixels that are on the object's topmost row.
4.  **Change to Blue:** Change the color of the identified leftmost pixel (on the topmost row of its object) from azure (8) to blue (1).
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)


    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Find contiguous blocks of azure (8) pixels.  For each block, find the
    topmost row it occupies.  Among the pixels on the topmost row, change
    the leftmost one to blue (1).
    """
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    for obj in azure_objects:
        # Find the topmost row for the current object.
        topmost_row = min(obj, key=lambda x: x[0])[0]

        # Filter pixels to only those on the topmost row.
        top_row_pixels = [pixel for pixel in obj if pixel[0] == topmost_row]

        # Find the leftmost pixel on the topmost row.
        leftmost_top_pixel = min(top_row_pixels, key=lambda x: x[1])

        # Change the identified pixel to blue (1).
        output_grid[leftmost_top_pixel[0], leftmost_top_pixel[1]] = 1

    return output_grid