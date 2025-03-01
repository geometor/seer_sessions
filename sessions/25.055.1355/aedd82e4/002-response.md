# aedd82e4 • 002 • example_1 • investigate_coder

---
```python
"""
The output grid is a copy of the input grid, with one modification: The pixel in the bottom-left corner is changed from red to blue. All other pixels remain the same.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Change the color of the pixel in the bottom-left corner to blue (1)
    output_grid[output_grid.shape[0] - 1, 0] = 1

    return output_grid
```
