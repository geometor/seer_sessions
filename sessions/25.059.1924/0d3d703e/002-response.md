# 0d3d703e • 002 • example_4 • investigate_coder

---
```python
"""
The input grid is a 3x3 grid of single-digit integers. Each digit in the input grid is replaced by a corresponding digit according to a fixed mapping. This mapping is consistent across all input/output pairs. The mapping is as follows: 3->4, 1->5, 2->6, 8->9, 5->1, 6->2, 9->8, 4->3. The output grid is the same dimensions as the input (3x3), with each number replaced based on the mapping.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Define the mapping
    mapping = {
        3: 4,
        1: 5,
        2: 6,
        8: 9,
        5: 1,
        6: 2,
        9: 8,
        4: 3
    }

    # change output pixels
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            output_grid[i, j] = mapping.get(input_grid[i, j], input_grid[i,j]) #.get handles key errors

    return output_grid
```
