# c3e719e8 • 006 • example_1 • investigate_coder

---
```python
"""
The input grid is replicated three times horizontally and three times vertically to form a 9x9 output grid. The remaining cells in the output grid are filled with zeros. The replicated grids are placed at positions (0,0), (3,3), and (6,6) with additional copies to tile the entire 3 x 3 grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_shape = np.array(input_grid).shape
    output_shape = (input_shape[0] * 3, input_shape[1] * 3)
    output_grid = np.zeros(output_shape, dtype=int)

    # change output pixels 
    for i in range(input_shape[0]):
        for j in range(input_shape[1]):
            for m in range(3):
                for n in range(3):
                    output_grid[i + input_shape[0] * m, j + input_shape[1] * n ] = input_grid[i][j]

    return output_grid
```
