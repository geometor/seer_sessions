# 1190e5a7 • 014 • refine_coder

---
```python
"""
The transformation rule identifies the largest rectangle formed by the color '8' (azure) within the input grid. The output grid is a cropped section of the input grid, corresponding to the area *before* (above and to the left) of this rectangle. If multiple such rectangles exist, the topmost and leftmost one is chosen. If no '8' rectangle is found, the output is an empty grid of size 0x0. The '8' rectangle must have a width and height of at least 1.
"""

import numpy as np

def find_largest_8_rectangle(grid):
    """Finds the top-left and bottom-right coordinates of the largest 8-rectangle."""
    rows, cols = grid.shape
    max_area = 0
    top_left = (0, 0)

    for r1 in range(rows):
        for c1 in range(cols):
            if grid[r1, c1] == 8:
                for r2 in range(r1, rows):
                    for c2 in range(c1, cols):
                        is_rectangle = True
                        for r in range(r1, r2 + 1):
                            for c in range(c1, c2 + 1):
                                if grid[r, c] != 8:
                                    is_rectangle = False
                                    break
                            if not is_rectangle:
                                break
                        if is_rectangle:
                            area = (r2 - r1 + 1) * (c2 - c1 + 1)
                            if area > max_area:
                                max_area = area
                                top_left = (r1, c1)
    if max_area > 0 :
        return top_left
    return None

def transform(input_grid):
    """
    Extracts a sub-grid from the input, stopping before the largest 8-rectangle.
    """
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # Find the top-left corner of the largest 8-rectangle
    top_left = find_largest_8_rectangle(input_grid)
   
    if top_left is not None:
      # Crop above and left of rectangle
      output_grid = input_grid[:top_left[0], :top_left[1]]
    else:
      # if no rectangle, return empty grid
      output_grid = np.empty((0,0))

    return output_grid.tolist()
```
