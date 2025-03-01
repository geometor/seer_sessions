# d4469b4b • 020 • example_4 • investigate_coder

---
```python
"""
The transformation rule involves dividing the 5x5 input grid into overlapping 3x3 regions. If a region contains at least one blue (1) pixel, the corresponding pixel in the 3x3 output grid is set to gray (5). Otherwise, if the region contains only white (0) pixels, the corresponding output pixel is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 5x5 grid into a 3x3 grid based on the presence of blue pixels in overlapping 3x3 regions.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)  # Initialize output grid with white (0)

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
            else:
                output_grid[i, j] = 0 # remains white

    return output_grid.tolist()
```
