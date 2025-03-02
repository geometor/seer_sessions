# 794b24be • 016 • refine_coder

---
```python
"""
Transforms a grid by placing a two-pixel red object at the top-left corner (0,0) and (0,1) 
if any blue pixels are present in the input grid. White pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.zeros_like(input_grid)  # Initialize output grid with zeros (white)

    # Check for the presence of any blue pixels
    blue_pixels = np.argwhere(input_grid == 1)
    
    if len(blue_pixels) > 0:  # If any blue pixels are found
        # Create the red object at the specified positions
        output_grid[0, 0] = 2  # Red pixel at (0, 0)
        output_grid[0, 1] = 2  # Red pixel at (0, 1)
    else:
        output_grid[:] = input_grid[:]

    return output_grid
```
