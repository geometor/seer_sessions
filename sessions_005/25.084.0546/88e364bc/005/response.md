```python
"""
The output grid is the same size as the input grid. All orange (7) pixels in the input grid are changed to orange (4) pixels in the output grid. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all positions of orange (7) pixels
    orange_pixels = np.argwhere(output_grid == 7)

    # Change all orange (7) pixels to orange (4)
    for pos in orange_pixels:
        output_grid[pos[0], pos[1]] = 4

    return output_grid
```
