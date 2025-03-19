# 6430c8c4 • 016 • refine_coder

---
```python
"""
1. **Identify Top-Left Object:** Find the dimensions of the contiguous block of same-colored pixels starting from the top-left corner of the input grid.
2. **Output Grid Size:**  The output grid has the same dimensions as this top-left object.
3. **Color Transformation:**
    * If the top-left object's color is NOT azure (8), fill the output grid with green (3).
    * If the top-left object's color IS azure (8), fill the output grid with white (0).
"""

import numpy as np

def get_object_dimensions(grid):
    """Find the dimensions of top-left colored object."""
    rows, cols = grid.shape
    first_color = grid[0,0]
    height = 0
    width = 0

    for r in range(rows):
        if grid[r,0] == first_color:
            height+=1
        else:
            break

    for c in range(cols):
        if grid[0,c] == first_color:
            width +=1
        else:
            break
    return height, width

def transform(input_grid):
    # Initialize numpy arrays for input grid
    input_grid = np.array(input_grid)

    #get object_dimensions
    height, width = get_object_dimensions(input_grid)
    # Initialize output_grid
    output_grid = np.zeros((height, width), dtype=int)

    # Get the color of the top-left object
    top_left_color = input_grid[0, 0]

    # Apply color transformation based on the top-left object's color
    if top_left_color != 8:
        output_grid[:] = 3  # Fill with green
    else:
        output_grid[:] = 0  # Fill with white

    return output_grid.tolist()
```
