# ed36ccf7 • 002 • example_1 • investigate_coder

---
```python
"""
The input grid is transformed by changing the top-middle cell to white if it is originally maroon, copying all the rest of the left most colum, duplicating the white color to the cell underneath and keeping the rest of the input grid, effectively creating a 2x1 vertical domino of white colored cells.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change the top-middle cell to white (0)
    output_grid[0, 1] = 0
    
    #Copy first column
    output_grid[:,0] = input_grid[:,0]

    # duplicate the white color to the cell underneath if top-left corner is also white
    if output_grid[0,0] == 0:
      output_grid[1, 0] = 0

    return output_grid
```
