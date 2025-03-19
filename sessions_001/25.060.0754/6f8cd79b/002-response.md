# 6f8cd79b • 002 • example_4 • investigate_coder

---
```python
"""
The transformation rule is to create an azure border around the original white grid, maintaining the inner white pixels. The border is always one pixel thick.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.full((rows, cols), 8, dtype=int)

    # change output pixels 
    # fill interior with 0s
    for i in range(1,rows-1):
        for j in range(1, cols-1):
            output_grid[i][j] = 0

    return output_grid
```
