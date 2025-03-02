# d4469b4b • 024 • refine_coder

---
```python
"""
The input grid is scanned for the presence of the color blue (1). If blue is found anywhere in the input grid, the output grid is a 1x1 grid with the color gray (5). If blue is not found, the output grid is a 1x1 grid with the color white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 1x1 array.
    output_grid = np.zeros((1, 1), dtype=int)

    # Check for the presence of blue (1) in the input grid.
    if np.any(input_grid == 1):
        output_grid[0, 0] = 5  # Set output to gray.
    else:
        output_grid[0, 0] = 0  # Set output to white.

    return output_grid
```
