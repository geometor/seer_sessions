# 1b2d62fb • 026 • refine_coder

---
```python
"""
The transformation identifies rows in the input grid that contain at least one blue (1) pixel. The output grid always has a width of 3, and the same height of the input grid. For each row in the input grid:

1.  **Check for Blue:** If a row contains a blue pixel, a specific checkered pattern of white (0) and azure (8) pixels is generated for that row in the output grid.
    - If the row is even numbered (starting from 0): create a `[0, 8, 8]` pattern
    - if the row is odd numbered: create a `[8, 0, 8]` pattern

2.  **No Blue:** If a row does *not* contain a blue pixel, the corresponding output row is filled with all white (0) pixels (`[0, 0, 0]`).

The output grid's height matches the input grid's height, and its width is always 3.
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
