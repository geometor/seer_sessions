"""
1. **Identify and Isolate Objects:** Find all non-white (color not 0) connected regions (objects) in the input grid. In this example, we find two objects: a red object and a green object.
2. **Extract Colors**: Record the distinct colors of those objects, here Red (2) and Green(3).
3. **Create Output Grid:** Create an output grid with dimensions based on number of objects. the height of each colored object determines height of the columns. The width will be the number of colors, in our case 2.
4. **Arrange Colors:** Put first color in first column, second color in the second column. Repeat colors vertically down their respective columns.
"""

import numpy as np

def find_objects(grid):
    """Find connected regions of non-zero pixels."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                if obj_pixels:
                    objects.append((grid[r,c], obj_pixels))
    return objects

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(np.array(input_grid))

    # Extract distinct colors and their heights
    colors = []
    heights = []

    for color, pixels in objects:
        colors.append(color)

        #calculate heights
        rows = [p[0] for p in pixels]
        min_row = min(rows)
        max_row = max(rows)
        heights.append(max_row - min_row + 1)


    # Determine output grid dimensions: max_height x number_of_colors
    output_height = max(heights)
    output_width = len(colors)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Arrange colors in columns
    for i, color in enumerate(colors):
        for j in range(output_height):
          output_grid[j, i] = color

    return output_grid