```python
"""
1. Examine the input 3x3 grid.
2. Select the value from the center cell in the input grid.
3. Create a new output grid with the same dimensions.
4. Fill all cells of the output grid with the selected value.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # get the center value
    center_row = input_grid.shape[0] // 2
    center_col = input_grid.shape[1] // 2
    center_value = input_grid[center_row, center_col]

    # change output pixels 
    output_grid[:] = center_value

    return output_grid
```
