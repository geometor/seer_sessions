# e8dc4411 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation involves assessing the location of azure pixels, and possibly replicating azure pixels to the right, under specific conditions, while not altering the background.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure pixels and apply transformation rules
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                # If the azure pixel is in the top two rows and the 3rd row has a yellow pixel to the right,
                #or, if the azure is in the top two rows, and the 3rd row has an azure pixel to the right of it,
                #replicate to the right
                if r < rows -1 and c+1<cols:
                  if (r < 2 and input_grid[r+1,c+1] ==4) or (r < 2 and input_grid[r, c+1] == 8):
                    if c + 1 < cols:
                        output_grid[r, c + 1] = 8

                #If an azure is in the top row on the right hand side of another azure pixel and is bordered
                #to the lower left by a yellow pixel, it transforms to an azure (8) pixel.

                if r>0 and c+1 < cols and c>0:
                    if (r==0 and input_grid[r,c-1]==8 and input_grid[r+1,c-1]==4):
                       output_grid[r,c]=8

    return output_grid
```
