# 99b1bc43 • 018 • refine_coder

---
```python
"""
1.  **Scan Input:** Examine the upper-left 4x4 region of the input grid.
2.  **Check for Colors:** For each cell within this region, check if the color is blue (1), red (2), or yellow (4).
3.  **Create Output:** Create a 4x4 output grid, initially filled with white (0).
4.  **Mark Presence:** If a cell in the scanned region of the input grid is blue, red, or yellow, change the corresponding cell in the output grid to green (3). The row and column in the output grid should be identical.
5. If a cell in the scanned region of input grid is not blue, red, or yellow, it is
   not changed (remains white/0).
6. The final output grid has been created.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid to highlight regions of blue, red and yellow with green and the rest with white."""

    input_array = np.array(input_grid)
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the upper-left 4x4 region of the input grid.
    for i in range(min(4, input_array.shape[0])):  # Ensure we don't go out of bounds
        for j in range(min(4, input_array.shape[1])): # Ensure we don't go out of bounds
            # Check for blue (1), red (2), or yellow (4).
            if input_array[i][j] in (1, 2, 4):
                # Mark the corresponding position in the output grid with green (3).
                output_grid[i][j] = 3

    return output_grid.tolist()
```
