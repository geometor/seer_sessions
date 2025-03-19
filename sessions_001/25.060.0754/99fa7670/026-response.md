# 99fa7670 • 026 • refine_coder

---
```python
"""
1.  **Examine** each row of the input grid.
2.  **Identify** pixels with the color blue (1) or gray (5).
3.  **If** a pixel is blue (1) or gray (5), **then** replace all pixels to the right of it in the same row with that pixel's color.
4. **If** a pixel is not blue (1) or gray(5), it is not changed.
5. If no pixels on a row are colors blue(1) or gray(5), the row will be unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid based on the color expansion rule."""

    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each row
    for i in range(rows):
        # Iterate through each pixel in the row from left to right
        for j in range(cols):
            # Check if the pixel is blue (1) or gray (5)
            if input_grid[i][j] == 1 or input_grid[i][j] == 5:
                # Expand the current pixel's color to the right
                for k in range(j, cols):
                    output_grid[i][k] = input_grid[i][j]

    return output_grid
```

