# b0c4d837 • 024 • refine_coder

---
```python
"""
Locates all azure (8) pixels in the input grid, then creates a 3x3 output grid.
The output grid is filled with the azure pixels from the input grid, row by row.
If there are fewer than 9 azure pixels, the remaining cells in the output grid are black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as 3x3 filled with 0 (black)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find azure (8) pixels
    azure_pixels = []
    for r_idx, row in enumerate(input_grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 8:
                azure_pixels.append((r_idx, c_idx))

    # Fill the output grid with azure pixels, row by row.
    count = 0
    for r in range(3):
        for c in range(3):
            if count < len(azure_pixels):
                output_grid[r][c] = 8
                count += 1

    return output_grid
```
