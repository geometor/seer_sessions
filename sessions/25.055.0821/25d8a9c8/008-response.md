# 25d8a9c8 • 008 • example_2 • investigate_coder

---
```python
"""
The transformation identifies the middle row of the input grid. 
Pixels in the middle row of the input grid are transformed to gray (5) in the output grid. 
All other pixels in the output grid are set to white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)
    height, width = output_grid.shape

    # Set all pixels in the middle row of the output grid to gray (5).
    middle_row = height // 2
    output_grid[middle_row, :] = 5

    # set all other rows to white
    output_grid[:middle_row,:] = 0
    output_grid[middle_row+1:,:] = 0
    

    return output_grid
```

