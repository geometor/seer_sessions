# d037b0a7 • 018 • refine_coder

---
```python
"""
1.  Identify the top-left pixel color: Determine the color of the pixel at position (0, 0) of the input grid.
2.  Fill the output grid:  Create an output grid with the same dimensions as the input grid. Fill the entire output grid with the color identified in step 1.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.full(input_grid.shape, input_grid[0, 0])

    # change output pixels - already done in initialization

    return output_grid
```
