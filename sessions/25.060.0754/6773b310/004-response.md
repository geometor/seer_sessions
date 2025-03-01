# 6773b310 • 004 • example_1 • investigate_coder

---
```python
"""
The program identifies the presence of magenta (6) within each 3x3 sub-region of the core area (excluding the azure border) and maps that to blue (1) in the output. Otherwise, the output is white(0). The azure border is effectively removed, and the grid is significantly down-sampled.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # 1. Identify the core region (remove azure border)
    core_grid = input_grid[1:rows-1, 1:cols-1]
    core_rows, core_cols = core_grid.shape

    # 2. Down-sample to 3x3 and apply color transformation
    output_grid = np.zeros((3, 3), dtype=int)
    for i in range(3):
        for j in range(3):
            # Extract 3x3 block
            block = core_grid[i*3:(i+1)*3, j*3:(j+1)*3]
            
            # Check for magenta (6) in the block
            if 6 in block:
                output_grid[i, j] = 1
            else:
                output_grid[i,j] = 0
            
    return output_grid.tolist()
```
