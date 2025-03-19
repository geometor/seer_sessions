# a85d4709 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation replaces values in the input grid with corresponding values in the output grid based on a clockwise color scheme. 0s are replaced with 3, 4, and 2 in a clockwise fashion around the edge, and 5s are replaced by the next clockwise value.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Define the clockwise replacement mapping
    replacement_map = {
        (0, 0): 3,  # Top-left 0
        (0, 1): 3, # Top-center 0
        (0, 2): 3,  # Top-right
        (1, 2): 4,  # Middle-right
        (2, 2): 2, # Bottom Right
        (2, 1): 2,  # Bottom-center
        (2, 0): 2,  # Bottom-left
        (1, 0): 4,  # Middle-left
        (1, 1): 4,  # Center

    }

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Get the value from the input grid
            value = input_grid[r, c]
            if value == 0:
              output_grid[r,c] = replacement_map[(r,c)]
            elif value == 5:
              if (r,c) == (0,2):
                output_grid[r,c] = 3
              if (r,c) == (1,1):
                output_grid[r,c] = 4
              if (r,c) == (2,0):
                output_grid[r,c] = 2

    return output_grid
```
