# d4469b4b • 034 • example_6 • investigate_coder

---
```python
"""
1. **Identify the region**: Examine the input grid and search for connected red pixels. A group of pixels can consist of pixels next to each other, or chained through other pixels by being next to it.

2.  **Condense into gray pixel region**: For each 3x1 subregion in the input, map the regions as follows:
    *   If the subregion is composed of at least one red pixel, then the output pixel is gray(5).
    *   Otherwise the subregion remains white (0).

3.  **Form Output Grid:** Create a 3x3 output grid based on the condensed regions.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros((3, 3), dtype=int)

    # Iterate through 3x1 subregions of the input grid
    for i in range(3):
        for j in range(3):
            # Extract the 3x1 subregion
            subregion = input_grid[i:i+3, j:j+1]
            # Check if any pixel in the subregion is red (2)
            if np.any(subregion == 2):
                output_grid[i, j] = 5  # Set corresponding output pixel to gray (5)
            # output remains 0 (white) by default
            
    return output_grid.tolist()
```
