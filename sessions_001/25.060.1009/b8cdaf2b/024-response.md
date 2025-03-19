# b8cdaf2b • 024 • example_4 • investigate_coder

---
```python
"""
1.  **Identify the Bottom Object:** Find the horizontal line of red and yellow pixels at the bottom of the input grid (rows 6 and 7).

2.  **Place Yellow Pixels:**
     Locate columns in the red/yellow object where yellow pixels are present. For each located column, place a yellow pixel at row index `[height - 4]` and `[height-3]` , where `height` represents the height of the input grid.

3. Leave other pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = input_grid.shape[0]

    # Find columns with yellow pixels in the bottom two rows
    for col in range(input_grid.shape[1]):
        if input_grid[height - 1, col] == 4:
            # Place yellow pixels
            output_grid[height - 4, col] = 4
            output_grid[height - 3, col] = 4
            
    return output_grid
```
