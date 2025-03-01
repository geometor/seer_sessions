# 794b24be • 020 • example_4 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid. If a pixel is blue (1), check if any
adjacent pixels in the same row are white (0). If so, change any blue pixels in the top row to red (2).
Otherwise, the pixel's value remains unchanged. Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check for white adjacency in the top row
    has_white_adjacent = False
    for r in range(rows):
        for c in range(cols):
             if input_grid[r,c] == 1:
                if c > 0 and input_grid[r, c-1] == 0:
                    has_white_adjacent = True
                if c < cols - 1 and input_grid[r, c+1] == 0:
                    has_white_adjacent= True
    
    if has_white_adjacent:
      # change output pixels
        for c in range(cols):
          if output_grid[0,c] == 1:
             output_grid[0,c] = 2

    return output_grid
```
