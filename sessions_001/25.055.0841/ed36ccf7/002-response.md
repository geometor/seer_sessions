# ed36ccf7 • 002 • example_1 • investigate_coder

---
```python
"""
The transformation repositions a 1x2 block of white pixels (0) from the top-right to the top-left of a 3x3 grid, filling the remaining cells with maroon pixels (9).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving the white pixels to the top-left.
    """
    # Initialize the output grid with maroon pixels.
    output_grid = np.full((3, 3), 9)

    # Place the white pixels at the top-left.
    output_grid[0, 0] = 0
    output_grid[1, 0] = 0

    return output_grid
```
