# 794b24be • 012 • refine_coder

---
```tool_code
"""
Replace all blue pixels with red pixels, keeping white pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell in the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # change output pixels: if the pixel is blue (1), change it to red (2)
            if output_grid[i, j] == 1:
                output_grid[i, j] = 2

    return output_grid
```
