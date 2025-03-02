# 794b24be • 038 • example_7 • investigate_coder

---
```python
"""
Convert all blue pixels in the first row of the input grid to red pixels in the output grid, and set any other pixels to white.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Iterate through the first row of the input grid.
    for j in range(input_grid.shape[1]):
        # Check if the pixel in the first row is blue (1).
        if input_grid[0, j] == 1:
            # Change the corresponding pixel in the output grid to red (2).
            output_grid[0, j] = 2
        else:
            # Keep any other pixels in the first row as white in the output
            output_grid[0,j] = input_grid[0,j] if input_grid[0,j] == 0 else 0

    return output_grid
```
