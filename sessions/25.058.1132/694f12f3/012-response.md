# 694f12f3 • 012 • refine_coder

---
```python
"""
Identifies yellow rectangles in the input grid and fills their inner area with a different color, maintaining a one-pixel yellow border.
If there's only one rectangle, it's filled with red. If there are two, the one positioned more towards the top or right is filled with red, and the other with blue.
"""

import numpy as np

def find_objects(grid, color):
    # Find all objects of a specific color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
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
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_rectangle_bounds(object_pixels):
    # get bounding box
    min_row = min(pixel[0] for pixel in object_pixels)
    max_row = max(pixel[0] for pixel in object_pixels)
    min_col = min(pixel[1] for pixel in object_pixels)
    max_col = max(pixel[1] for pixel in object_pixels)

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find yellow objects
    yellow_objects = find_objects(input_grid, 4)

    # Handle the cases based on the number of yellow rectangles
    if len(yellow_objects) == 1:
        # Fill the single rectangle with red
        min_row, max_row, min_col, max_col = get_rectangle_bounds(yellow_objects[0])
        for row in range(min_row + 1, max_row):
            for col in range(min_col + 1, max_col):
                output_grid[row, col] = 2  # Red

    elif len(yellow_objects) == 2:
        # Determine which rectangle is more top-right
        min_row1, max_row1, min_col1, max_col1 = get_rectangle_bounds(yellow_objects[0])
        min_row2, max_row2, min_col2, max_col2 = get_rectangle_bounds(yellow_objects[1])

        # Calculate a score for "top-rightness" (lower row and higher col is better)
        score1 = -min_row1 + max_col1
        score2 = -min_row2+ max_col2
        
        if score1 > score2:
            fill_color1 = 2
            fill_color2 = 1
        elif score2 > score1:
            fill_color1 = 1
            fill_color2 = 2
        else: #same score
            if min_row1 < min_row2: # object 1 is higher, so fill red
                fill_color1 = 2
                fill_color2 = 1
            else:
                fill_color1 = 1
                fill_color2 = 2


        # Fill the rectangles accordingly
        for row in range(min_row1 + 1, max_row1):
            for col in range(min_col1 + 1, max_col1):
                output_grid[row, col] = fill_color1
        for row in range(min_row2 + 1, max_row2):
            for col in range(min_col2 + 1, max_col2):
                output_grid[row, col] = fill_color2

    return output_grid
```
