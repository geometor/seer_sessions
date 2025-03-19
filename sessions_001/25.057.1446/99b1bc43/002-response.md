# 99b1bc43 • 002 • example_1 • investigate_coder

---
```python
"""
1. Locate the 2x2 block at the bottom right corner of the input grid.
2. Change all pixels within this 2x2 block to green (color code 3) in the output grid.
3. Fill the remaining upper region of the output grid with white (color code 0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize output grid as all zeros with size 4x4
    output_grid = np.zeros((4, 4), dtype=int)

    # Get dimensions of the input grid
    input_rows, input_cols = input_grid.shape

    # locate the bottom right 2 x 2 region
    bottom_right_region = input_grid[input_rows-2:input_rows, input_cols-2:input_cols]
   
    # set the same region in output to green
    output_grid[2:4, 2:4] = 3

    return output_grid
```
