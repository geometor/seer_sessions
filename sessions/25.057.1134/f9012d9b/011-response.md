# f9012d9b • 011 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous blocks of the same color in the input grid.
2.  **Filter:** Keep only the black objects.
3. **Output:** The remaining objects form the output grid. The blue objects are removed.
"""

import numpy as np
from scipy.ndimage import label

def get_objects(grid):
    labeled_grid, num_objects = label(grid)
    objects = []
    for i in range(1, num_objects + 1):
        object_pixels = (labeled_grid == i)
        object_color = grid[object_pixels][0]
        objects.append((object_pixels, object_color))
    return objects

def transform(input_grid):
    # initialize output_grid to be the same size/type, but all white (0)
    output_grid = np.zeros_like(input_grid)

    # Get all objects in the input grid.
    objects = get_objects(input_grid)

    # Filter to keep only black objects and copy them to the output
    for object_pixels, object_color in objects:
        if object_color == 0:  # Black color is 0
            output_grid[object_pixels] = object_color

    return output_grid
```

