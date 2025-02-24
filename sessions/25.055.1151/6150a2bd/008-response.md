# 6150a2bd • 008 • example_2 • investigate_coder

---
```python
"""
The input grid is rotated 180 degrees. The values are mirrored along the top-left to bottom-right diagonal.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid by 180 degrees and mirrors the values.
    """
    # Initialize output grid as a copy of the input grid.
    output_grid = np.array(input_grid)
    
    # Rotate the grid by 180 degrees.
    output_grid = np.rot90(output_grid, 2)

    # Mirror the values along the top-left to bottom-right diagonal of original grid.
    rows, cols = output_grid.shape
    mirrored_grid = np.copy(output_grid)
    for i in range(rows):
      for j in range(cols):
        output_grid[i,j] = mirrored_grid[rows - 1 - j, cols - 1 - i]
          
    return output_grid.tolist()
```
