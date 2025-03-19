# a699fb00 • 012 • refine_coder

---
```python
"""
1.  **Find Blue Pixels:** Iterate through the input grid, identifying all pixels with the color blue (value 1).
2.  **Iterate to the Right:** For each blue pixel found:
    *   Start at the position immediately to its right.
    *   While the current position is within the grid boundaries and the pixel color is white (0):
        *   Change the pixel's color to red (2).
        *   Move one position to the right.
3. Return the modified grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            # Find Blue Pixels
            if input_grid[r, c] == 1:
                # Iterate to the Right
                c_current = c + 1
                while c_current < cols and output_grid[r, c_current] == 0:
                    output_grid[r, c_current] = 2
                    c_current += 1
    return output_grid
```

