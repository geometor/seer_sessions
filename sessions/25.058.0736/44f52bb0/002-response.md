# 44f52bb0 • 002 • example_1 • investigate_coder

---
```python
"""
Counts the occurrences of the color red (2) in the input grid and returns a 1x1 grid containing the color blue (1) if red appears.
"""

import numpy as np

def transform(input_grid):
    """
    Transform input_grid.
    """
    # initialize output_grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Count the occurrences of red (2)
    red_count = np.sum(input_grid == 2)

    # if red exists in input
    if(red_count > 0):
        # Set the output to blue (1)
        output_grid[0, 0] = 1
    else:
      output_grid[0, 0] = 0

    return output_grid
```
