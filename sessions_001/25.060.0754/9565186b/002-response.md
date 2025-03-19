# 9565186b • 002 • example_4 • investigate_coder

---
```python
"""
Examine the input grid. The output grid replaces certain colors with gray (5) based on the following rule:
If an azure (8), a blue(1), a red(2), a green(3) is present, then replace them with grey(5), keeping every other color in place.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the cell's color needs to be replaced with gray (5)
            if output_grid[i, j] in [1, 2, 3, 8]:
                output_grid[i, j] = 5

    return output_grid
```
