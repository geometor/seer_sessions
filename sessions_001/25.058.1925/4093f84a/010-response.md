# 4093f84a • 010 • example_2 • investigate_coder

---
```python
"""
1. Identify all pixels with the color green (value 3).
2. Change the green pixels to white (value 0).
3. Leave all other pixels (gray and white) unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by removing green pixels.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of all green pixels.
    green_pixels = np.where(output_grid == 3)

    # Change the green pixels to white (0).
    output_grid[green_pixels] = 0

    return output_grid
```

