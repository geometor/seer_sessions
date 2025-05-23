```python
"""
Iterate through each cell of the input grid. If the cell's value is 0 (white),
keep it as 0 (white) in the output grid. If the cell's value is 1 (blue),
change it to 2 (red) in the output grid. Copy the content of last generated
row to a new row. Append this new row at the bottom of output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((input_grid.shape[0] + 1, input_grid.shape[1]), dtype=int)

    # change output pixels
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] == 1:
                output_grid[r, c] = 2
            else:
                output_grid[r,c] = input_grid[r,c]
    
    #copy last row to a new one and append
    output_grid[-1, :] = output_grid[-2, :]

    return output_grid.tolist()
```