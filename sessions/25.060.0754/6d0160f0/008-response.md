# 6d0160f0 • 008 • example_1 • investigate_coder

---
```python
"""
Maintain all 'Gray' (5) pixels to output grid.
Maintain all pixels that are not 'Gray'(5) in the same column as any Gray pixel to the output grid.
Replace other pixel with a 'Gray'(5) pixel.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find columns containing gray pixels
    gray_columns = set()
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 5:
                gray_columns.add(c)

    # Iterate through the grid and apply the transformation
    for r in range(rows):
        for c in range(cols):
            # Maintain gray pixels
            if input_grid[r, c] == 5:
                continue  # Already gray, no change needed
            # Maintain non-gray pixels in gray columns
            elif c in gray_columns:
                continue # Pixel in same column as gray, no change
            # Replace other pixels with gray
            else:
                output_grid[r, c] = 5

    return output_grid
```
