# 794b24be • 030 • refine_coder

---
```python
"""
1.  **Initialization:** Create an output grid of the same dimensions as the input grid, filled with zeros (white).
2.  **Iterate:** For each non-zero pixel in the input grid:
    *   Get its row and column position.
    *   In the output grid, set the pixel at the *same* row and column position to red (value 2).
3. Return the output grid
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with zeros, same size as input
    output_grid = np.zeros_like(input_grid)

    # Iterate through all non-zero pixels in the input grid
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if input_grid[row, col] != 0:
                # Set the corresponding pixel in the output grid to red (2)
                output_grid[row, col] = 2

    return output_grid
```
