# ba26e723 • 026 • refine_coder

---
```python
"""
Iterates through the input grid, identifies yellow (4) pixels, and checks if the pixels directly above or below are black (0). If either neighbor is black, the yellow pixel is changed to magenta (6).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # Identify yellow pixels
            if output_grid[i, j] == 4:
                # Check neighbors above and below
                above = i - 1
                below = i + 1

                # Conditional replacement: Check if above or below pixel is black (0)
                if (above >= 0 and output_grid[above, j] == 0) or \
                   (below < rows and output_grid[below, j] == 0):
                    output_grid[i, j] = 6

    return output_grid
```

