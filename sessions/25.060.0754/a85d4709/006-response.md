# a85d4709 • 006 • refine_coder

---
```python
"""
Transforms a 3x3 input grid to a 3x3 output grid based on a row-dependent color mapping,
specifically considering the colors 0 (white) and 5 (gray) in the input.

- Row 0: White (0) and gray (5) pixels in the input become green (3) in the output.
- Row 1: White (0) and gray (5) pixels in the input become yellow (4) in the output.
- Row 2: White (0) and gray (5) pixels in the input become red (2) in the output.
- Other color pixels keep their original value.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions as the input.
    output_grid = np.array(input_grid).copy()
    rows, cols = output_grid.shape
    
    # Iterate over rows and columns, mapping colors based on row and input color.
    for i in range(rows):
        for j in range(cols):
            if i == 0 and (input_grid[i][j] == 0 or input_grid[i][j] == 5):
                output_grid[i, j] = 3
            elif i == 1 and (input_grid[i][j] == 0 or input_grid[i][j] == 5):
                output_grid[i, j] = 4
            elif i == 2 and (input_grid[i][j] == 0 or input_grid[i][j] == 5):
                output_grid[i, j] = 2

    return output_grid.tolist()
```
