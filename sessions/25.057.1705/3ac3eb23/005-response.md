# 3ac3eb23 • 005 • refine_coder

---
```python
"""
1.  Identify all pixels that are either red (color 2) or azure (color 8).
2.  Copy each identified pixel to the cell directly below it, *if* that cell exists (i.e., we are not at the bottom row).
3.  Preserve all other pixels in their original state and color.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Identify red (2) or azure (8) pixels
            if input_grid[r, c] == 2 or input_grid[r, c] == 8:
                # Copy to the cell below if it exists
                if r + 1 < rows:
                    output_grid[r + 1, c] = input_grid[r, c]

    return output_grid
```

