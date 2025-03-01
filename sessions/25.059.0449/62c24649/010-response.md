# 62c24649 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is to expand the input grid by a factor of 2. Each pixel in the input grid is replicated as a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_shape = input_grid.shape
    output_shape = (input_shape[0] * 2, input_shape[1] * 2)
    output_grid = np.zeros(output_shape, dtype=int)

    # change output pixels 
    for i in range(input_shape[0]):
        for j in range(input_shape[1]):
            # Replicate each input pixel into a 2x2 block in the output.
            output_grid[2*i:2*i+2, 2*j:2*j+2] = input_grid[i, j]

    return output_grid
```
