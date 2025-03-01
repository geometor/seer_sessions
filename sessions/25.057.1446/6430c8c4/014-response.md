# 6430c8c4 • 014 • example_3 • investigate_coder

---
```python
"""
The transformation rule involves dividing the input grid into 2x2 regions (ignoring the last row if the height is odd).
If any non-white pixel exists within a 2x2 region, the corresponding output pixel is green (3).
Otherwise, if the 2x2 region contains only white pixels, the output pixel is white (0).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through 2x2 regions, effectively ignoring the last row
    for i in range(4):
        for j in range(4):
            # Extract the 2x2 region from the input grid
            region = input_grid[i*2:min((i+1)*2, rows), j*2:(j+1)*2]
            
            # Check if any non-white pixel exists in the region
            if np.any(region != 0):
                output_grid[i, j] = 3  # Set output pixel to green
            else:
                output_grid[i, j] = 0  # Set output pixel to white

    return output_grid.tolist()
```
