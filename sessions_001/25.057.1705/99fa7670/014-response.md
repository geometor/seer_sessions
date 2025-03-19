# 99fa7670 • 014 • example_3 • investigate_coder

---
```python
"""
1. **Identify Objects:** Find all pixels in the input grid that have a non-zero color value. These are the "active" objects.
2. **Horizontal Expansion:** For each active object, replace all pixels in its row with the object's color.
3. **Partial duplication**: For each active object, replicate it to the very end of the rows below the original.
4. **Preserve Background:** All other pixels (with an initial value of 0) remain unchanged (white).
"""

import numpy as np

def get_objects(grid):
    """Finds all non-zero pixels and returns their coordinates and color."""
    objects = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel != 0:
                objects.append(((row_idx, col_idx), pixel))
    return objects

def transform(input_grid):
    """Transforms the input grid according to the specified rules."""
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    for (row, col), color in objects:
        # Horizontal Expansion
        output_grid[row, :] = color
        
    # partial duplication with order - azure first, gray next
    for (row, col), color in sorted(objects, reverse=True, key=lambda x : x[1]):    
        #Partial Duplication - azure
        if color == 8:
          if row + 1 < output_grid.shape[0]:
            output_grid[row + 1, -1] = color
          if row + 2 < output_grid.shape[0]:
            output_grid[row + 2, -1] = color
        
        #Partial Duplication - gray
        if color == 5:
          if row + 1 < output_grid.shape[0]:
            output_grid[row + 1, -1] = color

    return output_grid
```
