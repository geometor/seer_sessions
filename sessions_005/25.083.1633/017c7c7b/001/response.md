```python
"""
1.  **Substitution:** Iterate through each cell of the input grid. If a cell's value is 1 (blue), replace it with 2 (red) in the output grid. Maintain all 0 (white) values.
2. **Extend Height**: The output grid is always equal or greater height than the input. Create new rows with the `0 2 0` pattern to pad the output.
The output grid height appears to always be odd, so use the `0 2 0` pattern and stop when the next full pattern won't fit.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    
    # change output pixels 
    output_grid[output_grid == 1] = 2

    # extend height
    h = output_grid.shape[0]
    if h % 2 == 0:
        h += 3
    else:
        h += 2

    new_output_grid = np.zeros((h, 3), dtype=int)
    new_output_grid[:,1] = 2

    for i in range(output_grid.shape[0]):
        new_output_grid[i,:] = output_grid[i,:]


    return new_output_grid.tolist()
```