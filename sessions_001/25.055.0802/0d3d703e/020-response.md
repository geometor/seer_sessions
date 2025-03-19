# 0d3d703e • 020 • example_4 • investigate_coder

---
```python
"""
The transformation rule is a one-to-one mapping of input pixel values (colors) to output pixel values (colors). Specifically:

1. Iterate through each pixel in the input grid.
2. If the pixel's value is 9 (maroon), change it to 8 (azure).
3. If the pixel's value is 4 (yellow), change it to 3 (green).
4. If the pixel's value is 2 (red), change it to 6 (magenta).
5. Maintain the grid's original 3x3 structure.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # define the color mapping
    color_map = {
        9: 8,
        4: 3,
        2: 6
    }

    # iterate through each pixel in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # apply color mapping
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid
```
