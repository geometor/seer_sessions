# 44f52bb0 • 012 • example_3 • investigate_coder

---
```python
"""
The input grid is reduced to a single pixel of color blue (1), regardless of the input grid's content.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a 1x1 grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the single pixel in output grid to blue (1)
    output_grid[0, 0] = 1

    return output_grid
```
