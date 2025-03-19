# 85c4e7cd • 008 • refine_coder

---
```python
"""
The transformation involves changing the colors of nested squares within a grid while preserving their spatial arrangement. A fixed color mapping is applied to each pixel in the input grid to produce the output grid. The mapping is as follows:

*   Yellow (4) becomes Azure (8)
*   Red (2) becomes Grey (5)
*   Blue (1) becomes Green (3)
*   Green (3) becomes Blue (1)

The input and output grids have identical dimensions. The nested square structure and relative sizes of the squares are the same in the input and the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # define the color mapping
    color_map = {
        4: 8,  # Yellow -> Azure
        2: 5,  # Red -> Grey
        1: 3,  # Blue -> Green
        3: 1,  # Green -> Blue
    }

    # iterate through each pixel in the input grid
    for i in range(rows):
        for j in range(cols):
            # get the color of the current pixel
            input_color = input_grid[i, j]
            # apply the color mapping and update the corresponding pixel in the output grid
            # Use .get() to handle potential missing keys (colors not in the map)
            output_grid[i, j] = color_map.get(input_color, input_color)

    return output_grid
```

