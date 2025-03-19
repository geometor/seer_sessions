# 6e82a1ae • 010 • example_2 • investigate_coder

---
```python
"""
Transforms a grid of pixels, changing gray (5) pixels to red (2), green (3), or blue (1) based on their spatial arrangement.

1.  **Identify Objects:** Find all contiguous blocks of gray (5) pixels. These are our input shapes.
2.  **Determine New Color:** For each gray shape, determine its new color based on the following rules:
    *   If the shape is a "horizontal line segment" (3 or more gray pixels in a row), change to red (2).
    *   If a pixel is on its own, check which color horizontal segment is closest. Assign pixel the value of segment color plus 1. If blue or red is closest at the same distance, choose the blue.
    * If shape is a 2x1, the color is blue (1).
3.  **Apply Transformation:** Replace the gray (5) pixels of each shape with the determined new color.
4.  **Output:** all white (0) remains unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of pixels of a specified color."""
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_horizontal_line(obj):
    """Checks if an object is a horizontal line segment of length 3 or more."""
    if len(obj) < 3:
        return False
    rows = [r for r, _ in obj]
    return len(set(rows)) == 1

def distance(r1,c1,r2,c2):
    return abs(r1-r2) + abs(c1 - c2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all gray objects
    gray_objects = find_objects(input_grid, 5)

    red_objects = []
    blue_objects = []

    # Determine the new color for each object
    for obj in gray_objects:
        if is_horizontal_line(obj):
            # Change to red (2)
            for r, c in obj:
                output_grid[r, c] = 2
            red_objects.append(obj)

        elif len(obj) == 2:
            rows = [pos[0] for pos in obj]
            cols = [pos[1] for pos in obj]

            if len(set(rows)) > len(set(cols)):   # stacks on top of each other
                #change to blue (1)
                for r,c in obj:
                    output_grid[r, c] = 1
                blue_objects.append(obj)
        

    for obj in gray_objects:

        if len(obj) == 1:
            r,c = obj[0]

            # find minimum distance from red object
            min_dist_red = 1000
            if len(red_objects) > 0:

                for red in red_objects:
                    for red_r, red_c in red:
                        dist = distance(r,c,red_r,red_c)
                        if dist < min_dist_red:
                            min_dist_red = dist


            # find minimum distance from blue object
            min_dist_blue = 1000
            if len(blue_objects) > 0:
                for blue in blue_objects:
                    for blue_r, blue_c in blue:
                        dist = distance(r,c,blue_r,blue_c)
                        if dist < min_dist_blue:
                            min_dist_blue = dist

            if min_dist_red < min_dist_blue:
                output_grid[r,c] = 3 # red + 1
            else:
                output_grid[r,c] = 2 # blue + 1  - handles the case where both are the same dist


    return output_grid
```
