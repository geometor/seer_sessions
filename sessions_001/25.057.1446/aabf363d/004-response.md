# aabf363d • 004 • refine_coder

---
```python
"""
1. Identify all pixels with the color red (value 2) in the input grid.
2. Identify all pixels with the color yellow (value 4) in the input grid.
3. Change the color of all of the pixels identified in step one to yellow (value 4).
4. Leave all other colors intact.
5. The resulting grid is the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all red pixels
    red_pixels = np.argwhere(input_grid == 2)

    # Change all red pixels to yellow
    for r, c in red_pixels:
        output_grid[r, c] = 4

    return output_grid
```
