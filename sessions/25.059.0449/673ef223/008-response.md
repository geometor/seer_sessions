# 673ef223 • 008 • refine_coder

---
```python
"""
Transforms the input grid by expanding an azure region horizontally to the left based on its proximity to the left edge, introducing a yellow pixel to the right of the original azure pixel, maintaining the left red line, and transforming the rightmost red line into an azure region of fixed width, starting from the column immediately to its left.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of all pixels of the specified color.
    objects = []
    rows, cols = np.where(grid == color)
    for r, c in zip(rows, cols):
        objects.append((r, c))
    return objects

def find_rightmost_red_line_start(grid):
    # Find the starting column of the rightmost red line.
    red_pixels = find_objects(grid, 2)
    if not red_pixels:
        return None
    max_col = -1
    for _, c in red_pixels:
        if c > max_col:
            max_col = c
    return max_col

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    input_height, input_width = input_grid.shape

    # Find the azure and red pixels.
    azure_pixels = find_objects(input_grid, 8)
    red_pixels = find_objects(input_grid, 2)

    # 1. & 2. Left azure transformation.
    for r, c in azure_pixels:
        if c < input_width / 2:  # Check for left side
            # Expand azure to the left by one less than the original column index.
            for i in range(c):
                if c - i -1 >= 0:
                  output_grid[r, c - i - 1] = 8

            # 3. Yellow Insertion
            if c + 1 < input_width:  # Check boundary
                output_grid[r, c + 1] = 4  # Add a yellow pixel to the right.

    # 4, 5, 6. Right red line transformation
    right_red_start = find_rightmost_red_line_start(input_grid)

    if right_red_start is not None:
        for r, c in red_pixels:
             if c == right_red_start: # Rightmost red line only
                for i in range(6):
                    if c - 1 - i >= 0:  # start one position to the left of red
                        output_grid[r, c - 1 - i] = 8  # azure, span 6 pixels


    # 7. Maintain left red line: No changes needed as we copied input_grid initially.

    return output_grid
```
