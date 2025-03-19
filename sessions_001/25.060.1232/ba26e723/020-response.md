# ba26e723 • 020 • refine_coder

---
```python
"""
1. Identify the Target Object: Find a horizontal line of connected yellow pixels in the top row of the input grid.
2. Transform: Change the color of *all* pixels in that identified line to magenta.
3. Preserve: All other pixels in the grid remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    rows, cols = input_grid.shape
    output_grid = input_grid.copy()

    # Find the start and end of the yellow line in the top row
    start = -1
    end = -1
    for c in range(cols):
        if input_grid[0, c] == 4:
            if start == -1:
                start = c
            end = c
        elif start != -1:
            break  # Line ended

    # If a yellow line was found, change it to magenta
    if start != -1:
        for c in range(start, end + 1):
            output_grid[0, c] = 6

    return output_grid
```
