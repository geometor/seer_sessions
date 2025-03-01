# b8cdaf2b • 014 • example_3 • investigate_coder

---
```python
"""
1. Preserve Bottom Rows: Copy the bottom two rows of the input grid directly to the output grid.
2. Clear Top Rows: Set all cells in the top rows of output (rows 0 to height-3) to white (0).
3. Insert Corner Blue: Insert the new blue color (1) to the corners of the third row from the bottom, (row = height -3, column = 0, and column = width -1 ).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""

    # Initialize output grid with the same dimensions as the input
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # 1. Preserve Bottom Two Rows
    output_grid[-2:, :] = input_grid[-2:, :]

    # 2. Clear Top Rows (already initialized to 0, which is white)

    # 3. Insert Corner Blue in the Third Row from the Bottom
    if height >= 3:  # Ensure there's at least a third row from the bottom
        output_grid[height - 3, 0] = 1
        output_grid[height - 3, width - 1] = 1

    return output_grid
```
