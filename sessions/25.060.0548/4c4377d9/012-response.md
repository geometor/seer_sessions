# 4c4377d9 • 012 • refine_coder

---
```python
"""
The output grid is created by flipping each row of the input grid horizontally. The height and width of the output is the same as the height and width of the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels 
    for i in range(rows):
        output_grid[i] = input_grid[i][::-1]

    return output_grid
```
