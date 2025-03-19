# 9565186b • 012 • refine_coder

---
```python
"""
1. Identify Blue Objects: Find all contiguous regions (connected components) of blue (1) pixels in the input grid.
2. Preserve Blue Objects: Keep the pixels within these blue connected components unchanged in the output grid.
3. Transform Other Pixels to Gray: Change all other pixels (those not part of any identified blue connected component) to gray (5).
"""

import numpy as np
from scipy.ndimage import label

def find_blue_objects(grid):
    # Create a boolean mask for blue pixels
    blue_mask = (grid == 1)
    # Label connected components of blue pixels
    labeled_mask, num_objects = label(blue_mask)
    return labeled_mask, num_objects

def transform(input_grid):
    # Find blue objects (connected components)
    labeled_mask, _ = find_blue_objects(input_grid)

    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Iterate through all pixels
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is NOT part of a blue object
            if labeled_mask[i, j] == 0:
                # Change the pixel to gray (5)
                output_grid[i, j] = 5

    return output_grid
```
