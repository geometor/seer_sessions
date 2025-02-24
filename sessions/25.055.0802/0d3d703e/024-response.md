# 0d3d703e • 024 • refine_coder

---
```python
"""
The transformation rule is a one-to-one color mapping applied to each pixel in the input grid. The mapping is as follows:

1.  Maroon (9) pixels become Azure (8).
2.  Yellow (4) pixels become Green (3).
3.  Red (2) pixels become Magenta (6).
4.  All other colors remain unchanged.
5.  The grid structure (3x3) is preserved.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # define the color mapping
    color_map = {
        9: 8,  # Maroon to Azure
        4: 3,  # Yellow to Green
        2: 6   # Red to Magenta
    }

    # iterate through each pixel in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # apply the color mapping if the current pixel's color is in the map
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid
```

