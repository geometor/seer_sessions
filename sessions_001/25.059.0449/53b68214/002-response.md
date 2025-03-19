# 53b68214 • 002 • example_3 • investigate_coder

---
```python
"""
The transformation rule is a vertical downward extension of the input shape, making it occupy more rows downwards until the height of grid is 10.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically extending the non-zero pixels downwards.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((10, cols), dtype=int)

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # If a non-zero pixel is found
            if input_grid[r, c] != 0:
                # Copy the pixel to the output grid
                output_grid[r, c] = input_grid[r, c]
                # Extend the pixel downwards until row 9
                for r_out in range(r + 1, 10):
                    output_grid[r_out, c] = input_grid[r, c]

    return output_grid.tolist()
```
