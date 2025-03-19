# d90796e8 • 008 • refine_coder

---
```python
"""
The transformation rule is as follows:

1. **Preserve '5' and '0':**  Cells with values '5' (gray) and '0' (white) in the input grid retain their values and positions in the output grid.
2. **First Row Propagation:** All pixels in the first row of the input grid are changed to the color of the pixel in [0,0].

"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # First Row Propagation: change all first row pixels to color at [0,0]
    first_row_val = output_grid[0,0]
    for j in range(output_grid.shape[1]):
        output_grid[0,j] = first_row_val

    return output_grid
```
