# aedd82e4 • 006 • refine_coder

---
```python
"""
The input is a 3x3 grid of pixels. Locate the pixel at the bottom-left corner (row 2, column 0, using 0-indexing). If this pixel is red (2), change its color to blue (1). All other pixels remain in the initial state (keep original values). Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change the color of the bottom-left pixel from red(2) to blue(1)
    if output_grid[2, 0] == 2:
      output_grid[2, 0] = 1

    return output_grid
```

