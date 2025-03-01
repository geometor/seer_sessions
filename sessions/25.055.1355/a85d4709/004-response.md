# a85d4709 • 004 • refine_coder

---
```python
"""
1.  **Initialization:** Begin with an input grid of arbitrary size.
2.  **Value Mapping:** Iterate through each pixel in the input grid.
    *   If a pixel's value is 0, change it to 3 (green).
    *   If a pixel's value is 5, change it to 4 (yellow).
    *   All other pixel values remain unchanged.
3.  **Output:** The modified grid becomes the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # change output pixels based on the mapping rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 4

    return output_grid
```

