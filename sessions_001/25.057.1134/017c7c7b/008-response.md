# 017c7c7b • 008 • example_2 • investigate_coder

---
```python
"""
The transformation rule involves replacing all blue (1) pixels with red (2) pixels in a checkerboard pattern and increasing the height of the grid by adding three rows that continue the checkerboard pattern.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)

    # Replace all blue (1) pixels with red (2)
    output_grid[output_grid == 1] = 2
    
    # Get dimensions of original grid
    rows, cols = output_grid.shape
    
    # Create the extension rows as numpy array.  The existing output_grid establishes
    # the checkerboard pattern, so just duplicate a slice.
    extension = np.copy(output_grid[0:3,:])
    
    # Vertically stack to add to bottom
    output_grid = np.vstack((output_grid, extension))

    return output_grid
```
