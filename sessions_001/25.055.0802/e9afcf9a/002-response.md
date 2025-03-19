# e9afcf9a • 002 • example_1 • investigate_coder

---
```python
"""
The transformation rule can be described as follows:

1.  **Maintain Grid Structure:** The input grid's dimensions (2x6) are preserved in the output grid.
2.  **Alternate Colors:** In each row of the output, the colors of the pixels alternate between green (3) and maroon (9).
3.  **Row 1 starts with original color:** first row starts with green(3).
4. **Row 2 starts with other color:** second row starts with maroon(9).

Essentially input becomes a checkerboard pattern of alternating green and maroon.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change output pixels 
    for r in range(rows):
        for c in range(cols):
            if r == 0: # First Row
                if c % 2 == 0:
                    output_grid[r,c] = 3
                else:
                    output_grid[r,c] = 9
            else: # Second Row
                if c % 2 == 0:
                    output_grid[r,c] = 9
                else:
                    output_grid[r,c] = 3

    return output_grid
```
