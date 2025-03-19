# 6150a2bd • 012 • refine_coder

---
```python
"""
1. Rotate the input grid 90 degrees clockwise.
2. Apply the following color transformations based on the *original* color in the input grid *before* rotation:
    *   Blue (1) remains Blue (1).
    *   Green (3) changes to Red (2).
    *   Magenta (6) changes to White (0).
    *   Gray (5) remains Gray (5).
    *   Yellow (4) changes to Gray (5).
"""

import numpy as np

def transform(input_grid):
    # Rotate the grid 90 degrees clockwise.
    input_grid = np.array(input_grid)
    rotated_grid = np.rot90(input_grid, k=-1)
    output_grid = rotated_grid.copy() # work on copy since modifying rotated

    # Apply color transformations based on original input colors.
    height, width = input_grid.shape
    for r in range(height):
        for c in range(width):
            original_color = input_grid[r, c]
            rotated_row = c
            rotated_col = height - 1 - r
            
            if original_color == 1:
                output_grid[rotated_row, rotated_col] = 1
            elif original_color == 3:
                output_grid[rotated_row, rotated_col] = 2
            elif original_color == 6:
                output_grid[rotated_row, rotated_col] = 0
            elif original_color == 5:
                output_grid[rotated_row, rotated_col] = 5
            elif original_color == 4:
                output_grid[rotated_row, rotated_col] = 5

    return output_grid.tolist()
```

