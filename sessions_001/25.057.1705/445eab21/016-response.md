# 445eab21 • 016 • refine_coder

---
```python
"""
Finds a 2x2 square within the input grid where a yellow "C" shape exists and a
blue pixel is located in the bottom-right corner of the 2x2 square.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a dictionary where keys are colors and values are lists of pixel coordinates.
    """
    objects = {}
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
            if (r, c) not in visited:
                color = grid[r, c]
                if color != 0:  # Ignore background
                    obj_pixels = []
                    dfs(r, c, color, obj_pixels)
                    if color not in objects:
                        objects[color] = []
                    objects[color].append(obj_pixels)
    return objects

def is_c_shape(pixels, grid):
    """
    Checks if a set of pixels roughly forms a "C" shape.  A very basic check.
    """
    if len(pixels) < 4:  # "C" needs at least 4 pixels
        return False

    # Check for a roughly rectangular/square bounding box
    rows, cols = zip(*pixels)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    # Simple heuristic:  If the area of the bounding box is close to the number
    # of pixels, it's likely not a "C" (more like a filled rectangle).  A "C"
    # would have a smaller area occupied compared to its bounding box.
    bounding_box_area = (max_row - min_row + 1) * (max_col - min_col + 1)

    return bounding_box_area > len(pixels) * 1.2 # at least 20 percent bigger

def transform(input_grid):
    """
    Transforms the input grid by finding a 2x2 square where a yellow "C" shape
    is present and the bottom-right pixel of the 2x2 square is blue.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((2, 2), dtype=int)

    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check for blue pixel at the bottom-right of the 2x2 square
            if input_grid[r+1, c+1] == 1:
                # Extract 2x2 square
                square = input_grid[r:r+2, c:c+2]

                # Check if the pixels in and around this square might form part
                # of yellow "C" shape.

                potential_c_pixels = []
                # Expand search slightly beyond 2x2 square for potential C shape.
                for r_check in range(max(0, r -1), min(rows,r+3)):
                   for c_check in range(max(0,c-1),min(cols,c+3)):
                        if input_grid[r_check,c_check] == 4:
                           potential_c_pixels.append((r_check,c_check))

                if is_c_shape(potential_c_pixels,input_grid):
                    output_grid = square
                    return output_grid

    return output_grid
```
