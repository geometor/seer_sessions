```python
"""
1.  **Identify Non-Zero Pixels:** Find all pixels in the input grid with values other than 0.

2.  **Conditional Horizontal Propagation (Rightward):**
    *   Iterate through the grid from left to right *and* top to bottom.
      * if the current value is not 0:
         * save value
      * if the current value *is* 0:
         * if there is a saved value, set this value to the saved value

3.  **Conditional Vertical Propagation (Downward):**
      - Iterate through the grid from top to bottom and left to right.
      - if the current value is not 0:
        - save the value
      - if the current value *is* 0:
        - if there is a saved value, set this value to the saved value
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    saved_value = 0

    # Conditional Horizontal Propagation (Rightward)
    for r in range(rows):
        saved_value = 0 # reset saved value for each row
        for c in range(cols):
            if output_grid[r, c] != 0:
                saved_value = output_grid[r,c]
            elif saved_value != 0:
                output_grid[r,c] = saved_value

    # Conditional Vertical Propagation (Downward)
    for c in range(cols):  # Iterate by columns first
        saved_value = 0  # reset saved_value for each column
        for r in range(rows):
            if output_grid[r, c] != 0:
                saved_value = output_grid[r,c]
            elif saved_value != 0:
                output_grid[r,c] = saved_value
    return output_grid
```