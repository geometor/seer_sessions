# 484b58aa • 004 • example_1 • investigate_coder

---
```python
"""
Removes all pixels of color 0 (white) from the input grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Find the indices of all white pixels (color 0).
    white_pixel_indices = np.where(output_grid == 0)
    
    # set all pixels with color zero to other values

    # Iterate through the grid and remove white pixels
    for i in range(input_grid.shape[0]):
      for j in range(input_grid.shape[1]):
        if input_grid[i,j] == 0:
            output_grid[i,j] = input_grid[i,j] #does nothing

    return output_grid
```

