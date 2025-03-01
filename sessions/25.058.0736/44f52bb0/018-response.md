# 44f52bb0 • 018 • refine_coder

---
```python
"""
Identifies single-pixel colored objects (excluding black) in the input grid.
If there are exactly two such objects, the output is a 1x1 blue (1) grid.
Otherwise, the output is a 1x1 black (0) grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid to a 1x1 black grid.
    output_grid = np.array([[0]])

    # Find single-pixel objects (excluding black).
    unique_colors = np.unique(input_grid)
    single_pixel_objects_count = 0

    for color in unique_colors:
        if color != 0:  # Exclude black
            count = np.count_nonzero(input_grid == color)
            if count == 1:
                single_pixel_objects_count += 1

    # Check if the count of single-pixel objects is exactly 2.
    if single_pixel_objects_count == 2:
        output_grid = np.array([[1]])

    return output_grid
```

