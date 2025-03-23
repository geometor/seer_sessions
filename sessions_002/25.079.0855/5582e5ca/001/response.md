```python
"""
Examine the input grid and identify the value in the top right corner.
Create a new 3x3 grid and fill all cells of the new grid with the identified value.
Return the new grid.
"""

import numpy as np

def transform(input_grid):
    # Get the value in the top-right corner of the input grid.
    top_right_value = input_grid[0][-1]

    # Create a new 3x3 grid filled with the top-right value.
    output_grid = np.full((3, 3), top_right_value)

    return output_grid
```
