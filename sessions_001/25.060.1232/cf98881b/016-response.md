# cf98881b • 016 • example_3 • investigate_coder

---
```python
"""
1.  **Identify the Region of Interest:** Focus on the top-left 4x4 section.
2. **Extract by coordinates:** Select all elements that form a sub-grid determined by rows 0-3 and columns 0-3.
3.  **Output the Sub-grid**: construct an output grid of size 4x4, mirroring
    the color and position of these pixels in the sub-grid
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a 4x4 array.
    output_grid = np.zeros((4, 4), dtype=int)

    # Iterate through the top-left 4x4 section of the input grid.
    for i in range(4):
        for j in range(4):
            # Copy the pixel value from the input grid to the output grid.
            output_grid[i][j] = input_grid[i][j]

    return output_grid
```
