# 1b2d62fb • 024 • refine_coder

---
```python
"""
The transformation identifies the row containing a blue (color 1) pixel.  It then generates a 3xN output grid, where N is the height of the input grid. The output grid follows a checkered pattern of white (0) and azure (8) pixels.  If the row contains a blue pixel, the output row is [8, 0, 8] if the row index is odd, and [0, 8, 8] if the row index is even. If the row does *not* contain a blue pixel, the output row is all white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid.
    num_rows = input_grid.shape[0]
    num_cols_out = 3
    output_grid = np.zeros((num_rows, num_cols_out), dtype=int)

    # Populate the output grid.
    for i in range(num_rows):
        if 1 in input_grid[i, :]:  # Check if blue exists in the row
            if i % 2 == 0:
                output_grid[i, :] = [0, 8, 8]
            else:
                output_grid[i, :] = [8, 0, 8]
        else:
            output_grid[i, :] = [0, 0, 0]

    return output_grid
```
