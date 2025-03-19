# a3df8b1e • 004 • example_1 • investigate_coder

---
```python
"""
The transformation creates a checkerboard-like pattern, by making alternating columns have opposing values, which are opposite, and each of which alternate from row to row.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels 
    for c in range(cols):
        for r in range(rows):
            if c % 2 == 0:  # Even column
                output_grid[r, c] = r % 2
            else:  # Odd column
                output_grid[r, c] = 1 - (r % 2)

    return output_grid
```
