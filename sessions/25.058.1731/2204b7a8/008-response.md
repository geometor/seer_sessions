# 2204b7a8 • 008 • refine_coder

---
```python
"""
The program performs a color substitution on a grid of pixels. The substitutions are:

- Green (3) becomes Blue (1).
- Orange (7) becomes Magenta (6).
- Yellow (4) becomes Green (3).
- Blue (1) becomes Yellow (4).

All other colors remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid.
    for row_index, row in enumerate(output_grid):
        for col_index, pixel_value in enumerate(row):
            # Apply the color transformations.
            if pixel_value == 3:
                output_grid[row_index, col_index] = 1
            elif pixel_value == 7:
                output_grid[row_index, col_index] = 6
            elif pixel_value == 4:
                output_grid[row_index, col_index] = 3
            elif pixel_value == 1:
                output_grid[row_index, col_index] = 4

    return output_grid
```

