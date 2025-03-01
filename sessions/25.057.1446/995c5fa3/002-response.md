# 995c5fa3 • 002 • example_1 • investigate_coder

---
```python
"""
Transforms a grid of gray and white pixels into a smaller 3x3 grid of red, azure, and green pixels.
The transformation is based on dividing the input grid into three horizontal sections based on white regions,
and mapping each section to a row in the output grid with a specific color.
"""

import numpy as np

def get_white_regions_bounds(input_grid):
    """
    Identify the row indices of distinct white pixel regions
    """
    white_rows = np.where(np.any(input_grid == 0, axis=1))[0]
    
    bounds = []
    start = white_rows[0]
    
    for i in range(len(white_rows)-1):
      if white_rows[i+1] - white_rows[i] > 1:
          bounds.append((start, white_rows[i]))
          start = white_rows[i+1]
    bounds.append((start, white_rows[-1]))

    return bounds

def transform(input_grid):
    """
    Transforms the input grid according to the described rules.
    """
    # Initialize the output grid as a 3x3 array.
    output_grid = np.zeros((3, 3), dtype=int)

    # Identify bounds of distinct white regions
    bounds = get_white_regions_bounds(input_grid)

    # Map sections to colors and fill output rows.
    color_map = {
        0: 2,  # First section: red
        1: 8,  # Second section: azure
        2: 3   # Third section: green
    }
    
    row_index = 0
    for bound in bounds:
      if row_index < 3:
        output_grid[row_index, :] = color_map[row_index]
      row_index+=1
    
    return output_grid
```
