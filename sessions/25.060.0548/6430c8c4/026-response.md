# 6430c8c4 • 026 • example_4 • investigate_coder

---
```python
"""
The upper-left shape, orange in color, is replaced with the color green in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Focus on the upper left 4x4 subgrid of the original image.
    sub_grid = input_grid[:4, :4]
    
    # Translate orange color (7) in the input sub-grid to green (3).
    for i in range(4):
        for j in range(4):
            if sub_grid[i,j] == 7:
              output_grid[i,j] = 3

    return output_grid
```
