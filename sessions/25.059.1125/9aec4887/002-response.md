# 9aec4887 • 002 • example_3 • investigate_coder

---
```python
"""
The input grid is transformed into a smaller output grid. The transformation identifies distinct colored "objects" (contiguous blocks of the same non-zero color) in the input grid, extracts their colors, and arranges them in a condensed 6x6 output grid. The relative positions of the objects from the input are somewhat preserved, but their original shapes are not. Empty space (color 0) is largely eliminated. The output grid is created to the combined unique colors of all bounding boxes, 6x6, where each color has 1 horizontal and 1 vertical line in the grid. Arrange the colors of the objects in the output grid by checking how the object colors are laid out in the bounding boxes and create a combined output grid.
"""

import numpy as np

def find_objects(grid):
    # Find all distinct objects in the grid.
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r, c], current_object))
    return objects

def get_bounding_boxes(objects):
    # Get the bounding box for each object.

    bounding_boxes = []
    for color, obj in objects:
        min_r, min_c = float('inf'), float('inf')
        max_r, max_c = float('-inf'), float('-inf')
        for r, c in obj:
            min_r = min(min_r, r)
            min_c = min(min_c, c)
            max_r = max(max_r, r)
            max_c = max(max_c, c)
        bounding_boxes.append((color, (min_r, min_c, max_r, max_c)))
    return bounding_boxes

def get_colors_in_bounding_boxes(grid, bounding_boxes):
    # get all unique colors in all the bounding box

    boxes_colors = []
    for _, (min_r, min_c, max_r, max_c) in bounding_boxes:
        colors = set()
        for r in range(min_r, max_r+1):
            for c in range(min_c, max_c + 1):
                colors.add(grid[r,c])
        boxes_colors.append(colors)
    return boxes_colors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    objects = find_objects(input_grid)
    bounding_boxes = get_bounding_boxes(objects)
    boxes_colors = get_colors_in_bounding_boxes(input_grid, bounding_boxes)

    # get the unique colors
    unique_colors = []
    for box in boxes_colors:
        for color in box:
            if color not in unique_colors:
                unique_colors.append(color)

    # get the order of colors as they appear in bounding boxes
    ordered_colors = []
    for _, (min_r, min_c, max_r, max_c) in bounding_boxes:
        for r in range(min_r, max_r+1):
            for c in range(min_c, max_c + 1):
                color = input_grid[r,c]
                if color in unique_colors and color not in ordered_colors:
                    ordered_colors.append(color)

    # Create output grid.
    output_grid = np.zeros((6, 6), dtype=int)

    # change output pixels
    color_x = {}
    color_y = {}

    # assign x and y to unique colors
    x = 1
    y = 1
    for color in ordered_colors:
      if color != 0:
        color_x[color] = x
        color_y[color] = y
        x += 1
        if x > 4:
          x = 1
          y += 1


    # map bounding box content to output grid
    for _, (min_r, min_c, max_r, max_c) in bounding_boxes:
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                color = input_grid[r,c]
                if color != 0:
                  output_grid[color_y[color], color_x[color]] = color

    # draw horizontal lines.
    for y in range(1,5):
      for color in ordered_colors:
        if color != 0 and color_y[color] == y:
            for x in range(0, 6):
                if output_grid[y,x] == 0:
                    output_grid[y,x] = color

    # draw vertical lines.
    for x in range(1,5):
      for color in ordered_colors:
        if color != 0 and color_x[color] == x:
            for y in range(0, 6):
                if output_grid[y, x] == 0:
                  output_grid[y, x] = color

    return output_grid
```
