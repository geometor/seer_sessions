```python
"""
The input grid is rotated 180 degrees to produce the output grid. This can be achieved by performing a horizontal flip followed by a vertical flip (or vice-versa). The positions of the elements are inverted both row-wise and column-wise.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid with the same dimensions as the input grid
    output_grid = np.copy(input_grid)
    rows = output_grid.shape[0]
    cols = output_grid.shape[1]

    # flip the grid horizontally
    output_grid = np.fliplr(output_grid)
    
    # flip the grid vertically
    output_grid = np.flipud(output_grid)
    

    return output_grid
```