# 007bbfb7 • 002 • example_1 • investigate_coder

---
```python
"""
The output pattern is a 9x9 grid of orange cells with four white columns (0,1,2,3, and 6). The input pattern is copied to the output, with 0's not overwriting the background and 7's overriding the white background.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid filled with orange (7).
    output_grid = np.full((9, 9), 7, dtype=int)

    # Set columns 0, 1, 2, 3 and 6 to white (0).
    for i in range(4):
        output_grid[:, i] = 0
    output_grid[:, 6] = 0
    
    # Superimpose the input pattern onto the output grid.
    for i in range(3):
        for j in range(3):
            if input_grid[i, j] == 7:  # Only superimpose orange (7).
              for row in range(3):
                for col in range(3):
                  output_grid[i*3+row,j*3+col]= input_grid[i,j]

    return output_grid
```
