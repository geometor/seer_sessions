# b527c5c6 • 024 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all green and red pixels. Treat each contiguous block of the same color as a distinct object.
2.  **Green Object Transformation:**
    *   The green object changes location, or expands vertically based on its relative position to the red pixels.
    * The transformation changes according to the number and relative locations of the red pixels.
3.  **Red Pixel Transformation**:
    * If only one red pixel is present, it is transformed into a vertical line.
    * If more that one red pixel is present, the upper red pixel is transformed into a vertical line, and the bottom red pixel expands to the right until reaching the width of the expanded green object.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color."""
    visited = set()
    objects = []

    def dfs(row, col):
        """Depth-first search to find contiguous pixels."""
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        object_pixels = [(row, col)]
        object_pixels.extend(dfs(row + 1, col))
        object_pixels.extend(dfs(row - 1, col))
        object_pixels.extend(dfs(row, col + 1))
        object_pixels.extend(dfs(row, col - 1))
        return object_pixels

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                objects.append(dfs(row, col))
    return objects

def transform(input_grid):
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    
    # Handle green object transformation
    if green_objects:
        if len(red_objects) == 0:
           pass # No red pixel, no change to green
        elif len(red_objects) == 1:
           # Relocate the green pixels.
           red_pixel_row = red_objects[0][0][0]
           red_pixel_col = red_objects[0][0][1]

           for green_pix in green_objects[0]:
               output_grid[green_pix[0], green_pix[1]] = 0
           output_grid[red_pixel_row, red_pixel_col] = 3

        else:  # Multiple red pixels (assume 2 for now)
            # Determine upper and lower red pixels
            red_objects.sort(key=lambda obj: obj[0][0])  # Sort by row
            upper_red_pixel = red_objects[0][0]
            lower_red_pixel = red_objects[1][0]

            # Expand green downwards
            if len(green_objects) > 0:
                min_green_row = min([p[0] for p in green_objects[0]])
                max_green_row = max([p[0] for p in green_objects[0]])
                min_green_col = min([p[1] for p in green_objects[0]])
                max_green_col = max([p[1] for p in green_objects[0]])
                for r in range(min_green_row, lower_red_pixel[0] +1):
                    for c in range(min_green_col, max_green_col + 1):
                        output_grid[r,c] = 3


    # Handle red pixel transformation
    if len(red_objects) == 1:
        # Transform into a vertical line
        red_pixel_row = red_objects[0][0][0]
        red_pixel_col = red_objects[0][0][1]
        output_grid[:, red_pixel_col] = 2
    elif len(red_objects) > 1:
        # Upper red pixel to vertical line
        output_grid[:, upper_red_pixel[1]] = 2

        # Lower red pixel expands horizontally
        row = lower_red_pixel[0] -1 #move up one row
        if green_objects:
           max_green_col = max([p[1] for p in green_objects[0]])
           for col in range(lower_red_pixel[1], max_green_col + 1):
            output_grid[row, col] = 2


    return output_grid
```
