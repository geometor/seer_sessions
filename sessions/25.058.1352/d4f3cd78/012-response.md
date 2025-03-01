# d4f3cd78 • 012 • refine_coder

---
```python
"""
1.  **Identify** all distinct, contiguous gray (5) shapes in the input grid.
2.  **Find** the horizontal center of the grid.
3.  For each gray shape:
    a. **Find** the top row of the shape.
    b. **Draw** a vertical line of azure (8) pixels, starting from the top edge of the shape, extending upwards to the top edge of the grid, aligned with the horizontal center.
    c. **Fill** with azure (8) only the gray (5) pixels *within that specific shape* that are directly below any azure (8) pixels.
"""

import numpy as np
from skimage.measure import label, regionprops

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    center_x = output_grid.shape[1] // 2

    # Identify all distinct gray objects
    gray_objects = label(input_grid == 5, connectivity=1)

    # Iterate through each gray object
    for obj_label in range(1, np.max(gray_objects) + 1):
        object_coords = np.argwhere(gray_objects == obj_label)

        # skip if no gray object exists
        if len(object_coords) == 0:
            continue

        min_row = np.min(object_coords[:, 0])

        # Draw vertical azure line
        for y in range(min_row):
            output_grid[y, center_x] = 8

        # Fill gray pixels within the object below the azure line
        object_mask = (gray_objects == obj_label)
        for x in range(input_grid.shape[1]):
            if output_grid[min_row -1, x] == 8:
              for y in range(min_row, input_grid.shape[0]):
                  if object_mask[y,x] and output_grid[y,x] == 5 :
                    output_grid[y, x] = 8
                  elif object_mask[y,x]:
                    break # stop when hitting a different color in this object

    return output_grid
```
