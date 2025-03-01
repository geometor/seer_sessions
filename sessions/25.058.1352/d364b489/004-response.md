# d364b489 • 004 • example_1 • investigate_coder

---
```python
"""
Iterates through each pixel of the input grid. If a pixel is blue (value 1),
a 3x3 block of pixels centered on that pixel's location in the output grid is
created.

The pixel at the center of the 3x3 block remains blue (1).
The pixel immediately to the left of center becomes gray(8)
The pixel immediately above and to the left of the center becomes red (2).
The pixel directly above the center becomes orange(7)
The pixel directly above and to the right of center becomes magenta (6).

Pixels in the output grid that are not part of any 3x3 block created
retain their input value, implicitly zero.
If two or more 3x3 block overlap, pixels are re-written according to the final
overlapping transformation.
"""

import numpy as np

def transform(input_grid):
    output_grid = np.zeros_like(input_grid)  # Initialize with zeros

    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 1:
                # Apply 3x3 transformation
                if r > 0 and c > 0:
                  output_grid[r-1,c-1] = 2
                if r > 0:
                  output_grid[r-1, c] = 7
                if r > 0 and c < cols -1:
                  output_grid[r-1, c+1] = 6
                if c > 0:
                  output_grid[r, c-1] = 8

                output_grid[r, c] = 1  # Center remains 1

    return output_grid
```
