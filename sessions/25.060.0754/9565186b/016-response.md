# 9565186b • 016 • refine_coder

---
```python
"""
The transformation rule is as follows:

1.  Iterate through every pixel of the input grid.
2.  If a pixel is azure (color code 8), change it to gray (color code 5).
3.  If a pixel is any color other than azure, leave it unchanged. Specifically, red (color 2) pixels are not modified.
4.  The output grid has the same dimensions (height and width) as the input grid. No pixels are added or removed, and the grid structure is preserved.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.  This ensures
    # the dimensions are the same and that we don't modify the original.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel's coordinates using NumPy's ndindex.
    for index in np.ndindex(input_grid.shape):
        # Check if the current pixel is azure (color code 8).
        if input_grid[index] == 8:
            # Replace azure pixels with gray pixels (color code 5).
            output_grid[index] = 5
        # Implicit else:  If not azure, no change is made due to the copy.

    return output_grid
```

