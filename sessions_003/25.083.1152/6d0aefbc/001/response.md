```python
"""
The transformation rule is to double each pixel in both dimensions, 
effectively creating a 2x2 "magnified" version of each original pixel.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each pixel both horizontally
    and vertically.
    """
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows * 2, cols * 2), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            # Duplicate the pixel value to the corresponding 2x2 block in the output grid
            output_grid[2*i:2*i+2, 2*j:2*j+2] = input_grid[i, j]

    return output_grid
```