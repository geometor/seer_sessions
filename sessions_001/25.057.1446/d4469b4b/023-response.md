# d4469b4b • 023 • refine_coder

---
```python
"""
Transforms a 5x5 grid into a 3x3 grid based on the presence of blue pixels in overlapping 3x3 regions.  Each 3x3 region in the input maps directly to a pixel in the output. If the 3x3 region contains any blue pixels, the output pixel is gray; otherwise, it's white.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 3x3 array filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through the 3x3 overlapping regions
    for i in range(3):
        for j in range(3):
            # Define the 3x3 region in the input grid
            row_start = i
            row_end = i + 3
            col_start = j
            col_end = j + 3
            
            region = input_grid[row_start:row_end, col_start:col_end]

            # Check for the presence of blue (1) pixels in the region
            if np.any(region == 1):
                output_grid[i, j] = 5  # Set to gray (5)
            # else, output_grid[i,j] remains 0 (white) by initialization

    return output_grid.tolist()
```
