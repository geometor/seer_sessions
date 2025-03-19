# 27a28665 • 030 • example_6 • investigate_coder

---
```python
"""
Counts the number of yellow (4) pixels in the input grid. If any of the border pixels are a different value than the center pixel, return a 1x1 grid with a blue pixel (1).
"""

import numpy as np

def transform(input_grid):
    # Convert input to numpy array
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # get center pixel
    center_pixel = input_array[rows//2, cols//2]

    # compare border to center
    different_border_pixel = False
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and input_array[r,c] != center_pixel:
                different_border_pixel = True
    
    # Create output grid
    if different_border_pixel:
        output_grid = np.array([[1]])
    else:
        output_grid = np.array([[center_pixel]])

    return output_grid.tolist()
```
