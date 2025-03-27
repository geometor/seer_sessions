```python
"""
The transformation rule involves a patterned expansion of the input grid. The output grid is created by:
1. Doubling the input horizontally.
2. Doubling the result vertically.
3. Doubling, mirroring, and flipping the colors of the input, placing the result in a border around the doubled input.
"""

import numpy as np

def transform(input_grid):
    # Convert input_grid to numpy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Double the input horizontally
    h_doubled = np.concatenate((input_grid, input_grid[:, ::-1]), axis=1)
    
    # 2. Double the result vertically
    output_grid = np.concatenate((h_doubled, h_doubled[::-1,:]), axis=0)
    
    return output_grid.tolist()
```