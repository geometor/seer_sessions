# 94f9d214 • 004 • refine_coder

---
```python
"""
The transformation rule is as follows:
1. Focus on the upper half: Consider only the top half rows of the input grid. The number of rows in the top half will be equal to the floor of the number of rows divided by two.
2. Maintain width: the output has the same width as the input.
3. Check for colored pixel: For each cell in the focused region of the input grid.
4. Transform colored pixels in the region:
    *   If the input cell is not white (0), set output to red (2).
    *   If the input cell is white (0), output remains white(0).
"""

import numpy as np

def transform(input_grid):
    # Get dimensions of the input grid
    rows, cols = input_grid.shape

    # Initialize the output grid with the same width and half the height, filled with white (0)
    output_grid = np.zeros((rows // 2, cols), dtype=int)

    # Iterate through the top half of the input grid
    for i in range(rows // 2):
        for j in range(cols):
            # Check if the pixel in the input grid is not white (0)
            if input_grid[i, j] != 0:
                # If not white, set the corresponding output pixel to red (2)
                output_grid[i, j] = 2

    return output_grid
```

