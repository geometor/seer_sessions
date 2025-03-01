# d631b094 • 006 • refine_coder

---
```python
"""
Checks for green pixels. If present, outputs a 1x1 green grid. Otherwise, counts blue pixels and outputs a 1xN blue grid, where N is the blue count. If neither color is present, returns an empty grid.
"""

import numpy as np

def transform(input_grid):
    # Check for the presence of green (3) pixels.
    if np.any(input_grid == 3):
        # Create a 1x1 output grid with a green pixel.
        output_grid = np.array([[3]], dtype=int)
        return output_grid

    # Count the number of blue (1) pixels in the input grid.
    blue_count = np.sum(input_grid == 1)

    # if blue exists, create output
    if blue_count > 0:
      # Create a 1xN output grid filled with blue pixels.
      output_grid = np.ones((1, blue_count), dtype=int)
      return output_grid

    # If neither green nor blue are present, return an empty array, represented by 0x0
    return np.empty((0, 0), dtype=int)
```
