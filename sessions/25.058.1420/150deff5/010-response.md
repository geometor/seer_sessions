# 150deff5 • 010 • example_2 • investigate_coder

---
```python
"""
Identify a contiguous block of gray (5) pixels forming the shape of "5". Recolor the top row and leftmost column of the "5" to azure (8). Recolor the remaining inner portion and bottom segment of the "5" to red (2).
"""

import numpy as np

def find_shape(grid, color):
    # Find all pixels of the specified color
    pixels = np.argwhere(grid == color)
    if len(pixels) == 0:
        return None, None, None

    # Determine bounding box
    min_row, min_col = np.min(pixels, axis=0)
    max_row, max_col = np.max(pixels, axis=0)
    
    shape_pixels = []
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col+1):
            if grid[r,c] == color:
                shape_pixels.append((r,c))

    return shape_pixels, (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find the "5" shape (gray pixels)
    shape_pixels, top_left, bottom_right = find_shape(input_grid, 5)
    if shape_pixels is None:
        return output_grid #return if not found
    
    min_row, min_col = top_left
    max_row, max_col = bottom_right

    # Recolor the shape
    for r, c in shape_pixels:
        if r == min_row or c == min_col:
            output_grid[r, c] = 8  # Azure
        else:
            output_grid[r,c] = 2 # red

    return output_grid
```
