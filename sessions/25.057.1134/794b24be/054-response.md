# 794b24be • 054 • refine_coder

---
```python
"""
Iterate through each pixel of the input grid. If a pixel is blue (value 1), change it to red (value 2) in the output grid.  If a pixel is white (value 0) keep its value as white (0). The dimensions of the output grid should be the same as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.  This automatically
    # ensures the dimensions are the same.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the input grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is blue (1)
            if output_grid[i, j] == 1:
                # Change blue pixels to red (2)
                output_grid[i, j] = 2
            # White pixels (0) are implicitly handled because output_grid
            # is initialized as a copy of input_grid.

    return output_grid
```

