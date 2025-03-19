# ea786f4a • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to replace the single central white pixel with a cross-shaped arrangement of white pixels, keeping all other pixels red.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by creating a cross of white pixels centered at the original white pixel's location.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the dimensions of the grid.
    rows, cols = input_grid.shape
    
    # Find the center coordinates.  We assume a single white pixel in input.
    center_row, center_col = np.where(input_grid == 0)
    if len(center_row) > 0:  # Check if a white pixel was found
       center_row, center_col = center_row[0], center_col[0]
    else:
      return output_grid # if no white cell, return original grid
    

    # Create the cross by setting the appropriate pixels to white (0).
    output_grid[center_row, :] = 0  # Set entire row to white
    output_grid[:, center_col] = 0  # Set entire column to white

    return output_grid
```
