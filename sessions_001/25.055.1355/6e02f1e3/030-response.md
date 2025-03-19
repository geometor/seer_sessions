# 6e02f1e3 • 030 • refine_coder

---
```python
"""
Replace every instance of each unique color found within the input grid with gray (5). Change all other pixels to white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replacing each unique color with gray (5) and the rest with white (0).
    """
    # Create a copy of the input grid to modify.  This avoids in-place modification.
    output_grid = np.copy(input_grid)

    # Find unique colors in the input grid.
    unique_colors = np.unique(input_grid)

    # Iterate through all unique colors.
    for color in unique_colors:
        # Replace all instances of the current color with gray (5).
        output_grid[output_grid == color] = 5

    # Replace all colors other than gray with white
    output_grid[output_grid != 5] = 0

    return output_grid
```

