# 0d3d703e • 014 • example_3 • investigate_coder

---
```python
"""
The transformation involves a direct color substitution on a 3x3 grid. The input grid's colors are replaced according to the following rule:

1.  Gray (5) is replaced with Blue (1).
2.  Azure (8) is replaced with Maroon (9).
3.  Magenta (6) is replaced with Red (2).

The spatial configuration of the grid, including the position of each pixel, remains unchanged during the transformation. The output grid is a direct color-mapped version of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by applying a color substitution.
    """
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Define the color mapping
    color_map = {
        5: 1,  # Gray to Blue
        8: 9,  # Azure to Maroon
        6: 2   # Magenta to Red
    }

    # Iterate through the input grid and apply color substitution
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] in color_map:
                output_grid[i, j] = color_map[output_grid[i, j]]

    return output_grid
```
