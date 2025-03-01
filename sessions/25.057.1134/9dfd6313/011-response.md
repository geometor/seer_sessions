# 9dfd6313 • 011 • refine_coder

---
```python
"""
Transformation Rule:

1.  Identify Objects: Find all contiguous blocks of non-zero colored pixels in the input grid.  Each block is an object.
2.  Vertical to Horizontal: If an object in the input grid is a vertical line (height > 1 and width = 1), transform this object into a horizontal line in the output grid.
    -  The horizontal line should have the same color as the vertical line.
    -  The horizontal line should have a length (width) equal to the height of the vertical line.
    - The horizontal lines row should be the same as the vertical lines min_row
    - The horizontal lines col should be one less then the input vertical lines col.
3.  Preserve Single Pixels: If an object in the input grid is a single pixel (height = 1 and width = 1), it should remain in the same position and with the same color in the output grid.
4.  Multiple Objects of the same color: If multiple objects have the same color, each is transformed.
5.  Background: All the zero (white) pixels remain unchanged.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies objects (contiguous non-zero pixels) and their properties.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, obj_pixels):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                if obj_pixels:
                    min_row = min(p[0] for p in obj_pixels)
                    max_row = max(p[0] for p in obj_pixels)
                    min_col = min(p[1] for p in obj_pixels)
                    max_col = max(p[1] for p in obj_pixels)
                    objects.append({
                        'color': int(grid[r, c]),
                        'pixels': obj_pixels,
                        'min_row': int(min_row),
                        'max_row': int(max_row),
                        'min_col': int(min_col),
                        'max_col': int(max_col),
                        'height': int(max_row - min_row + 1),
                        'width': int(max_col - min_col + 1)
                    })
    return objects


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # get objects
    objects = get_objects(input_grid)

    # change output pixels 
    for obj in objects:
        if obj['height'] > 1 and obj['width'] == 1:
            # Vertical to Horizontal transformation
            color = obj['color']
            length = obj['height']
            row = obj['min_row']
            col = obj['min_col'] -1
            for i in range(length):
                if col + i < output_grid.shape[1]: # boundary check
                  output_grid[row, col + i] = color
        elif obj['height'] == 1 and obj['width'] == 1:
            # preserve single pixels
             output_grid[obj['min_row'],obj['min_col']] = obj['color']
        else:
          # handle other shapes - for now just copy them
          for r,c in obj['pixels']:
            output_grid[r,c] = obj['color']
    return output_grid
```
